"""
OCR Processor - Extracts text from images of math problems.

This module:
1. Takes an image (photo or screenshot)
2. Uses EasyOCR for text extraction
3. Returns extracted text with confidence score
"""

from pathlib import Path

# Import our config
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import OCR_CONFIDENCE_THRESHOLD


class OCRProcessor:
    """
    Processes image input to extract math problems.
    """
    
    def __init__(self):
        """Initialize the OCR processor."""
        self.name = "OCR Processor"
        self.confidence_threshold = OCR_CONFIDENCE_THRESHOLD
        self.easyocr_reader = None
        self._init_easyocr()
    
    def _init_easyocr(self):
        """Try to initialize EasyOCR."""
        try:
            import easyocr
            self.easyocr_reader = easyocr.Reader(["en"], gpu=False)
            print("✅ EasyOCR initialized")
        except Exception as e:
            print(f"⚠️ EasyOCR not available: {e}")
            self.easyocr_reader = None
    
    def process(self, image_path: str = None, image_bytes: bytes = None) -> dict:
        """
        Process an image to extract math problem text.
        
        Args:
            image_path: Path to the image file
            image_bytes: Raw image bytes (from upload)
        
        Returns:
            Dictionary with extracted text and metadata
        """
        if not image_path and not image_bytes:
            return {
                "processor": self.name,
                "success": False,
                "error": "No image provided",
                "processed_text": "",
                "confidence": 0.0
            }
        
        # Read image bytes if path is given
        if image_path and not image_bytes:
            try:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
            except Exception as e:
                return {
                    "processor": self.name,
                    "success": False,
                    "error": f"Could not read image: {str(e)}",
                    "processed_text": "",
                    "confidence": 0.0
                }
        
        # Try EasyOCR
        easyocr_result = self._try_easyocr(image_path, image_bytes)
        
        return self._format_result(easyocr_result)
    
    def _try_easyocr(self, image_path: str, image_bytes: bytes) -> dict:
        """
        Try to extract text using EasyOCR.
        
        Args:
            image_path: Path to the image
            image_bytes: Raw image bytes
        
        Returns:
            Dictionary with OCR results
        """
        if self.easyocr_reader is None:
            return {
                "method": "easyocr",
                "success": False,
                "text": "",
                "confidence": 0.0,
                "error": "EasyOCR not available"
            }
        
        try:
            # EasyOCR can read from file path or numpy array
            if image_path:
                results = self.easyocr_reader.readtext(image_path)
            else:
                # Convert bytes to numpy array
                import numpy as np
                from PIL import Image
                import io
                
                image = Image.open(io.BytesIO(image_bytes))
                image_array = np.array(image)
                results = self.easyocr_reader.readtext(image_array)
            
            if not results:
                return {
                    "method": "easyocr",
                    "success": False,
                    "text": "",
                    "confidence": 0.0,
                    "error": "No text detected in image"
                }
            
            # Combine all detected text
            texts = []
            confidences = []
            
            for (bbox, text, confidence) in results:
                texts.append(text)
                confidences.append(confidence)
            
            combined_text = " ".join(texts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            return {
                "method": "easyocr",
                "success": True,
                "text": combined_text,
                "confidence": round(avg_confidence, 3),
                "details": [
                    {"text": t, "confidence": round(c, 3)}
                    for t, c in zip(texts, confidences)
                ]
            }
            
        except Exception as e:
            return {
                "method": "easyocr",
                "success": False,
                "text": "",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _format_result(self, ocr_result: dict) -> dict:
        """
        Format the OCR result as final output.
        
        Args:
            ocr_result: Result from OCR method
        
        Returns:
            Formatted result dictionary
        """
        if not ocr_result["success"]:
            return {
                "processor": self.name,
                "success": False,
                "error": ocr_result.get("error", "OCR failed"),
                "processed_text": "",
                "confidence": 0.0,
                "input_type": "image"
            }
        
        # Check if confidence is below threshold
        needs_review = ocr_result["confidence"] < self.confidence_threshold
        
        return {
            "processor": self.name,
            "success": True,
            "processed_text": ocr_result["text"],
            "confidence": ocr_result["confidence"],
            "method_used": ocr_result["method"],
            "needs_review": needs_review,
            "input_type": "image"
        }
    
    def needs_human_review(self, result: dict) -> bool:
        """
        Check if the OCR result needs human review.
        
        Args:
            result: Output from process()
        
        Returns:
            True if human review is needed
        """
        if not result.get("success", False):
            return True
        
        if result.get("needs_review", False):
            return True
        
        if result.get("confidence", 0.0) < self.confidence_threshold:
            return True
        
        return False
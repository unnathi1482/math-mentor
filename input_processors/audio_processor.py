"""
Audio Processor - Converts spoken math problems to text.

This module:
1. Takes an audio file (recorded or uploaded)
2. Uses Groq's Whisper API for speech-to-text
3. Cleans up math-specific phrases
4. Returns transcript with confidence score
"""

import tempfile
import os
from pathlib import Path
from groq import Groq

# Import our config
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import GROQ_API_KEY, ASR_CONFIDENCE_THRESHOLD


class AudioProcessor:
    """
    Processes audio input to extract math problems.
    """
    
    def __init__(self):
        """Initialize the audio processor."""
        self.name = "Audio Processor"
        self.client = Groq(api_key=GROQ_API_KEY)
        self.confidence_threshold = ASR_CONFIDENCE_THRESHOLD
    
    def process(self, audio_path: str = None, audio_bytes: bytes = None, file_name: str = "audio.wav") -> dict:
        """
        Process audio input to extract math problem text.
        
        Args:
            audio_path: Path to the audio file
            audio_bytes: Raw audio bytes (from upload)
            file_name: Name of the audio file (for format detection)
        
        Returns:
            Dictionary with transcribed text and metadata
        """
        if not audio_path and not audio_bytes:
            return {
                "processor": self.name,
                "success": False,
                "error": "No audio provided",
                "processed_text": "",
                "confidence": 0.0
            }
        
        # Step 1: Transcribe the audio
        transcription_result = self._transcribe(audio_path, audio_bytes, file_name)
        
        if not transcription_result["success"]:
            return {
                "processor": self.name,
                "success": False,
                "error": transcription_result.get("error", "Transcription failed"),
                "processed_text": "",
                "confidence": 0.0,
                "input_type": "audio"
            }
        
        raw_transcript = transcription_result["text"]
        
        # Step 2: Clean up math-specific phrases
        cleaned_result = self._basic_math_cleanup(raw_transcript)
        
        # Step 3: Determine confidence
        confidence = self._estimate_confidence(raw_transcript, cleaned_result)
        needs_review = confidence < self.confidence_threshold
        
        return {
            "processor": self.name,
            "success": True,
            "raw_transcript": raw_transcript,
            "processed_text": cleaned_result,
            "confidence": confidence,
            "needs_review": needs_review,
            "input_type": "audio"
        }
    
    def _transcribe(self, audio_path: str, audio_bytes: bytes, file_name: str) -> dict:
        """
        Transcribe audio using Groq's Whisper API.
        
        Args:
            audio_path: Path to audio file
            audio_bytes: Raw audio bytes
            file_name: Name of the audio file
        
        Returns:
            Dictionary with transcription result
        """
        temp_file_path = None
        
        try:
            # If we have bytes but no path, save to temp file
            if audio_bytes and not audio_path:
                # Get file extension
                extension = os.path.splitext(file_name)[1] if file_name else ".wav"
                if not extension:
                    extension = ".wav"
                
                # Save to temp file
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=extension
                )
                temp_file.write(audio_bytes)
                temp_file.close()
                temp_file_path = temp_file.name
                audio_path = temp_file_path
            
            # Call Groq Whisper API
            with open(audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-large-v3",
                    language="en",
                    prompt="This is a math problem. It may contain mathematical terms like integral, derivative, sine, cosine, square root, equation, matrix, probability, factorial, and variable names like x, y, z."
                )
            
            return {
                "success": True,
                "text": transcript.text
            }
            
        except Exception as e:
            return {
                "success": False,
                "text": "",
                "error": str(e)
            }
        finally:
            # Clean up temp file
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except Exception:
                    pass
    
    def _basic_math_cleanup(self, text: str) -> str:
        """
        Basic cleanup of math phrases.
        
        Args:
            text: Raw transcript text
        
        Returns:
            Text with basic math replacements
        """
        replacements = {
            "x squared": "x²",
            "x square": "x²",
            "y squared": "y²",
            "y square": "y²",
            "squared": "²",
            "cubed": "³",
            "square root of": "√",
            "square root": "√",
            "cube root of": "∛",
            "to the power of": "^",
            "raised to": "^",
            "plus": "+",
            "minus": "-",
            "times": "×",
            "divided by": "÷",
            "equals": "=",
            "equal to": "=",
            "greater than or equal to": "≥",
            "less than or equal to": "≤",
            "greater than": ">",
            "less than": "<",
            "not equal to": "≠",
            "pi": "π",
            "theta": "θ",
            "alpha": "α",
            "beta": "β",
            "gamma": "γ",
            "delta": "δ",
            "sigma": "σ",
            "lambda": "λ",
            "infinity": "∞",
            "integral of": "∫",
            "summation of": "Σ",
            "derivative of": "d/dx",
        }
        
        result = text
        for old, new in replacements.items():
            result = result.replace(old, new)
            # Also try with capital first letter
            result = result.replace(old.capitalize(), new)
        
        return result
    
    def _estimate_confidence(self, raw_transcript: str, cleaned_text: str) -> float:
        """
        Estimate confidence of the transcription.
        
        Args:
            raw_transcript: Original transcript
            cleaned_text: Cleaned transcript
        
        Returns:
            Confidence score between 0.0 and 1.0
        """
        confidence = 0.85  # Base confidence for Whisper
        
        # Lower confidence if transcript is very short
        if len(raw_transcript.split()) < 3:
            confidence -= 0.2
        
        # Lower confidence if transcript is very long (might have errors)
        if len(raw_transcript.split()) > 50:
            confidence -= 0.1
        
        # Lower confidence if there are many numbers (harder to transcribe)
        number_count = sum(1 for char in raw_transcript if char.isdigit())
        if number_count > 10:
            confidence -= 0.1
        
        # Higher confidence if common math words are detected
        math_words = ["solve", "find", "calculate", "equation", "derivative", "integral", "probability"]
        math_word_count = sum(1 for word in math_words if word in raw_transcript.lower())
        if math_word_count > 0:
            confidence += 0.05
        
        # Keep confidence in valid range
        confidence = max(0.0, min(1.0, confidence))
        
        return round(confidence, 3)
    
    def needs_human_review(self, result: dict) -> bool:
        """
        Check if the transcription needs human review.
        
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
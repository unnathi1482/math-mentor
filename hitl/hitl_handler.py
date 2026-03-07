"""
HITL Handler - Manages Human-in-the-Loop interactions.

This module:
1. Determines when human input is needed
2. Formats questions for the user
3. Processes human corrections
4. Stores corrections for future learning
"""

from pathlib import Path

# Import our modules
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import (
    OCR_CONFIDENCE_THRESHOLD,
    ASR_CONFIDENCE_THRESHOLD,
    VERIFIER_CONFIDENCE_THRESHOLD
)
from memory.memory_store import MemoryStore


class HITLHandler:
    """
    Handles Human-in-the-Loop interactions.
    """
    
    def __init__(self):
        """Initialize the HITL handler."""
        self.name = "HITL Handler"
        self.memory_store = MemoryStore()
    
    def should_trigger_hitl(self, pipeline_result: dict) -> bool:
        """
        Determine if HITL should be triggered based on pipeline results.
        
        Args:
            pipeline_result: Complete results from orchestrator
        
        Returns:
            True if human input is needed
        """
        # Check if already flagged
        if pipeline_result.get("needs_hitl", False):
            return True
        
        # Check OCR confidence
        if self._check_ocr_trigger(pipeline_result):
            return True
        
        # Check audio confidence
        if self._check_audio_trigger(pipeline_result):
            return True
        
        # Check parser clarification
        if self._check_parser_trigger(pipeline_result):
            return True
        
        # Check verifier confidence
        if self._check_verifier_trigger(pipeline_result):
            return True
        
        return False
    
    def _check_ocr_trigger(self, pipeline_result: dict) -> bool:
        """Check if OCR confidence is too low."""
        # Check if input was image
        raw_input_type = pipeline_result.get("raw_input", "")
        
        # Look for OCR confidence in pipeline
        # This would come from input processing step
        # For now, check if explicitly marked
        return False  # Will be set by OCR processor
    
    def _check_audio_trigger(self, pipeline_result: dict) -> bool:
        """Check if audio transcription confidence is too low."""
        # Similar to OCR check
        return False  # Will be set by audio processor
    
    def _check_parser_trigger(self, pipeline_result: dict) -> bool:
        """Check if parser needs clarification."""
        parsed = pipeline_result.get("parsed", {})
        return parsed.get("needs_clarification", False)
    
    def _check_verifier_trigger(self, pipeline_result: dict) -> bool:
        """Check if verifier confidence is too low."""
        verification = pipeline_result.get("verification", {})
        confidence = verification.get("confidence", 1.0)
        
        return confidence < VERIFIER_CONFIDENCE_THRESHOLD
    
    def get_hitl_type(self, pipeline_result: dict) -> str:
        """
        Determine what type of HITL is needed.
        
        Args:
            pipeline_result: Complete results from orchestrator
        
        Returns:
            Type: "ocr_review", "audio_review", "clarification", "verification", or "user_request"
        """
        if pipeline_result.get("hitl_type"):
            return pipeline_result.get("hitl_type")
        
        # Check triggers in order of priority
        parsed = pipeline_result.get("parsed", {})
        if parsed.get("needs_clarification", False):
            return "clarification"
        
        verification = pipeline_result.get("verification", {})
        if verification.get("confidence", 1.0) < VERIFIER_CONFIDENCE_THRESHOLD:
            return "verification"
        
        return "general_review"
    
    def format_hitl_request(self, pipeline_result: dict) -> dict:
        """
        Format a request for human input.
        
        Args:
            pipeline_result: Complete results from orchestrator
        
        Returns:
            Dictionary with formatted HITL request
        """
        hitl_type = self.get_hitl_type(pipeline_result)
        
        if hitl_type == "clarification":
            return self._format_clarification_request(pipeline_result)
        
        elif hitl_type == "verification":
            return self._format_verification_request(pipeline_result)
        
        elif hitl_type == "ocr_review":
            return self._format_ocr_review_request(pipeline_result)
        
        elif hitl_type == "audio_review":
            return self._format_audio_review_request(pipeline_result)
        
        else:
            return self._format_general_review_request(pipeline_result)
    
    def _format_clarification_request(self, pipeline_result: dict) -> dict:
        """Format a clarification request."""
        parsed = pipeline_result.get("parsed", {})
        
        return {
            "type": "clarification",
            "title": "⚠️ Need Clarification",
            "message": parsed.get("clarification_question", "Could you clarify the problem?"),
            "extracted_text": parsed.get("raw_input", ""),
            "allow_edit": True,
            "buttons": ["Submit Clarification", "Cancel"]
        }
    
    def _format_verification_request(self, pipeline_result: dict) -> dict:
        """Format a verification request."""
        verification = pipeline_result.get("verification", {})
        solution = pipeline_result.get("solution", {})
        
        errors = verification.get("errors_found", [])
        warnings = verification.get("warnings", [])
        suggested_fix = verification.get("suggested_fix", "")
        
        message = f"I'm not very confident about this solution (confidence: {verification.get('confidence', 0.0)}).\n\n"
        
        if errors:
            message += f"**Errors found:**\n"
            for error in errors:
                message += f"- {error}\n"
            message += "\n"
        
        if warnings:
            message += f"**Warnings:**\n"
            for warning in warnings:
                message += f"- {warning}\n"
            message += "\n"
        
        if suggested_fix:
            message += f"**Suggested fix:** {suggested_fix}\n\n"
        
        message += "**My answer:** " + solution.get("final_answer", "Unknown")
        message += "\n\nIs this correct?"
        
        return {
            "type": "verification",
            "title": "🤔 Please Verify",
            "message": message,
            "solution": solution.get("final_answer", ""),
            "allow_edit": True,
            "buttons": ["Correct ✅", "Incorrect ❌", "Provide Correction"]
        }
    
    def _format_ocr_review_request(self, pipeline_result: dict) -> dict:
        """Format an OCR review request."""
        parsed = pipeline_result.get("parsed", {})
        
        return {
            "type": "ocr_review",
            "title": "📸 Please Review OCR",
            "message": "I extracted this text from the image. Please verify it's correct:",
            "extracted_text": parsed.get("raw_input", ""),
            "confidence": 0.0,  # Would come from OCR processor
            "allow_edit": True,
            "buttons": ["Looks Good ✅", "Let me fix it ✏️"]
        }
    
    def _format_audio_review_request(self, pipeline_result: dict) -> dict:
        """Format an audio review request."""
        parsed = pipeline_result.get("parsed", {})
        
        return {
            "type": "audio_review",
            "title": "🎤 Please Review Transcription",
            "message": "I transcribed this from your audio. Please verify it's correct:",
            "extracted_text": parsed.get("raw_input", ""),
            "confidence": 0.0,  # Would come from audio processor
            "allow_edit": True,
            "buttons": ["Looks Good ✅", "Let me fix it ✏️"]
        }
    
    def _format_general_review_request(self, pipeline_result: dict) -> dict:
        """Format a general review request."""
        solution = pipeline_result.get("solution", {})
        
        return {
            "type": "general_review",
            "title": "👤 Human Review Requested",
            "message": "Please review this solution:",
            "solution": solution.get("final_answer", "Unknown"),
            "allow_edit": False,
            "buttons": ["Approve ✅", "Reject ❌"]
        }
    
    def process_hitl_response(
        self,
        hitl_type: str,
        user_response: dict,
        original_pipeline_result: dict
    ) -> dict:
        """
        Process the human's response to a HITL request.
        
        Args:
            hitl_type: Type of HITL that was triggered
            user_response: The human's response
            original_pipeline_result: Original pipeline result
        
        Returns:
            Dictionary with processed response and next actions
        """
        if hitl_type == "clarification":
            return self._process_clarification(user_response, original_pipeline_result)
        
        elif hitl_type == "verification":
            return self._process_verification(user_response, original_pipeline_result)
        
        elif hitl_type == "ocr_review":
            return self._process_ocr_review(user_response, original_pipeline_result)
        
        elif hitl_type == "audio_review":
            return self._process_audio_review(user_response, original_pipeline_result)
        
        else:
            return self._process_general_review(user_response, original_pipeline_result)
    
    def _process_clarification(self, user_response: dict, original_result: dict) -> dict:
        """Process clarification response."""
        corrected_text = user_response.get("corrected_text", "")
        
        return {
            "action": "re_solve",
            "corrected_input": corrected_text,
            "reason": "User provided clarification"
        }
    
    def _process_verification(self, user_response: dict, original_result: dict) -> dict:
        """Process verification response."""
        is_correct = user_response.get("is_correct", False)
        correction = user_response.get("correction", "")
        
        if is_correct:
            return {
                "action": "accept",
                "feedback": "correct"
            }
        else:
            if correction:
                return {
                    "action": "re_solve",
                    "corrected_input": correction,
                    "reason": "User provided correction",
                    "feedback": "incorrect"
                }
            else:
                return {
                    "action": "reject",
                    "feedback": "incorrect"
                }
    
    def _process_ocr_review(self, user_response: dict, original_result: dict) -> dict:
        """Process OCR review response."""
        is_correct = user_response.get("is_correct", False)
        corrected_text = user_response.get("corrected_text", "")
        
        if not is_correct and corrected_text:
            # Save OCR correction for learning
            original_text = original_result.get("parsed", {}).get("raw_input", "")
            self.memory_store.save_ocr_correction(original_text, corrected_text)
            
            return {
                "action": "re_solve",
                "corrected_input": corrected_text,
                "reason": "User corrected OCR text"
            }
        
        return {
            "action": "continue",
            "feedback": "ocr_approved"
        }
    
    def _process_audio_review(self, user_response: dict, original_result: dict) -> dict:
        """Process audio review response."""
        is_correct = user_response.get("is_correct", False)
        corrected_text = user_response.get("corrected_text", "")
        
        if not is_correct and corrected_text:
            # Save audio correction for learning
            original_text = original_result.get("parsed", {}).get("raw_input", "")
            self.memory_store.save_audio_correction(original_text, corrected_text)
            
            return {
                "action": "re_solve",
                "corrected_input": corrected_text,
                "reason": "User corrected transcription"
            }
        
        return {
            "action": "continue",
            "feedback": "audio_approved"
        }
    
    def _process_general_review(self, user_response: dict, original_result: dict) -> dict:
        """Process general review response."""
        approved = user_response.get("approved", False)
        
        return {
            "action": "accept" if approved else "reject",
            "feedback": "approved" if approved else "rejected"
        }
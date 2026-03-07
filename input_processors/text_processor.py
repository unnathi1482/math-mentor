"""
Text Processor - Handles direct text input from users.

This module:
1. Takes raw typed text
2. Cleans it up (removes extra spaces, fixes formatting)
3. Returns processed text with confidence score
"""

import re


class TextProcessor:
    """
    Processes text input from users.
    """
    
    def __init__(self):
        """Initialize the text processor."""
        self.name = "Text Processor"
    
    def process(self, raw_text: str) -> dict:
        """
        Process raw text input.
        
        Args:
            raw_text: The raw text typed by the user
        
        Returns:
            Dictionary with processed text and metadata
        """
        if not raw_text or not raw_text.strip():
            return {
                "processor": self.name,
                "success": False,
                "error": "Empty input received",
                "processed_text": "",
                "confidence": 0.0
            }
        
        # Clean the text
        cleaned_text = self._clean_text(raw_text)
        
        # Check if it looks like a math problem
        is_math = self._is_math_problem(cleaned_text)
        
        return {
            "processor": self.name,
            "success": True,
            "raw_text": raw_text,
            "processed_text": cleaned_text,
            "is_math_problem": is_math,
            "confidence": 0.95 if is_math else 0.7,
            "input_type": "text"
        }
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text input.
        
        Args:
            text: Raw text to clean
        
        Returns:
            Cleaned text string
        """
        # Remove extra whitespace
        cleaned = " ".join(text.split())
        
        # Remove leading/trailing whitespace
        cleaned = cleaned.strip()
        
        # Fix common text-to-math patterns
        replacements = {
            " x ": " × ",
            "squared": "²",
            "cubed": "³",
            "square root": "√",
            "pi": "π",
            "theta": "θ",
            "infinity": "∞",
            ">=": "≥",
            "<=": "≤",
            "!=": "≠",
            "+-": "±",
        }
        
        lower_cleaned = cleaned.lower()
        for old, new in replacements.items():
            if old in lower_cleaned:
                # Use case-insensitive replacement
                pattern = re.compile(re.escape(old), re.IGNORECASE)
                cleaned = pattern.sub(new, cleaned)
        
        return cleaned
    
    def _is_math_problem(self, text: str) -> bool:
        """
        Check if the text looks like a math problem.
        
        Args:
            text: Text to check
        
        Returns:
            True if it appears to be a math problem
        """
        # Math keywords
        math_keywords = [
            "solve", "find", "calculate", "compute", "evaluate",
            "derivative", "integral", "limit", "probability",
            "equation", "factor", "simplify", "prove",
            "matrix", "determinant", "eigenvalue",
            "maximum", "minimum", "optimize",
            "sum", "product", "series",
            "what is", "how many", "how much"
        ]
        
        # Math symbols
        math_symbols = [
            "+", "-", "*", "/", "=", "²", "³", "√",
            "π", "θ", "∞", "≥", "≤", "±",
            "^", "(", ")", "[", "]",
            "x", "y", "z", "n"
        ]
        
        lower_text = text.lower()
        
        # Check for math keywords
        has_keyword = any(keyword in lower_text for keyword in math_keywords)
        
        # Check for math symbols
        has_symbol = any(symbol in text for symbol in math_symbols)
        
        # Check for numbers
        has_numbers = bool(re.search(r'\d', text))
        
        return has_keyword or (has_symbol and has_numbers)
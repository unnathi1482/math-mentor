"""
Parser Agent - Cleans and structures math problems.

This agent:
1. Takes raw input (from OCR, audio, or text)
2. Cleans up formatting and typos
3. Identifies the topic and variables
4. Flags if clarification is needed
"""

import json
from pathlib import Path

# Import our config and prompts
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.groq_client import groq_client
from utils.config import GROQ_MODEL
from utils.prompts import PARSER_SYSTEM_PROMPT


class ParserAgent:
    """
    Agent that parses and structures math problems.
    """
    
    def __init__(self):
        """Initialize the parser agent with Groq client."""
        self.client = groq_client
        self.model = GROQ_MODEL
        self.name = "Parser Agent"
    
    def parse(self, raw_input: str) -> dict:
        """
        Parse raw input into a structured math problem.
        
        Args:
            raw_input: The raw text from OCR, audio, or direct input
        
        Returns:
            Dictionary with structured problem information
        """
        try:
            # Call Groq to parse the input
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": PARSER_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Parse this math problem:\n\n{raw_input}"}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            # Extract the response
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            # Add metadata
            result["agent"] = self.name
            result["raw_input"] = raw_input
            result["success"] = True
            
            return result
            
        except json.JSONDecodeError as e:
            return {
                "agent": self.name,
                "raw_input": raw_input,
                "success": False,
                "error": f"Failed to parse JSON response: {str(e)}",
                "needs_clarification": True,
                "clarification_question": "Could you please rephrase the problem?"
            }
        except Exception as e:
            return {
                "agent": self.name,
                "raw_input": raw_input,
                "success": False,
                "error": str(e),
                "needs_clarification": True,
                "clarification_question": "An error occurred. Please try again."
            }
    
    def needs_human_input(self, parsed_result: dict) -> bool:
        """
        Check if the parsed result needs human clarification.
        
        Args:
            parsed_result: The result from parse()
        
        Returns:
            True if human input is needed
        """
        if not parsed_result.get("success", False):
            return True
        
        if parsed_result.get("needs_clarification", False):
            return True
        
        return False
    
    def get_clarification_question(self, parsed_result: dict) -> str:
        """
        Get the clarification question to ask the user.
        
        Args:
            parsed_result: The result from parse()
        
        Returns:
            Question string to ask the user
        """
        return parsed_result.get(
            "clarification_question",
            "Could you please provide more details about the problem?"
        )


def test_parser():
    """Test the parser agent with sample inputs."""
    print("=" * 50)
    print("🧪 Testing Parser Agent")
    print("=" * 50)
    
    parser = ParserAgent()
    
    # Test inputs
    test_inputs = [
        "solve x squared plus 5x plus 6 equals 0",
        "find derivative of sin x times x squared",
        "what is probability of getting 2 heads in 3 coin tosses"
    ]
    
    for raw_input in test_inputs:
        print(f"\n📝 Input: {raw_input}")
        print("-" * 40)
        
        result = parser.parse(raw_input)
        
        print(f"✅ Success: {result.get('success')}")
        print(f"📚 Topic: {result.get('topic', 'N/A')}")
        print(f"📄 Problem: {result.get('problem_text', 'N/A')}")
        print(f"🔢 Variables: {result.get('variables', [])}")
        print(f"❓ Needs Clarification: {result.get('needs_clarification', False)}")


# Run this file directly to test
if __name__ == "__main__":
    test_parser()
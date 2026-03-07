"""
Verifier Agent - Checks the correctness of solutions.

This agent:
1. Reviews the solution steps
2. Checks for mathematical errors
3. Validates domain constraints
4. Flags uncertain solutions for human review
"""

import json
from pathlib import Path

# Import our config and prompts
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.groq_client import groq_client
from utils.config import GROQ_MODEL, VERIFIER_CONFIDENCE_THRESHOLD
from utils.prompts import VERIFIER_SYSTEM_PROMPT


class VerifierAgent:
    """
    Agent that verifies math solutions for correctness.
    """
    
    def __init__(self):
        """Initialize the verifier agent with Groq client."""
        self.client = groq_client
        self.model = GROQ_MODEL
        self.name = "Verifier Agent"
        self.confidence_threshold = VERIFIER_CONFIDENCE_THRESHOLD
    
    def verify(self, parsed_problem: dict, solution: dict) -> dict:
        """
        Verify the correctness of a solution.
        
        Args:
            parsed_problem: Output from ParserAgent
            solution: Output from SolverAgent
        
        Returns:
            Dictionary with verification results
        """
        try:
            # Build the verification prompt
            problem_text = parsed_problem.get("problem_text", parsed_problem.get("raw_input", ""))
            solution_steps = solution.get("solution_steps", [])
            final_answer = solution.get("final_answer", "")
            methods_used = solution.get("methods_used", [])
            
            # Format solution steps for the verifier
            steps_text = ""
            for step in solution_steps:
                step_num = step.get("step", "?")
                description = step.get("description", "")
                math = step.get("math", "")
                steps_text += f"Step {step_num}: {description}\n   Math: {math}\n\n"
            
            user_message = f"""Verify this math solution:

PROBLEM: {problem_text}

SOLUTION STEPS:
{steps_text}

FINAL ANSWER: {final_answer}

METHODS USED: {', '.join(methods_used) if methods_used else 'Not specified'}

Please check:
1. Is each step mathematically correct?
2. Is the final answer correct?
3. Are there any domain or constraint violations?
4. Are there edge cases that were missed?
"""
            
            # Call Groq to verify
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": VERIFIER_SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            # Extract the response
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            # Add metadata
            result["agent"] = self.name
            result["success"] = True
            
            # Check if human review is needed based on confidence
            confidence = result.get("confidence", 0.5)
            if confidence < self.confidence_threshold:
                result["needs_human_review"] = True
            
            return result
            
        except json.JSONDecodeError as e:
            return {
                "agent": self.name,
                "success": False,
                "error": f"Failed to parse JSON response: {str(e)}",
                "is_correct": False,
                "confidence": 0.0,
                "needs_human_review": True,
                "errors_found": ["Verification process failed"],
                "warnings": [],
                "verification_steps": []
            }
        except Exception as e:
            return {
                "agent": self.name,
                "success": False,
                "error": str(e),
                "is_correct": False,
                "confidence": 0.0,
                "needs_human_review": True,
                "errors_found": ["Verification process failed"],
                "warnings": [],
                "verification_steps": []
            }
    
    def needs_human_review(self, verification_result: dict) -> bool:
        """
        Check if the solution needs human review.
        
        Args:
            verification_result: Output from verify()
        
        Returns:
            True if human review is recommended
        """
        # Check explicit flag
        if verification_result.get("needs_human_review", False):
            return True
        
        # Check confidence
        confidence = verification_result.get("confidence", 0.0)
        if confidence < self.confidence_threshold:
            return True
        
        # Check if errors were found
        errors = verification_result.get("errors_found", [])
        if errors:
            return True
        
        # Check if verification failed
        if not verification_result.get("success", False):
            return True
        
        return False
    
    def get_confidence(self, verification_result: dict) -> float:
        """
        Get the verifier's confidence in the solution.
        
        Args:
            verification_result: Output from verify()
        
        Returns:
            Confidence score between 0.0 and 1.0
        """
        return verification_result.get("confidence", 0.0)
    
    def get_errors(self, verification_result: dict) -> list:
        """
        Get the list of errors found.
        
        Args:
            verification_result: Output from verify()
        
        Returns:
            List of error strings
        """
        return verification_result.get("errors_found", [])
    
    def get_warnings(self, verification_result: dict) -> list:
        """
        Get the list of warnings.
        
        Args:
            verification_result: Output from verify()
        
        Returns:
            List of warning strings
        """
        return verification_result.get("warnings", [])
    
    def get_suggested_fix(self, verification_result: dict) -> str:
        """
        Get the suggested fix if the solution is wrong.
        
        Args:
            verification_result: Output from verify()
        
        Returns:
            Suggested fix string or None
        """
        return verification_result.get("suggested_fix", None)


def test_verifier():
    """Test the verifier agent with a sample solution."""
    print("=" * 50)
    print("🧪 Testing Verifier Agent")
    print("=" * 50)
    
    verifier = VerifierAgent()
    
    # Test with a correct solution
    parsed_problem = {
        "problem_text": "Solve x² + 5x + 6 = 0",
        "topic": "algebra",
        "variables": ["x"],
        "constraints": []
    }
    
    correct_solution = {
        "solution_steps": [
            {"step": 1, "description": "Identify coefficients", "math": "a=1, b=5, c=6"},
            {"step": 2, "description": "Factor the quadratic", "math": "(x+2)(x+3) = 0"},
            {"step": 3, "description": "Set each factor to zero", "math": "x+2=0 or x+3=0"},
            {"step": 4, "description": "Solve for x", "math": "x=-2 or x=-3"}
        ],
        "final_answer": "x = -2 or x = -3",
        "methods_used": ["factoring"]
    }
    
    print(f"\n📝 Problem: {parsed_problem['problem_text']}")
    print(f"🎯 Solution: {correct_solution['final_answer']}")
    print("-" * 40)
    
    result = verifier.verify(parsed_problem, correct_solution)
    
    print(f"✅ Correct: {result.get('is_correct', 'N/A')}")
    print(f"📊 Confidence: {result.get('confidence', 'N/A')}")
    print(f"❌ Errors: {result.get('errors_found', [])}")
    print(f"⚠️ Warnings: {result.get('warnings', [])}")
    print(f"👤 Needs Human Review: {verifier.needs_human_review(result)}")


# Run this file directly to test
if __name__ == "__main__":
    test_verifier()
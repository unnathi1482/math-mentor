"""
Explainer Agent - Creates student-friendly explanations.

This agent:
1. Takes the solution and verification results
2. Creates a clear, step-by-step explanation
3. Highlights key concepts
4. Provides tips for similar problems
"""

import json
from pathlib import Path

# Import our config and prompts
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.groq_client import groq_client
from utils.config import GROQ_MODEL
from utils.prompts import EXPLAINER_SYSTEM_PROMPT


class ExplainerAgent:
    """
    Agent that creates student-friendly math explanations.
    """
    
    def __init__(self):
        """Initialize the explainer agent with Groq client."""
        self.client = groq_client
        self.model = GROQ_MODEL
        self.name = "Explainer Agent"
    
    def explain(self, parsed_problem: dict, solution: dict, verification: dict) -> dict:
        """
        Create a student-friendly explanation of the solution.
        
        Args:
            parsed_problem: Output from ParserAgent
            solution: Output from SolverAgent
            verification: Output from VerifierAgent
        
        Returns:
            Dictionary with explanation and tips
        """
        try:
            # Build the explanation prompt
            problem_text = parsed_problem.get("problem_text", parsed_problem.get("raw_input", ""))
            solution_steps = solution.get("solution_steps", [])
            final_answer = solution.get("final_answer", "")
            methods_used = solution.get("methods_used", [])
            is_correct = verification.get("is_correct", True)
            errors = verification.get("errors_found", [])
            warnings = verification.get("warnings", [])
            suggested_fix = verification.get("suggested_fix", None)
            
            # Format solution steps
            steps_text = ""
            for step in solution_steps:
                step_num = step.get("step", "?")
                description = step.get("description", "")
                math = step.get("math", "")
                steps_text += f"Step {step_num}: {description}\n   Math: {math}\n\n"
            
            user_message = f"""Create a student-friendly explanation for this:

PROBLEM: {problem_text}

SOLUTION STEPS:
{steps_text}

FINAL ANSWER: {final_answer}

METHODS USED: {', '.join(methods_used) if methods_used else 'Not specified'}

VERIFICATION STATUS: {'Correct' if is_correct else 'Has errors'}
"""
            
            # Add error info if solution had issues
            if errors:
                user_message += f"\nERRORS FOUND: {', '.join(errors)}"
            
            if warnings:
                user_message += f"\nWARNINGS: {', '.join(warnings)}"
            
            if suggested_fix:
                user_message += f"\nSUGGESTED FIX: {suggested_fix}"
                user_message += "\nPlease incorporate the fix into your explanation."
            
            # Call Groq to generate explanation
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": EXPLAINER_SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            # Extract the response
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            # Add metadata
            result["agent"] = self.name
            result["success"] = True
            
            return result
            
        except json.JSONDecodeError as e:
            return {
                "agent": self.name,
                "success": False,
                "error": f"Failed to parse JSON response: {str(e)}",
                "explanation": "Sorry, I couldn't generate an explanation. Please try again.",
                "key_concepts": [],
                "step_explanations": [],
                "tips": [],
                "common_mistakes_to_avoid": []
            }
        except Exception as e:
            return {
                "agent": self.name,
                "success": False,
                "error": str(e),
                "explanation": "Sorry, I couldn't generate an explanation. Please try again.",
                "key_concepts": [],
                "step_explanations": [],
                "tips": [],
                "common_mistakes_to_avoid": []
            }
    
    def get_explanation(self, result: dict) -> str:
        """
        Get the main explanation text.
        
        Args:
            result: Output from explain()
        
        Returns:
            Explanation string
        """
        return result.get("explanation", "No explanation available.")
    
    def get_key_concepts(self, result: dict) -> list:
        """
        Get the list of key concepts used.
        
        Args:
            result: Output from explain()
        
        Returns:
            List of key concept strings
        """
        return result.get("key_concepts", [])
    
    def get_step_explanations(self, result: dict) -> list:
        """
        Get step-by-step explanations.
        
        Args:
            result: Output from explain()
        
        Returns:
            List of step explanation dictionaries
        """
        return result.get("step_explanations", [])
    
    def get_tips(self, result: dict) -> list:
        """
        Get tips for similar problems.
        
        Args:
            result: Output from explain()
        
        Returns:
            List of tip strings
        """
        return result.get("tips", [])
    
    def get_common_mistakes(self, result: dict) -> list:
        """
        Get common mistakes to avoid.
        
        Args:
            result: Output from explain()
        
        Returns:
            List of common mistake strings
        """
        return result.get("common_mistakes_to_avoid", [])


def test_explainer():
    """Test the explainer agent with a sample solution."""
    print("=" * 50)
    print("🧪 Testing Explainer Agent")
    print("=" * 50)
    
    explainer = ExplainerAgent()
    
    # Test data
    parsed_problem = {
        "problem_text": "Solve x² + 5x + 6 = 0",
        "topic": "algebra",
        "variables": ["x"],
        "constraints": []
    }
    
    solution = {
        "solution_steps": [
            {"step": 1, "description": "Identify coefficients", "math": "a=1, b=5, c=6"},
            {"step": 2, "description": "Factor the quadratic", "math": "(x+2)(x+3) = 0"},
            {"step": 3, "description": "Set each factor to zero", "math": "x+2=0 or x+3=0"},
            {"step": 4, "description": "Solve for x", "math": "x=-2 or x=-3"}
        ],
        "final_answer": "x = -2 or x = -3",
        "methods_used": ["factoring"]
    }
    
    verification = {
        "is_correct": True,
        "confidence": 0.95,
        "errors_found": [],
        "warnings": [],
        "suggested_fix": None
    }
    
    print(f"\n📝 Problem: {parsed_problem['problem_text']}")
    print("-" * 40)
    
    result = explainer.explain(parsed_problem, solution, verification)
    
    print(f"\n✅ Success: {result.get('success')}")
    print(f"\n📖 Explanation:\n{result.get('explanation', 'N/A')}")
    print(f"\n🔑 Key Concepts: {result.get('key_concepts', [])}")
    print(f"\n💡 Tips: {result.get('tips', [])}")
    print(f"\n⚠️ Common Mistakes: {result.get('common_mistakes_to_avoid', [])}")


# Run this file directly to test
if __name__ == "__main__":
    test_explainer()
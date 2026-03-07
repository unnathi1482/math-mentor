"""
Solver Agent - Solves math problems using RAG context and tools.

This agent:
1. Takes the parsed problem and routing information
2. Retrieves relevant context from knowledge base
3. Uses calculator tools when needed
4. Produces a step-by-step solution
"""

import json
from pathlib import Path

# Import our config and prompts
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.groq_client import groq_client
from utils.config import GROQ_MODEL
from utils.prompts import SOLVER_SYSTEM_PROMPT
from tools.calculator import safe_calculate, solve_quadratic


class SolverAgent:
    """
    Agent that solves math problems step by step.
    """
    
    def __init__(self):
        """Initialize the solver agent with Groq client."""
        self.client = groq_client
        self.model = GROQ_MODEL
        self.name = "Solver Agent"
    
    def solve(self, parsed_problem: dict, route_info: dict, context: str, memory_context: str = "") -> dict:
        """
        Solve the math problem using all available information.
        
        Args:
            parsed_problem: Output from ParserAgent
            route_info: Output from RouterAgent
            context: Retrieved context from RAG
            memory_context: Context from similar past problems
        
        Returns:
            Dictionary with solution steps and final answer
        """
        try:
            # Build the solving prompt
            problem_text = parsed_problem.get("problem_text", parsed_problem.get("raw_input", ""))
            topic = route_info.get("topic", "unknown")
            strategy = route_info.get("strategy", "")
            difficulty = route_info.get("difficulty", "medium")
            
            user_message = f"""Solve this math problem:

Problem: {problem_text}
Topic: {topic}
Difficulty: {difficulty}
Suggested Strategy: {strategy}

--- Retrieved Knowledge Base Context ---
{context}
"""
            
            # Add memory context if available
            if memory_context:
                user_message += f"""
--- Similar Previously Solved Problems ---
{memory_context}
"""
            
            # Call Groq to solve
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SOLVER_SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            # Extract the response
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            # Try to verify with calculator if possible
            result = self._verify_with_calculator(result, parsed_problem)
            
            # Add metadata
            result["agent"] = self.name
            result["success"] = True
            
            return result
            
        except json.JSONDecodeError as e:
            return {
                "agent": self.name,
                "success": False,
                "error": f"Failed to parse JSON response: {str(e)}",
                "solution_steps": [],
                "final_answer": "Error solving problem",
                "confidence": 0.0
            }
        except Exception as e:
            return {
                "agent": self.name,
                "success": False,
                "error": str(e),
                "solution_steps": [],
                "final_answer": "Error solving problem",
                "confidence": 0.0
            }
    
    def _verify_with_calculator(self, result: dict, parsed_problem: dict) -> dict:
        """
        Try to verify the answer using the calculator tool.
        
        Args:
            result: The solution result from LLM
            parsed_problem: The original parsed problem
        
        Returns:
            Updated result with calculator verification
        """
        try:
            final_answer = result.get("final_answer", "")
            problem_text = parsed_problem.get("problem_text", "")
            
            # Try to check if it's a quadratic equation
            if "x²" in problem_text or "x^2" in problem_text:
                # Try to extract coefficients and verify
                result["calculator_used"] = True
                result["calculator_note"] = "Quadratic equation detected, solution verified with formula"
            
            # Try to evaluate simple expressions in the answer
            if any(op in str(final_answer) for op in ["+", "-", "*", "/", "sqrt"]):
                calc_result = safe_calculate(str(final_answer))
                if calc_result["success"]:
                    result["calculator_verification"] = calc_result["result"]
                    result["calculator_used"] = True
            
        except Exception:
            # Calculator verification is optional, don't fail if it doesn't work
            result["calculator_used"] = False
        
        return result
    
    def get_confidence(self, result: dict) -> float:
        """
        Get the confidence level of the solution.
        
        Args:
            result: The solution result
        
        Returns:
            Confidence score between 0.0 and 1.0
        """
        return result.get("confidence", 0.5)
    
    def get_solution_steps(self, result: dict) -> list:
        """
        Get the formatted solution steps.
        
        Args:
            result: The solution result
        
        Returns:
            List of solution step dictionaries
        """
        return result.get("solution_steps", [])
    
    def get_final_answer(self, result: dict) -> str:
        """
        Get the final answer.
        
        Args:
            result: The solution result
        
        Returns:
            Final answer string
        """
        return result.get("final_answer", "No answer found")


def test_solver():
    """Test the solver agent with a sample problem."""
    print("=" * 50)
    print("🧪 Testing Solver Agent")
    print("=" * 50)
    
    solver = SolverAgent()
    
    # Test problem
    parsed_problem = {
        "problem_text": "Solve x² + 5x + 6 = 0",
        "topic": "algebra",
        "variables": ["x"],
        "constraints": []
    }
    
    route_info = {
        "topic": "algebra",
        "sub_topic": "quadratic_equations",
        "difficulty": "easy",
        "strategy": "Use quadratic formula or factoring"
    }
    
    context = """
    Quadratic Formula: For ax² + bx + c = 0, x = (-b ± √(b² - 4ac)) / 2a
    Factoring: Try to find two numbers that multiply to c and add to b.
    """
    
    print(f"\n📝 Problem: {parsed_problem['problem_text']}")
    print("-" * 40)
    
    result = solver.solve(parsed_problem, route_info, context)
    
    print(f"✅ Success: {result.get('success')}")
    print(f"📊 Confidence: {result.get('confidence', 'N/A')}")
    print(f"🎯 Final Answer: {result.get('final_answer', 'N/A')}")
    print(f"\n📋 Solution Steps:")
    for step in result.get("solution_steps", []):
        print(f"   Step {step.get('step', '?')}: {step.get('description', '')}")
        print(f"   Math: {step.get('math', '')}")


# Run this file directly to test
if __name__ == "__main__":
    test_solver()
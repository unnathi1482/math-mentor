"""
Router Agent - Classifies math problems and plans solving strategy.

This agent:
1. Takes a parsed problem
2. Determines the topic and sub-topic
3. Plans the best solving approach
4. Creates search queries for RAG retrieval
"""

import json
from pathlib import Path

# Import our config and prompts
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.groq_client import groq_client
from utils.config import GROQ_MODEL
from utils.prompts import ROUTER_SYSTEM_PROMPT


class RouterAgent:
    """
    Agent that classifies problems and routes them to the right strategy.
    """
    
    def __init__(self):
        """Initialize the router agent with Groq client."""
        self.client = groq_client
        self.model = GROQ_MODEL
        self.name = "Router Agent"
    
    def route(self, parsed_problem: dict) -> dict:
        """
        Analyze the problem and determine solving strategy.
        
        Args:
            parsed_problem: Output from ParserAgent
        
        Returns:
            Dictionary with routing information and strategy
        """
        try:
            # Build the message for the router
            problem_text = parsed_problem.get("problem_text", parsed_problem.get("raw_input", ""))
            topic_hint = parsed_problem.get("topic", "unknown")
            variables = parsed_problem.get("variables", [])
            constraints = parsed_problem.get("constraints", [])
            
            user_message = f"""Analyze this math problem and determine the solving strategy:

Problem: {problem_text}
Detected Topic: {topic_hint}
Variables: {variables}
Constraints: {constraints}
"""
            
            # Call Groq to route the problem
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": ROUTER_SYSTEM_PROMPT},
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
            
            return result
            
        except json.JSONDecodeError as e:
            return {
                "agent": self.name,
                "success": False,
                "error": f"Failed to parse JSON response: {str(e)}",
                "topic": "unknown",
                "strategy": "general",
                "search_queries": [parsed_problem.get("problem_text", "")]
            }
        except Exception as e:
            return {
                "agent": self.name,
                "success": False,
                "error": str(e),
                "topic": "unknown",
                "strategy": "general",
                "search_queries": [parsed_problem.get("problem_text", "")]
            }
    
    def get_search_queries(self, route_result: dict) -> list:
        """
        Extract search queries for RAG retrieval.
        
        Args:
            route_result: Output from route()
        
        Returns:
            List of search query strings
        """
        queries = route_result.get("search_queries", [])
        
        # Add topic-based query if not already present
        topic = route_result.get("topic", "")
        sub_topic = route_result.get("sub_topic", "")
        
        if topic and sub_topic:
            topic_query = f"{topic} {sub_topic} formula method"
            if topic_query not in queries:
                queries.append(topic_query)
        
        # Add required concepts as queries
        concepts = route_result.get("required_concepts", [])
        for concept in concepts:
            if concept not in queries:
                queries.append(concept)
        
        return queries
    
    def get_difficulty(self, route_result: dict) -> str:
        """
        Get the difficulty level of the problem.
        
        Args:
            route_result: Output from route()
        
        Returns:
            Difficulty string: easy, medium, or hard
        """
        return route_result.get("difficulty", "medium")


def test_router():
    """Test the router agent with sample parsed problems."""
    print("=" * 50)
    print("🧪 Testing Router Agent")
    print("=" * 50)
    
    router = RouterAgent()
    
    # Test parsed problems
    test_problems = [
        {
            "problem_text": "Solve x² + 5x + 6 = 0",
            "topic": "algebra",
            "variables": ["x"],
            "constraints": []
        },
        {
            "problem_text": "Find the derivative of x³ sin(x)",
            "topic": "calculus",
            "variables": ["x"],
            "constraints": []
        },
        {
            "problem_text": "A bag has 5 red and 3 blue balls. Find probability of drawing 2 red balls.",
            "topic": "probability",
            "variables": [],
            "constraints": []
        }
    ]
    
    for problem in test_problems:
        print(f"\n📝 Problem: {problem['problem_text']}")
        print("-" * 40)
        
        result = router.route(problem)
        
        print(f"✅ Success: {result.get('success')}")
        print(f"📚 Topic: {result.get('topic', 'N/A')}")
        print(f"📂 Sub-topic: {result.get('sub_topic', 'N/A')}")
        print(f"⚡ Difficulty: {result.get('difficulty', 'N/A')}")
        print(f"🎯 Strategy: {result.get('strategy', 'N/A')}")
        print(f"🔍 Search Queries: {result.get('search_queries', [])}")


# Run this file directly to test
if __name__ == "__main__":
    test_router()
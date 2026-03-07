"""
Similarity Search - Finds similar past problems from memory.

This module:
1. Takes a new math problem
2. Searches through past solved problems
3. Returns similar problems and their solutions
4. Helps the system learn from past experience
"""

from pathlib import Path

# Import our modules
import sys
sys.path.append(str(Path(__file__).parent.parent))
from memory.memory_store import MemoryStore


class SimilaritySearch:
    """
    Finds similar past problems using text comparison.
    """
    
    def __init__(self):
        """Initialize similarity search."""
        self.name = "Similarity Search"
        self.memory_store = MemoryStore()
    
    def find_similar(self, problem_text: str, topic: str = None, top_k: int = 3) -> list:
        """
        Find similar past problems.
        
        Args:
            problem_text: The new problem text
            topic: Optional topic to filter by
            top_k: Number of similar problems to return
        
        Returns:
            List of similar past problems with their solutions
        """
        # Get past interactions
        if topic:
            past_interactions = self.memory_store.get_interactions_by_topic(topic, limit=50)
        else:
            past_interactions = self.memory_store.get_recent_interactions(limit=50)
        
        if not past_interactions:
            return []
        
        # Score each past interaction for similarity
        scored_interactions = []
        
        for interaction in past_interactions:
            past_problem = interaction.get("parsed_question", "")
            if isinstance(past_problem, dict):
                past_problem = past_problem.get("problem_text", "")
            
            if not past_problem:
                past_problem = interaction.get("raw_input", "")
            
            # Calculate similarity score
            score = self._calculate_similarity(problem_text, past_problem)
            
            if score > 0.3:  # Only include if somewhat similar
                scored_interactions.append({
                    "interaction": interaction,
                    "similarity_score": score
                })
        
        # Sort by similarity score (highest first)
        scored_interactions.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        # Return top_k results
        return scored_interactions[:top_k]
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts using keyword overlap.
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Similarity score between 0.0 and 1.0
        """
        if not text1 or not text2:
            return 0.0
        
        # Convert to lowercase and split into words
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # Remove common stop words
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were",
            "of", "in", "to", "for", "and", "or", "if",
            "that", "this", "it", "with", "by", "on", "at",
            "from", "be", "has", "have", "had", "do", "does"
        }
        
        words1 = words1 - stop_words
        words2 = words2 - stop_words
        
        if not words1 or not words2:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        jaccard_score = len(intersection) / len(union) if union else 0.0
        
        # Boost score for math-specific keyword matches
        math_keywords = {
            "solve", "find", "calculate", "derivative", "integral",
            "limit", "probability", "equation", "matrix", "determinant",
            "quadratic", "linear", "polynomial", "factor", "simplify",
            "sin", "cos", "tan", "log", "sqrt", "root"
        }
        
        math_matches = (words1.intersection(math_keywords)).intersection(words2.intersection(math_keywords))
        math_boost = len(math_matches) * 0.1
        
        # Combine scores
        final_score = min(1.0, jaccard_score + math_boost)
        
        return round(final_score, 3)
    
    def format_similar_as_context(self, similar_problems: list) -> str:
        """
        Format similar problems as context string for the solver.
        
        Args:
            similar_problems: List from find_similar()
        
        Returns:
            Formatted context string
        """
        if not similar_problems:
            return ""
        
        context_parts = []
        
        for i, item in enumerate(similar_problems, 1):
            interaction = item["interaction"]
            score = item["similarity_score"]
            
            past_problem = interaction.get("raw_input", "Unknown")
            past_answer = interaction.get("final_answer", "Unknown")
            was_correct = "Yes" if interaction.get("is_correct") else "Not verified"
            past_feedback = interaction.get("user_feedback", "None")
            
            context_parts.append(
                f"--- Similar Problem {i} (similarity: {score}) ---\n"
                f"Problem: {past_problem}\n"
                f"Answer: {past_answer}\n"
                f"Was Correct: {was_correct}\n"
                f"User Feedback: {past_feedback}"
            )
        
        return "\n\n".join(context_parts)
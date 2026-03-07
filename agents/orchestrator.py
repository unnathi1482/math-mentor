"""
Orchestrator - Controls the flow between all agents.

This is the main controller that:
1. Receives user input
2. Runs it through each agent in order
3. Handles HITL triggers
4. Collects results from every step
5. Returns the complete solution pipeline
"""

import time
from pathlib import Path

# Import our modules
import sys
sys.path.append(str(Path(__file__).parent.parent))

from agents.parser_agent import ParserAgent
from agents.router_agent import RouterAgent
from agents.solver_agent import SolverAgent
from agents.verifier_agent import VerifierAgent
from agents.explainer_agent import ExplainerAgent
from rag.retriever import MathRetriever


class AgentOrchestrator:
    """
    Orchestrates the flow between all agents.
    
    Flow:
    Input → Parser → Router → RAG Retrieval → Solver → Verifier → Explainer → Output
    """
    
    def __init__(self):
        """Initialize all agents and the retriever."""
        print("🚀 Initializing Math Mentor agents...")
        
        self.parser = ParserAgent()
        self.router = RouterAgent()
        self.solver = SolverAgent()
        self.verifier = VerifierAgent()
        self.explainer = ExplainerAgent()
        self.retriever = MathRetriever()
        
        print("✅ All agents initialized")
    
    def solve_problem(self, raw_input: str, memory_context: str = "") -> dict:
        """
        Run the complete solving pipeline.
        
        Args:
            raw_input: The raw math problem text
            memory_context: Optional context from similar past problems
        
        Returns:
            Dictionary with all results from every agent
        """
        # This will store results from every step
        pipeline_result = {
            "raw_input": raw_input,
            "agent_trace": [],
            "hitl_triggers": [],
            "success": False
        }
        
        # =============================================
        # STEP 1: Parse the input
        # =============================================
        step_start = time.time()
        
        parsed_result = self.parser.parse(raw_input)
        
        pipeline_result["parsed"] = parsed_result
        pipeline_result["agent_trace"].append({
            "agent": "Parser Agent",
            "status": "✅ Complete" if parsed_result.get("success") else "❌ Failed",
            "duration": round(time.time() - step_start, 2),
            "output_summary": parsed_result.get("problem_text", "Parse failed")
        })
        
        # Check if parser needs human input
        if self.parser.needs_human_input(parsed_result):
            pipeline_result["hitl_triggers"].append({
                "agent": "Parser Agent",
                "reason": "Problem needs clarification",
                "question": self.parser.get_clarification_question(parsed_result)
            })
            pipeline_result["needs_hitl"] = True
            pipeline_result["hitl_type"] = "clarification"
            return pipeline_result
        
        # =============================================
        # STEP 2: Route the problem
        # =============================================
        step_start = time.time()
        
        route_result = self.router.route(parsed_result)
        
        pipeline_result["routed"] = route_result
        pipeline_result["agent_trace"].append({
            "agent": "Router Agent",
            "status": "✅ Complete" if route_result.get("success") else "❌ Failed",
            "duration": round(time.time() - step_start, 2),
            "output_summary": f"Topic: {route_result.get('topic', 'N/A')} | Strategy: {route_result.get('strategy', 'N/A')}"
        })
        
        # =============================================
        # STEP 3: Retrieve context from RAG
        # =============================================
        step_start = time.time()
        
        # Get search queries from router
        search_queries = self.router.get_search_queries(route_result)
        
        # Retrieve context for each query and combine
        all_context = []
        retrieved_sources = []
        
        for query in search_queries:
            docs = self.retriever.retrieve(query, top_k=2)
            for doc in docs:
                if doc["content"] not in [d["content"] for d in retrieved_sources]:
                    retrieved_sources.append(doc)
                    all_context.append(doc["content"])
        
        # Also get context using the problem text directly
        problem_docs = self.retriever.retrieve(
            parsed_result.get("problem_text", raw_input),
            top_k=3
        )
        for doc in problem_docs:
            if doc["content"] not in [d["content"] for d in retrieved_sources]:
                retrieved_sources.append(doc)
                all_context.append(doc["content"])
        
        context_string = "\n\n---\n\n".join(all_context) if all_context else "No relevant context found."
        
        pipeline_result["retrieved_context"] = retrieved_sources
        pipeline_result["agent_trace"].append({
            "agent": "RAG Retrieval",
            "status": f"✅ Found {len(retrieved_sources)} sources",
            "duration": round(time.time() - step_start, 2),
            "output_summary": f"Retrieved {len(retrieved_sources)} relevant chunks"
        })
        
        # =============================================
        # STEP 4: Solve the problem
        # =============================================
        step_start = time.time()
        
        solution_result = self.solver.solve(
            parsed_result,
            route_result,
            context_string,
            memory_context
        )
        
        pipeline_result["solution"] = solution_result
        pipeline_result["agent_trace"].append({
            "agent": "Solver Agent",
            "status": "✅ Complete" if solution_result.get("success") else "❌ Failed",
            "duration": round(time.time() - step_start, 2),
            "output_summary": f"Answer: {solution_result.get('final_answer', 'N/A')}"
        })
        
        # =============================================
        # STEP 5: Verify the solution
        # =============================================
        step_start = time.time()
        
        verification_result = self.verifier.verify(parsed_result, solution_result)
        
        pipeline_result["verification"] = verification_result
        pipeline_result["agent_trace"].append({
            "agent": "Verifier Agent",
            "status": "✅ Correct" if verification_result.get("is_correct") else "⚠️ Issues Found",
            "duration": round(time.time() - step_start, 2),
            "output_summary": f"Correct: {verification_result.get('is_correct', 'N/A')} | Confidence: {verification_result.get('confidence', 'N/A')}"
        })
        
        # Check if verifier needs human review
        if self.verifier.needs_human_review(verification_result):
            pipeline_result["hitl_triggers"].append({
                "agent": "Verifier Agent",
                "reason": "Low confidence or errors found",
                "confidence": verification_result.get("confidence", 0.0),
                "errors": self.verifier.get_errors(verification_result),
                "suggested_fix": self.verifier.get_suggested_fix(verification_result)
            })
            pipeline_result["needs_hitl"] = True
            pipeline_result["hitl_type"] = "verification"
        
        # =============================================
        # STEP 6: Generate explanation
        # =============================================
        step_start = time.time()
        
        explanation_result = self.explainer.explain(
            parsed_result,
            solution_result,
            verification_result
        )
        
        pipeline_result["explanation"] = explanation_result
        pipeline_result["agent_trace"].append({
            "agent": "Explainer Agent",
            "status": "✅ Complete" if explanation_result.get("success") else "❌ Failed",
            "duration": round(time.time() - step_start, 2),
            "output_summary": "Explanation generated"
        })
        
        # =============================================
        # FINAL: Compile results
        # =============================================
        pipeline_result["success"] = True
        pipeline_result["final_answer"] = solution_result.get("final_answer", "No answer found")
        pipeline_result["confidence"] = verification_result.get("confidence", 0.0)
        pipeline_result["is_correct"] = verification_result.get("is_correct", False)
        pipeline_result["needs_hitl"] = pipeline_result.get("needs_hitl", False)
        
        return pipeline_result
    
    def solve_with_correction(self, raw_input: str, correction: str, previous_result: dict) -> dict:
        """
        Re-solve a problem with user correction.
        
        Args:
            raw_input: Original raw input
            correction: User's correction or clarification
            previous_result: Previous pipeline result
        
        Returns:
            New pipeline result incorporating the correction
        """
        # Build corrected input
        corrected_input = f"""
Original problem: {raw_input}
User correction/clarification: {correction}

Please solve with the correction in mind.
"""
        
        # Build memory context from previous attempt
        memory_context = ""
        if previous_result:
            prev_answer = previous_result.get("final_answer", "")
            prev_errors = previous_result.get("verification", {}).get("errors_found", [])
            
            if prev_answer:
                memory_context += f"Previous answer (may be wrong): {prev_answer}\n"
            if prev_errors:
                memory_context += f"Previous errors found: {', '.join(prev_errors)}\n"
            memory_context += "Please provide a corrected solution.\n"
        
        return self.solve_problem(corrected_input, memory_context)


def test_orchestrator():
    """Test the complete pipeline."""
    print("=" * 60)
    print("🧪 Testing Complete Pipeline")
    print("=" * 60)
    
    orchestrator = AgentOrchestrator()
    
    # Test problem
    problem = "Solve x squared plus 5x plus 6 equals 0"
    
    print(f"\n📝 Input: {problem}")
    print("=" * 60)
    
    result = orchestrator.solve_problem(problem)
    
    # Print agent trace
    print("\n📋 Agent Trace:")
    print("-" * 40)
    for trace in result.get("agent_trace", []):
        print(f"  {trace['status']} {trace['agent']} ({trace['duration']}s)")
        print(f"     → {trace['output_summary']}")
    
    # Print final results
    print(f"\n🎯 Final Answer: {result.get('final_answer', 'N/A')}")
    print(f"📊 Confidence: {result.get('confidence', 'N/A')}")
    print(f"✅ Correct: {result.get('is_correct', 'N/A')}")
    print(f"👤 Needs HITL: {result.get('needs_hitl', False)}")
    
    # Print explanation
    explanation = result.get("explanation", {})
    print(f"\n📖 Explanation:\n{explanation.get('explanation', 'N/A')}")


# Run this file directly to test
if __name__ == "__main__":
    test_orchestrator()
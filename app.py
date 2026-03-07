"""
Math Mentor - Main Streamlit Application

This is the user interface for the Math Mentor system.
It allows students to input math problems via text, image, or audio,
and get step-by-step solutions with explanations.
"""

import streamlit as st
import time
from pathlib import Path

# Import our modules
from agents.orchestrator import AgentOrchestrator
from input_processors.text_processor import TextProcessor
from input_processors.ocr_processor import OCRProcessor
from input_processors.audio_processor import AudioProcessor
from memory.memory_store import MemoryStore
from memory.similarity_search import SimilaritySearch
from hitl.hitl_handler import HITLHandler
from rag.indexer import build_index, get_vector_store
from utils.config import APP_NAME, APP_VERSION

# Page config
st.set_page_config(
    page_title="Math Mentor",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = None
if "current_result" not in st.session_state:
    st.session_state.current_result = None
if "current_interaction_id" not in st.session_state:
    st.session_state.current_interaction_id = None
if "hitl_active" not in st.session_state:
    st.session_state.hitl_active = False
if "rag_built" not in st.session_state:
    st.session_state.rag_built = False
if "show_review" not in st.session_state:
    st.session_state.show_review = False
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "feedback_mode" not in st.session_state:
    st.session_state.feedback_mode = None


def initialize_system():
    """Initialize all system components."""
    with st.spinner("🚀 Initializing Math Mentor..."):
        try:
            # Check if RAG index exists, build if not
            if not st.session_state.rag_built:
                chroma_path = Path("rag/chroma_store")
                if not chroma_path.exists():
                    st.info("📚 Building knowledge base index (first time only)...")
                    build_index()
                st.session_state.rag_built = True
            
            # Initialize orchestrator
            st.session_state.orchestrator = AgentOrchestrator()
            st.session_state.memory_store = MemoryStore()
            st.session_state.similarity_search = SimilaritySearch()
            st.session_state.hitl_handler = HITLHandler()
            
            st.success("✅ System initialized successfully!")
            return True
        except Exception as e:
            st.error(f"❌ Initialization failed: {e}")
            return False


def display_header():
    """Display the app header."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title(f"🧮 {APP_NAME}")
        st.caption(f"AI-Powered Math Problem Solver with Step-by-Step Explanations | v{APP_VERSION}")
    
    with col2:
        # Display stats
        stats = st.session_state.memory_store.get_stats()
        st.metric("Problems Solved", stats.get("total_interactions", 0))


def display_input_section():
    """Display the input section."""
    st.subheader("📝 Input Your Math Problem")
    
    # Input mode selector
    input_mode = st.radio(
        "Choose input mode:",
        ["📄 Text", "📸 Image", "🎤 Audio"],
        horizontal=True
    )
    
    user_input = None
    input_type = "text"
    
    if input_mode == "📄 Text":
        user_input = st.text_area(
            "Type your math problem:",
            placeholder="Example: Solve x² + 5x + 6 = 0",
            height=100
        )
        input_type = "text"
    
    elif input_mode == "📸 Image":
        uploaded_image = st.file_uploader(
            "Upload an image of the problem:",
            type=["png", "jpg", "jpeg"]
        )
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
            user_input = uploaded_image.read()
            input_type = "image"
    
    elif input_mode == "🎤 Audio":
        uploaded_audio = st.file_uploader(
            "Upload an audio file:",
            type=["wav", "mp3", "m4a"]
        )
        if uploaded_audio:
            st.audio(uploaded_audio)
            user_input = uploaded_audio.read()
            input_type = "audio"
    
    return user_input, input_type


def process_input(user_input, input_type):
    """Process the user input."""
    with st.spinner("🔄 Processing input..."):
        if input_type == "text":
            processor = TextProcessor()
            result = processor.process(user_input)
        
        elif input_type == "image":
            processor = OCRProcessor()
            result = processor.process(image_bytes=user_input)
        
        elif input_type == "audio":
            processor = AudioProcessor()
            result = processor.process(audio_bytes=user_input)
        
        return result


def display_extracted_text(processed_input):
    """Display extracted text for user confirmation."""
    confidence = processed_input.get("confidence", 0.0)
    
    # Show warning if confidence is low
    if confidence < 0.7:
        st.warning(f"⚠️ Low Confidence Extraction ({confidence:.0%}) - Please verify carefully!")
    else:
        st.info(f"✅ Extraction Confidence: {confidence:.0%}")
    
    st.write("**Extracted Text:**")
    
    extracted_text = processed_input.get("processed_text", "")
    
    # Allow user to edit
    corrected_text = st.text_area(
        "Please verify and correct if needed:",
        value=extracted_text,
        height=100,
        key="extracted_text_edit"
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("✅ Looks Good - Solve It!", use_container_width=True, type="primary"):
            return corrected_text, True
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.show_review = False
            st.rerun()
            return None, False
    
    return corrected_text, None


def solve_problem(problem_text):
    """Solve the math problem."""
    with st.spinner("🧠 Solving your problem..."):
        # Find similar past problems
        similar = st.session_state.similarity_search.find_similar(problem_text, top_k=2)
        memory_context = st.session_state.similarity_search.format_similar_as_context(similar)
        
        # Solve
        result = st.session_state.orchestrator.solve_problem(problem_text, memory_context)
        
        st.session_state.current_result = result
        
        # Save to memory
        interaction_data = {
            "input_type": "text",
            "raw_input": problem_text,
            "parsed_question": result.get("parsed", {}),
            "topic": result.get("parsed", {}).get("topic", ""),
            "retrieved_context": result.get("retrieved_context", []),
            "solution_steps": result.get("solution", {}).get("solution_steps", []),
            "final_answer": result.get("final_answer", ""),
            "confidence": result.get("confidence", 0.0),
            "is_correct": result.get("is_correct", False),
            "explanation": result.get("explanation", {}).get("explanation", ""),
            "agent_trace": result.get("agent_trace", [])
        }
        
        interaction_id = st.session_state.memory_store.save_interaction(interaction_data)
        st.session_state.current_interaction_id = interaction_id
        
        return result


def display_agent_trace(result):
    """Display the agent execution trace."""
    with st.expander("🤖 Agent Trace", expanded=False):
        trace = result.get("agent_trace", [])
        
        for step in trace:
            status_icon = "✅" if "Complete" in step.get("status", "") else "❌"
            st.write(f"{status_icon} **{step.get('agent', 'Unknown')}** ({step.get('duration', 0)}s)")
            st.caption(f"   {step.get('output_summary', '')}")


def display_retrieved_context(result):
    """Display retrieved RAG context."""
    with st.expander("📚 Retrieved Knowledge", expanded=False):
        sources = result.get("retrieved_context", [])
        
        if not sources:
            st.info("No relevant sources found")
        else:
            for i, source in enumerate(sources, 1):
                st.markdown(f"**Source {i}:** {Path(source.get('source', 'Unknown')).stem}")
                st.caption(f"Relevance: {source.get('relevance_score', 0.0)}")
                with st.container():
                    st.text(source.get("content", "")[:300] + "...")
                st.divider()


def display_solution(result):
    """Display the solution."""
    st.subheader("✨ Solution")
    
    solution = result.get("solution", {})
    
    # Display confidence
    confidence = result.get("confidence", 0.0)
    is_correct = result.get("is_correct", False)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if is_correct:
            st.success(f"**Final Answer:** {result.get('final_answer', 'N/A')}")
        else:
            st.warning(f"**Final Answer:** {result.get('final_answer', 'N/A')}")
    
    with col2:
        st.metric("Confidence", f"{confidence:.0%}")
    
    # Display solution steps
    st.markdown("**Step-by-Step Solution:**")
    
    steps = solution.get("solution_steps", [])
    for step in steps:
        st.markdown(f"**Step {step.get('step', '?')}:** {step.get('description', '')}")
        st.code(step.get('math', ''), language="")


def display_explanation(result):
    """Display the explanation."""
    with st.expander("📖 Detailed Explanation", expanded=True):
        explanation_data = result.get("explanation", {})
        
        explanation = explanation_data.get("explanation", "No explanation available")
        st.markdown(explanation)
        
        # Key concepts
        concepts = explanation_data.get("key_concepts", [])
        if concepts:
            st.markdown("**🔑 Key Concepts:**")
            for concept in concepts:
                st.markdown(f"- {concept}")
        
        # Tips
        tips = explanation_data.get("tips", [])
        if tips:
            st.markdown("**💡 Tips for Similar Problems:**")
            for tip in tips:
                st.markdown(f"- {tip}")
        
        # Common mistakes
        mistakes = explanation_data.get("common_mistakes_to_avoid", [])
        if mistakes:
            st.markdown("**⚠️ Common Mistakes to Avoid:**")
            for mistake in mistakes:
                st.markdown(f"- {mistake}")


def display_feedback_section():
    """Display feedback buttons."""
    st.divider()
    st.subheader("📊 Was this solution helpful?")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("✅ Correct", use_container_width=True):
            st.session_state.memory_store.update_feedback(
                st.session_state.current_interaction_id,
                "correct"
            )
            st.success("Thank you! I'll remember this.")
            st.balloons()
    
    with col2:
        if st.button("❌ Incorrect", use_container_width=True):
            st.session_state.feedback_mode = "incorrect"
    
    # Correction input
    if st.session_state.get("feedback_mode") == "incorrect":
        correction = st.text_area("Please provide the correct answer or explain what's wrong:")
        if st.button("Submit Correction"):
            st.session_state.memory_store.update_feedback(
                st.session_state.current_interaction_id,
                "incorrect",
                correction
            )
            st.warning("Thank you for the correction! I'll learn from this.")
            st.session_state.feedback_mode = None


def display_sidebar():
    """Display the sidebar with stats and settings."""
    with st.sidebar:
        st.header("📊 Statistics")
        
        stats = st.session_state.memory_store.get_stats()
        
        st.metric("Total Problems", stats.get("total_interactions", 0))
        st.metric("Accuracy Rate", f"{stats.get('accuracy_rate', 0)}%")
        st.metric("Avg Confidence", f"{stats.get('average_confidence', 0):.0%}")
        
        st.divider()
        
        st.header("📚 By Topic")
        by_topic = stats.get("by_topic", {})
        for topic, count in by_topic.items():
            st.write(f"**{topic.title()}:** {count}")
        
        st.divider()
        
        st.header("🔧 Settings")
        if st.button("🔄 Rebuild RAG Index", use_container_width=True):
            with st.spinner("Rebuilding..."):
                build_index()
            st.success("Index rebuilt!")


# =============================================================================
# MAIN APP
# =============================================================================

def main():
    """Main application logic."""
    
    # Initialize system if not done
    if st.session_state.orchestrator is None:
        if not initialize_system():
            st.stop()
    
    # Display header
    display_header()
    
    # Sidebar
    display_sidebar()
    
    # Main content
    st.divider()
    
    # If showing review, display that first
    if st.session_state.show_review:
        st.subheader("📋 Please Verify Extracted Text")
        corrected_text, confirmed = display_extracted_text(st.session_state.pending_input)
        
        if confirmed is True:
            st.session_state.show_review = False
            result = solve_problem(corrected_text)
            st.session_state.show_result = True
            st.rerun()
        elif confirmed is False:
            st.session_state.show_review = False
            st.rerun()
        return
    
    # Input section
    user_input, input_type = display_input_section()
    
    # Process button
    if st.button("🚀 Solve Problem", type="primary", use_container_width=True):
        if not user_input:
            st.warning("⚠️ Please provide input first!")
        else:
            # Process input
            processed_input = process_input(user_input, input_type)
            
            if not processed_input.get("success"):
                st.error(f"❌ Error processing input: {processed_input.get('error', 'Unknown error')}")
            else:
                # ALWAYS show extracted text for review if image/audio
                if input_type in ["image", "audio"]:
                    st.session_state.pending_input = processed_input
                    st.session_state.show_review = True
                    st.rerun()
                else:
                    # Solve directly for text input
                    problem_text = processed_input.get("processed_text", user_input)
                    result = solve_problem(problem_text)
                    st.session_state.show_result = True
    
    # Display results
    if st.session_state.show_result and st.session_state.current_result:
        result = st.session_state.current_result
        
        # Agent trace
        display_agent_trace(result)
        
        # Retrieved context
        display_retrieved_context(result)
        
        st.divider()
        
        # Solution
        display_solution(result)
        
        # Explanation
        display_explanation(result)
        
        # Feedback
        display_feedback_section()


if __name__ == "__main__":
    main()
# 🧮 Math Mentor

An AI-powered math problem solver that accepts text, image, and audio inputs, provides step-by-step solutions, learns from feedback, and improves over time.

## 🌟 Features

- **Multimodal Input**: Text, Image (OCR), and Audio (Speech-to-Text)
- **Multi-Agent System**: 5 specialized agents (Parser, Router, Solver, Verifier, Explainer)
- **RAG Pipeline**: Retrieves relevant formulas and methods from curated knowledge base
- **Human-in-the-Loop**: Asks for help when uncertain
- **Memory & Learning**: Remembers past problems and improves over time
- **Step-by-Step Explanations**: Clear, student-friendly breakdowns

## 📋 Prerequisites

- Python 3.9 or higher
- Groq API key (free)

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd math-mentor

2. Install dependencies
Bash

pip install -r requirements.txt
3. Set up environment variables
Copy .env.example to .env:

Bash

copy .env.example .env
Edit .env and add your Groq API key:

text

GROQ_API_KEY=your_groq_api_key_here
Get free Groq API key: https://console.groq.com/keys

4. Build the RAG index (first time only)
Bash

python rag/indexer.py
This will process the knowledge base and create a vector store.

▶️ Running the Application
Bash

streamlit run app.py
The app will open in your browser at http://localhost:8501

🎯 Usage
Text Input
Select "📄 Text"
Type your math problem
Click "Solve Problem"
Image Input
Select "📸 Image"
Upload a photo or screenshot
Verify extracted text (IMPORTANT: Always check OCR output!)
Click "Looks Good - Solve It!"
Audio Input
Select "🎤 Audio"
Upload an audio file
Review transcription
Click "Solve Problem"
🤝 Human-in-the-Loop (HITL)
HITL is triggered when:

OCR/Audio confidence is low (< 70%)
Parser needs clarification
Verifier is uncertain (< 80% confidence)
Always verify extracted text from images/audio before solving!

📊 Memory & Learning
The system stores every interaction in memory/memory.db (SQLite).

Remembers past problems
Learns from corrections
Reuses successful solution patterns
🧪 Testing Individual Components

🏗️ Architecture

User Input (Text/Image/Audio)
    ↓
Input Processors (OCR/Whisper/Text)
    ↓
Parser Agent → Structured Problem
    ↓
Router Agent → Problem Classification
    ↓
RAG Retrieval → Relevant Knowledge
    ↓
Solver Agent → Step-by-Step Solution
    ↓
Verifier Agent → Correctness Check
    ↓
Explainer Agent → Student-Friendly Explanation
    ↓
Display + Memory Storage

🔧 Technology Stack
LLM: Groq (Llama 3.3 70B) - Free API
Embeddings: HuggingFace (sentence-transformers) - Free, Local
Vector Store: ChromaDB
OCR: EasyOCR
Speech-to-Text: Groq Whisper
UI: Streamlit
Memory: SQLite
Agents: LangGraph

🐛 Troubleshooting
Error: "GROQ_API_KEY not found"

Make sure .env file exists and contains your API key
Error: "Vector store not found"

Run python rag/indexer.py to build the RAG index
OCR not working well

Use clear, high-contrast images
Larger font size helps
Always verify extracted text manually

👨‍💻 Author - Unnathi Yamavaram


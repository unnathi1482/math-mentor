# 🧮 Math Mentor

**Math Mentor** is an AI-powered assistant designed to help students solve mathematics problems with clear, step-by-step explanations.
It supports **text, image, and audio inputs**, retrieves relevant mathematical knowledge, and uses a **multi-agent reasoning pipeline** to generate reliable solutions.

The system is designed not only to solve problems, but also to **explain the reasoning process**, helping students understand the concepts behind the solution.

---

## 🌟 Key Features

**Multimodal Problem Input**

* 📄 **Text Input** – type a math problem directly
* 📸 **Image Input** – upload photos or screenshots of questions
* 🎤 **Audio Input** – speak a problem and convert speech to text

**Multi-Agent Architecture**

The system uses specialized agents working together:

* **Parser Agent** – converts raw input into structured math problems
* **Router Agent** – identifies the type of mathematical task
* **Solver Agent** – generates a step-by-step solution
* **Verifier Agent** – checks solution correctness
* **Explainer Agent** – rewrites the solution for student clarity

**Retrieval-Augmented Generation (RAG)**

Relevant formulas, methods, and examples are retrieved from a curated knowledge base before solving.

**Human-in-the-Loop**

If the system is uncertain (low confidence or unclear input), it requests clarification from the user.

**Memory System**

The application stores previous interactions and solutions, allowing it to:

* recall past problems
* reuse successful reasoning patterns
* improve explanations over time

---

## 🏗️ System Architecture

```
User Input (Text / Image / Audio)
        │
        ▼
Input Processors
(OCR / Speech-to-Text / Text)
        │
        ▼
Parser Agent
        │
        ▼
Router Agent
(problem classification)
        │
        ▼
RAG Retrieval
(knowledge base lookup)
        │
        ▼
Solver Agent
(step-by-step reasoning)
        │
        ▼
Verifier Agent
(correctness validation)
        │
        ▼
Explainer Agent
(student-friendly explanation)
        │
        ▼
UI Display + Memory Storage
```

---

## 🧰 Technology Stack

**LLM Inference**

* Groq (Llama 3.3 70B)

**Frameworks & Libraries**

* Streamlit — interactive web interface
* LangGraph — multi-agent orchestration
* ChromaDB — vector database for RAG
* HuggingFace Sentence Transformers — embeddings
* EasyOCR — image text extraction
* Groq Whisper — speech-to-text

**Storage**

* SQLite — conversation and solution memory

---

## 📂 Project Structure

```
math-mentor
│
├── app.py                  # Streamlit application
├── requirements.txt
├── README.md
│
├── agents/                 # Multi-agent reasoning pipeline
├── input_processors/       # OCR, speech, and text processing
├── rag/                    # Retrieval-Augmented Generation
│   └── knowledge_base/
├── memory/                 # Persistent memory store
├── tools/                  # Utility tools (calculator etc.)
└── utils/                  # Config, prompts, API client
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/unnathi1482/math-mentor.git
cd math-mentor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example environment file:

```bash
copy .env.example .env
```

Then open `.env` and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

You can obtain a free API key from the Groq console.

---

## 🔎 Build the Knowledge Index (First Run)

Before running the application, generate the vector index used for retrieval:

```bash
python rag/indexer.py
```

This step processes the knowledge base and creates the vector store.

---

## ▶️ Running the Application

Start the Streamlit interface:

```bash
streamlit run app.py
```

The application will launch in your browser at:

```
http://localhost:8501
```

---

## 🎯 Usage

### Text Input

1. Select **Text**
2. Enter a math problem
3. Click **Solve Problem**

### Image Input

1. Select **Image**
2. Upload a photo or screenshot
3. Verify the extracted OCR text
4. Solve the problem

### Audio Input

1. Select **Audio**
2. Upload an audio recording
3. Review the transcription
4. Solve the problem

---

## 🤝 Human-in-the-Loop (HITL)

The system requests user confirmation when:

* OCR confidence is low
* speech transcription is uncertain
* the parser needs clarification
* the verifier detects a possible mistake

This helps maintain solution accuracy.

---

## 🧠 Memory System

All interactions are stored locally using SQLite.

The system can:

* remember previously solved problems
* learn from corrections
* reuse successful reasoning patterns

Database location:

```
memory/memory.db
```

---

## 🐛 Troubleshooting

**GROQ_API_KEY not found**

Ensure your `.env` file exists and contains the API key.

**Vector store not found**

Run:

```
python rag/indexer.py
```

**OCR inaccuracies**

For best results:

* use clear, high-contrast images
* avoid handwritten text if possible
* verify extracted text before solving

---

## 👨‍💻 Author

**Unnathi Yamavaram**

AI / ML Developer
GitHub: [https://github.com/unnathi1482](https://github.com/unnathi1482)

---

## 📄 License

This project is open source and available under the MIT License.


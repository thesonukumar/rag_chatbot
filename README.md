# Serverless RAG Chatbot
> A production-ready, stateless Retrieval-Augmented Generation engine for interactive PDF intelligence.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1.0-black?style=for-the-badge&logo=flask)
![LangChain](https://img.shields.io/badge/LangChain-0.3.25-green?style=for-the-badge&logo=langchain)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector_DB-blue?style=for-the-badge&logo=pinecone)
![Gemini](https://img.shields.io/badge/Google_Gemini-3.1_Flash_Lite-orange?style=for-the-badge&logo=google)

## 🛠 Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Flask** | Core web framework, routing, and HTTP session management. |
| **LangChain** | Orchestration framework for LLM chaining, chunking, and retrieval logic. |
| **Google Gemini API** | Provides both `gemini-embedding-2` for vectorization and `gemini-3.1-flash-lite` for generation. |
| **Pinecone** | Cloud-native vector database for stateless, horizontally scalable semantic search. |
| **PyPDF** | Parses and extracts raw text from uploaded PDF documents. |
| **Vanilla JS & CSS** | Provides a modern, responsive, and animated Glassmorphism frontend UI. |

## 📋 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Installation & Setup](#️-installation--setup)
- [Usage](#-usage)
- [Configuration Reference](#️-configuration-reference)
- [Guardrails & Safety](#-guardrails--safety)
- [Contributing](#-contributing)
- [License](#-license)

## 📖 Overview

This project is a high-performance Retrieval-Augmented Generation (RAG) chatbot designed to extract strictly sourced answers from user-uploaded PDFs. It solves the critical issues of LLM token limitations, hallucinations, and high inference costs by exclusively querying mathematically relevant document chunks. Its stateless, serverless-ready architecture ensures complete user privacy through session-isolated vector namespaces while gracefully handling strict external API rate limits.

## 🏗 System Architecture

The application operates on a strict **Ingestion → Retrieval → Generation** workflow to process data efficiently and safely.

1. **Ingestion**: Uploaded PDFs are parsed, chunked into overlapping segments, converted into 3072-dimensional vectors using Gemini embeddings, and batched to Pinecone.
2. **Retrieval**: User queries are vectorized. Pinecone executes a similarity search to return the top 15 most relevant chunks specifically isolated to the active user's session namespace.
3. **Generation**: The retrieved chunks, along with the recent conversational memory, are injected into a strict prompt. The LLM generates an answer relying solely on the provided context.

```text
[PDF Upload] → (PyPDFLoader) → (TextSplitter) → [Gemini Embedder] → [Pinecone Vector DB]
                                                                        ↓
[User Query] → (Query Vectorization) → [Similarity Search (Top K)] ←────┘
                                               ↓
[Context Chunks + Chat History] → [Strict Prompt Template] → [Gemini 3.1 LLM] → [Answer]
```

## 📂 Project Structure

```text
rag_chatbot/
├── .env                    # Environment variables (API keys)
├── app.py                  # Main Flask application and API route definitions
├── documentation.txt       # Internal architectural design documentation
├── requirements.txt        # Production Python dependency manifest
├── vercel.json             # Deployment configuration for Vercel environments
├── src/                    # Core RAG Logic
│   ├── __init__.py         # Package initialization marker
│   ├── chunker.py          # Handles text splitting (1000 chars, 200 overlap)
│   ├── document_loader.py  # PDF parsing logic using PyPDF
│   ├── embedder.py         # Interfaces with Gemini Embedding API
│   ├── generator.py        # Orchestrates the Chat model and context prompting
│   ├── retriever.py        # Executes vector similarity searches against Pinecone
│   └── vector_store.py     # Manages Pinecone DB connection, batching, and indexing
├── static/                 # Static Assets
│   └── style.css           # Custom Glassmorphism UI styles and animations
└── templates/              # HTML Templates
    └── index.html          # Vanilla JS frontend interface
```

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- Google API Key (for Gemini)
- Pinecone API Key

### Step-by-Step Installation

```bash
# 1. Clone the repository
git clone https://github.com/thesonukumar/rag_chatbot.git
cd rag_chatbot

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 3. Install required dependencies
pip install -r requirements.txt
```

### Environment Configuration
Create a `.env` file in the root directory.

| Variable Name | Description | Example Value |
| :--- | :--- | :--- |
| `GOOGLE_API_KEY` | Authentication key for Google Gemini (Embeddings & Generation). | `AIzaSyB...` |
| `PINECONE_API_KEY` | Authentication key for your Pinecone vector database environment. | `pc-sk-123...` |

## 🚀 Usage

Start the application server:

```bash
python app.py
# Or for production deployment: gunicorn app:app
```

**Expected Terminal Output:**

```text
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

Once running, navigate to `http://127.0.0.1:5000` in your web browser. Upload your PDF documents using the UI and begin chatting.

## ⚙️ Configuration Reference

The internal RAG parameters are tuned for optimal performance within free-tier constraints.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `CHUNK_SIZE` | `int` | `1000` | The number of characters per document segment. |
| `CHUNK_OVERLAP` | `int` | `200` | The character overlap between chunks to preserve context. |
| `TOP_K` | `int` | `15` | The number of semantic chunks retrieved per query. |
| `EMBEDDING_DIMENSIONS`| `int` | `3072` | The vector space dimensionality used by `gemini-embedding-2`. |
| `UPLOAD_FOLDER` | `string` | `'/tmp/data'` | Local path for temporary PDF parsing before cleanup. |
| `MAX_CONTENT_LENGTH` | `int` | `16MB` | Enforced maximum file upload size per request. |

## 🛡 Guardrails & Safety

This system implements three core production guardrails to ensure reliability and data privacy:

1. **User Isolation (Session Namespaces)**
   Every user's uploaded document embeddings are isolated in the Pinecone database using a unique `session_id` namespace. It is cryptographically impossible for one user to retrieve contextual chunks belonging to another user's session.

2. **API Rate-Limit Protection (Backoff Engine)**
   Google’s strict API quota (100 RPM) is actively managed during the ingestion phase. The vector store implements automated batching and a 60-second pause-and-resume mechanism when `429 Quota Exceeded` errors are detected, preventing pipeline crashes.

3. **Hallucination & Prompt Injection Defense**
   The generator prompt acts as a strict sandbox. The LLM is explicitly instructed to synthesize answers *only* using the retrieved semantic chunks. If the answer cannot be found in the provided context, it will refuse to guess, drastically reducing the risk of confident hallucinations.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

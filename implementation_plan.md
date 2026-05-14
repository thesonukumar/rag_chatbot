# 🧠 RAG PDF Q&A Chatbot — Learning Roadmap

> This is NOT a "copy-paste and run" plan. This is a **learning journey** where you understand every concept deeply before writing a single line of code for it.

---

## How This Roadmap Works

Each phase follows this pattern:

```
📖 CONCEPT   → What is it? Why do we need it? How does it work?
🔨 BUILD     → Write the code yourself (with guidance)
✅ CHECKPOINT → Verify you understood it before moving on
🧩 YOUR CALL → Decisions YOU make (not me)
```

> [!IMPORTANT]
> **You are in control.** At every phase, I'll explain the concept, give you options, and YOU decide how to proceed. If something doesn't make sense — stop me and ask.

---

## The Big Picture: What Are We Building?

Before we write any code, let's understand the **problem** and the **solution**.

### The Problem
You have a 200-page PDF textbook. You want to ask: *"What does chapter 5 say about neural networks?"*

A normal ChatGPT/Gemini **cannot answer this** because:
- It has never seen YOUR specific PDF
- It has a token limit (can't read 200 pages at once)
- It might hallucinate (make up answers)

### The Solution: RAG (Retrieval-Augmented Generation)

RAG is a 3-step process:

```
┌─────────────────────────────────────────────────────────┐
│                    RAG PIPELINE                         │
│                                                         │
│  📄 PDF                                                 │
│   ↓                                                     │
│  ✂️ CHUNK → Split into small pieces                     │
│   ↓                                                     │
│  🔢 EMBED → Convert text to numbers (vectors)           │
│   ↓                                                     │
│  💾 STORE → Save vectors in a database                  │
│   ↓                                                     │
│  ❓ User asks a question                                │
│   ↓                                                     │
│  🔍 RETRIEVE → Find the most relevant chunks            │
│   ↓                                                     │
│  🤖 GENERATE → Send chunks + question to LLM            │
│   ↓                                                     │
│  💬 Answer with sources!                                │
└─────────────────────────────────────────────────────────┘
```

### Key Vocabulary (Bookmark This!)

| Term | Meaning |
|---|---|
| **LLM** | Large Language Model — the AI brain (GPT, Gemini, Llama) |
| **Embedding** | Converting text into a list of numbers that capture its *meaning* |
| **Vector** | That list of numbers (e.g., `[0.12, -0.45, 0.78, ...]`) |
| **Vector Database** | A database optimized for searching by meaning, not keywords |
| **Chunk** | A small piece of your document (e.g., 500 words) |
| **Retrieval** | Finding the most relevant chunks for a question |
| **Generation** | The LLM producing a human-readable answer using the retrieved context |
| **Context Window** | Maximum amount of text an LLM can process at once |
| **Prompt Template** | A structured way to tell the LLM what to do with the retrieved text |

---

## Phase 0: Environment & Tools Setup

### 📖 Concept: Why Do We Need a Virtual Environment?

When you install Python packages, they go into a global location. But different projects need different versions of the same package. A **virtual environment** is an isolated box for each project's dependencies.

```
Global Python ──→ Project A needs langchain 0.1
                  Project B needs langchain 0.3   ← CONFLICT!

Virtual Env    ──→ Project A (own langchain 0.1)  ← NO CONFLICT!
               ──→ Project B (own langchain 0.3)
```

### 🔨 Build Steps
1. Create a virtual environment
2. Create a `requirements.txt` (dependency list)
3. Install core dependencies
4. Understand what each dependency does

### Dependencies We'll Use

| Package | What It Does | Why We Need It |
|---|---|---|
| `langchain` | RAG framework | Orchestrates the entire pipeline |
| `langchain-community` | Community integrations | PDF loaders, vector stores |
| `pypdf` | PDF reader | Extracts text from PDFs |
| `chromadb` | Vector database | Stores and searches embeddings locally |
| `python-dotenv` | Environment variables | Keeps API keys safe |
| `streamlit` | Web UI framework | Simple frontend (no HTML/CSS needed) |

> [!NOTE]
> We'll also need an **LLM provider** and an **embedding model**. That's YOUR first decision below.

### 🧩 YOUR CALL: Choose Your LLM

| Option | Package to Install | Cost | Setup |
|---|---|---|---|
| **Google Gemini** | `langchain-google-genai` | Free tier (60 requests/min) | Get API key from [AI Studio](https://aistudio.google.com/apikey) |
| **OpenAI (GPT)** | `langchain-openai` | ~$0.01 per query | Get API key from [OpenAI](https://platform.openai.com/api-keys) |
| **Ollama (Local)** | `langchain-ollama` | Completely free | Install [Ollama](https://ollama.com) + download a model |

> **My suggestion for learning:** Google Gemini — it's free, high quality, and easy to set up. But YOU decide.

### ✅ Checkpoint
Before moving on, you should be able to answer:
- What is a virtual environment and why do we use one?
- What does each package in `requirements.txt` do?
- Where is your API key stored and why shouldn't it be in your code?

---

## Phase 1: Load a PDF (Document Loading)

### 📖 Concept: How Do Computers Read PDFs?

A PDF is **not plain text** — it's a complex format with fonts, images, layouts, and metadata. We need a **parser** to extract the readable text from it.

Different parsers have different strengths:

| Parser | Good At | Bad At |
|---|---|---|
| `PyPDF` | Simple text PDFs, fast | Complex layouts, tables |
| `PDFPlumber` | Tables, structured data | Slower |
| `Unstructured` | Everything | Heavy, complex setup |

We'll start with **PyPDF** (simplest) and you can upgrade later.

### 🔨 Build Steps
1. Create `src/document_loader.py`
2. Load a sample PDF
3. Print the raw extracted text
4. Inspect: How many pages? What does the text look like?

### Key Learning: What is a "Document" Object?

In LangChain, a **Document** is a simple object with two fields:
```python
Document(
    page_content="The actual text from the PDF...",
    metadata={"source": "myfile.pdf", "page": 0}
)
```
This structure is important because **metadata** lets us track WHERE information came from (which page, which file).

### 🧩 YOUR CALL
- Which PDF will you use for testing? (Pick something you're familiar with so you can verify the answers!)

### ✅ Checkpoint
- Can you load a PDF and print its text?
- What information is in the `metadata`?
- What problems do you notice with the raw text? (formatting issues, headers/footers, etc.)

---

## Phase 2: Chunking (Text Splitting)

### 📖 Concept: Why Can't We Send the Whole Document?

Two critical reasons:

**1. Token Limits:** LLMs have a maximum input size (called "context window")
- GPT-4: ~128K tokens (~96K words)
- Gemini 1.5: ~1M tokens
- But bigger input = slower + more expensive!

**2. Retrieval Precision:** If you send 200 pages, the LLM gets confused. If you send the *exact 3 paragraphs* that answer the question, the LLM gives a precise answer.

### Chunking Strategies

```
Strategy 1: Fixed Size (Simple)
─────────────────────────────
[    500 chars    ][    500 chars    ][    500 chars    ]
Problem: May cut sentences in half!

Strategy 2: Fixed Size + Overlap (Better)
─────────────────────────────────────────
[    500 chars    ]
          [    500 chars    ]          ← 100 char overlap
                    [    500 chars    ]
Why overlap? So context isn't lost at boundaries!

Strategy 3: Recursive Character Splitting (Best for text)
─────────────────────────────────────────────────────────
Tries to split by: \n\n → \n → " " → ""
Preserves paragraph structure!
```

### 🔨 Build Steps
1. Create `src/chunker.py`
2. Implement `RecursiveCharacterTextSplitter`
3. **Experiment**: Try different `chunk_size` and `chunk_overlap` values
4. Print chunks and manually inspect them

### 🧩 YOUR CALL: Chunk Parameters

| Parameter | What It Controls | Typical Range |
|---|---|---|
| `chunk_size` | Max characters per chunk | 200–2000 |
| `chunk_overlap` | Characters shared between adjacent chunks | 50–200 |

> Try `chunk_size=1000` and `chunk_overlap=200` first, then experiment!

### ✅ Checkpoint
- How many chunks did your PDF produce?
- Look at chunk boundaries — are sentences being cut?
- What happens when you make `chunk_size` very small (100) vs very large (5000)?
- Why does overlap matter? Can you find an example where removing overlap loses context?

---

## Phase 3: Embeddings (Text → Numbers)

### 📖 Concept: What Are Embeddings?

This is the **most important concept in RAG**. Let's break it down.

**Problem:** Computers can't understand meaning. The word "dog" is just 3 characters to a computer.

**Solution:** Convert words into **vectors** (lists of numbers) where **similar meanings = similar numbers**.

```
"dog"  → [0.82, -0.12, 0.45, 0.33, ...]    (768 numbers)
"puppy" → [0.80, -0.10, 0.47, 0.31, ...]   ← Very similar!
"car"  → [-0.21, 0.67, -0.33, 0.11, ...]    ← Very different!
```

**How is similarity measured?** Using **cosine similarity** — the angle between two vectors:
- Cosine = 1.0 → identical meaning
- Cosine = 0.0 → unrelated
- Cosine = -1.0 → opposite meaning

### Embedding Models

| Model | Dimensions | Quality | Cost |
|---|---|---|---|
| `text-embedding-004` (Google) | 768 | Great | Free tier |
| `text-embedding-3-small` (OpenAI) | 1536 | Great | Paid |
| `nomic-embed-text` (Ollama) | 768 | Good | Free (local) |

### 🔨 Build Steps
1. Create `src/embedder.py`
2. Embed a single sentence and inspect the vector
3. Embed multiple sentences and compute similarity between them
4. **Experiment**: Embed similar vs different sentences — see the similarity scores!

### ✅ Checkpoint
- What does an embedding vector look like? How many dimensions?
- If you embed "What is machine learning?" and "Explain ML to me" — are they similar?
- If you embed "What is machine learning?" and "How to cook pasta?" — are they similar?
- Why can't we use keyword search instead? (Hint: synonyms!)

---

## Phase 4: Vector Store (Storing & Searching Embeddings)

### 📖 Concept: What Is a Vector Database?

A regular database searches by **exact match**:
```sql
SELECT * FROM docs WHERE content LIKE '%machine learning%'
```
This FAILS for: *"Explain ML"* — because "ML" ≠ "machine learning" as text.

A **vector database** searches by **meaning**:
```
Query: "Explain ML" → vector → find closest vectors → return matching chunks
```

### Why ChromaDB?

We'll use **ChromaDB** because:
- ✅ Runs locally (no cloud setup)
- ✅ Free and open source
- ✅ Stores data on disk (persists between runs)
- ✅ Perfect for learning

Other options (for your knowledge): Pinecone (cloud), Weaviate, FAISS, Qdrant

### 🔨 Build Steps
1. Create `src/vector_store.py`
2. Create a ChromaDB collection
3. Add your chunked + embedded documents
4. Query it with a question and see what comes back!

### 🧩 YOUR CALL
- Should the vector store persist on disk or rebuild every time? (Persistence is better for large PDFs)

### ✅ Checkpoint
- How many vectors are stored?
- When you search for a question, do the returned chunks actually contain relevant info?
- What happens if you search for something NOT in the document?
- Try the same question in different words — does it still find the right chunks?

---

## Phase 5: Retrieval (Finding Relevant Information)

### 📖 Concept: How Does Retrieval Work?

```
User Question: "What is backpropagation?"
         ↓
   Embed the question → [0.45, -0.12, ...]
         ↓
   Search vector store for closest matches
         ↓
   Return top-K most similar chunks
         ↓
   These chunks become the "context" for the LLM
```

### Key Parameter: `k` (Number of Results)

| k value | Effect |
|---|---|
| `k=1` | Very focused, might miss info |
| `k=3-5` | Good balance (recommended) |
| `k=10+` | More context but might confuse the LLM |

### Advanced Retrieval (for later)
- **MMR (Maximal Marginal Relevance)**: Avoids returning duplicate-ish chunks
- **Re-ranking**: Use a second model to re-score results
- **Hybrid Search**: Combine keyword search + semantic search

### 🔨 Build Steps
1. Create `src/retriever.py`
2. Implement basic similarity search
3. Test with multiple questions
4. Print the retrieved chunks with their similarity scores

### ✅ Checkpoint
- For a given question, are the top-K results actually relevant?
- What's the similarity score of the best match vs the worst?
- Does changing `k` improve or worsen the results?

---

## Phase 6: Generation (LLM Answering with Context)

### 📖 Concept: What Is a Prompt Template?

We don't just send the question to the LLM. We send a **structured prompt**:

```
System: You are a helpful assistant that answers questions 
based ONLY on the provided context. If the context doesn't 
contain the answer, say "I don't know."

Context:
{retrieved_chunks_go_here}

Question: {user_question}

Answer:
```

**Why "based ONLY on the provided context"?** → To prevent **hallucination** (the LLM making up answers not in your document).

### 🔨 Build Steps
1. Create `src/generator.py`
2. Set up the LLM connection (Gemini/OpenAI/Ollama)
3. Create a prompt template
4. Send retrieved context + question → get answer!
5. **Experiment**: What happens if you remove "ONLY based on context"?

### 🧩 YOUR CALL
- How strict should the LLM be? (Only answer from context vs. allowed to use general knowledge too?)
- Should the answer include source references? (e.g., "According to page 5...")

### ✅ Checkpoint
- Does the LLM answer correctly based on the PDF content?
- Does it say "I don't know" for questions not in the PDF?
- What happens with a bad prompt template?

---

## Phase 7: Complete RAG Pipeline

### 📖 Concept: Chaining Everything Together

Now we connect all the pieces:

```
PDF → Loader → Chunker → Embedder → Vector Store
                                          ↓
User Question → Embed Question → Retriever → Generator → Answer
```

### 🔨 Build Steps
1. Create `src/rag_pipeline.py` — the main orchestrator
2. Create `main.py` — command-line interface
3. Two modes:
   - **Ingest mode**: Load PDF → Chunk → Embed → Store
   - **Query mode**: Question → Retrieve → Generate → Answer

### Project Structure at This Point

```
RAG/
├── .env                    ← API keys (never commit this!)
├── requirements.txt        ← Dependencies
├── main.py                 ← Entry point
├── src/
│   ├── __init__.py
│   ├── document_loader.py  ← Phase 1
│   ├── chunker.py          ← Phase 2
│   ├── embedder.py         ← Phase 3
│   ├── vector_store.py     ← Phase 4
│   ├── retriever.py        ← Phase 5
│   ├── generator.py        ← Phase 6
│   └── rag_pipeline.py     ← Phase 7 (connects everything)
├── data/                   ← Your PDF files
├── vectorstore/            ← ChromaDB storage
└── tests/                  ← Test scripts
```

### ✅ Checkpoint
- Can you ingest a PDF and then ask questions about it via terminal?
- Does the full pipeline work end-to-end?
- Can you explain what happens at each step when a user asks a question?

---

## Phase 8: Web UI (Flask)

### 📖 Concept: Why Flask?

Streamlit is great for rapid Python-only prototypes, but **Flask** gives you complete control over your web application. You get to build a real frontend using HTML, CSS, and JavaScript.

This is perfect for creating a polished, modern, and highly customized Chat Interface for your RAG system. We'll use:
- **Backend:** Flask (Python) to serve endpoints for uploading and chatting.
- **Frontend:** HTML, vanilla CSS (for a modern premium look), and vanilla JS (for fetching data asynchronously).

### 🔨 Build Steps
1. Add `flask` to `requirements.txt` and install it.
2. Create `app.py` — The Flask server.
   - Route `GET /` to render the UI.
   - Route `POST /upload` to handle PDF uploads and trigger `create_vector_store()`.
   - Route `POST /ask` to take a question and trigger `generate_answer()`.
3. Create `templates/index.html` — The frontend UI.
   - We will build a beautiful, modern chat interface.
4. Create `static/style.css` — Custom styling to make it look premium.
   
### ✅ Checkpoint
- Can you load the web UI in your browser?
- Can you successfully upload a new PDF via the web interface?
- Does the chat interface display messages and loading states correctly?
- Do you get answers back from the Gemini backend?

---

## Phase 9: Evaluation & Improvements (Bonus)

Once everything works, we can explore:

| Improvement | What It Does |
|---|---|
| **Multi-PDF support** | Query across multiple documents |
| **Chat memory** | Remember previous questions in conversation |
| **Better chunking** | Semantic chunking instead of fixed size |
| **Re-ranking** | Use a cross-encoder to improve retrieval |
| **Streaming responses** | See the LLM answer word by word |
| **Evaluation metrics** | Measure how good your RAG system is |

---

## Summary: Learning Timeline

| Phase | Concept | Time Estimate |
|---|---|---|
| Phase 0 | Setup & Tools | 30 min |
| Phase 1 | Document Loading | 1 hour |
| Phase 2 | Chunking | 1-2 hours |
| Phase 3 | Embeddings | 2-3 hours (most important!) |
| Phase 4 | Vector Store | 1-2 hours |
| Phase 5 | Retrieval | 1 hour |
| Phase 6 | Generation | 1-2 hours |
| Phase 7 | Full Pipeline | 1-2 hours |
| Phase 8 | Web UI | 1-2 hours |
| Phase 9 | Improvements | Ongoing |

> [!IMPORTANT]
> ### Before We Start — Your Decisions:
> 1. **Which LLM** do you want to use? (Gemini recommended for free tier)
> 2. **Do you have an API key?** If not, I'll guide you to get one.
> 3. **Which PDF** will you use for testing?
> 4. **Does this roadmap structure work for you?** Want to add/remove anything?
>
> Reply with your choices and we'll begin Phase 0! 🚀

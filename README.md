# 📄 RAG PDF Chatbot — Talk to your Documents

Live Demo: [rag-chatbot-psi-one.vercel.app](https://rag-chatbot-psi-one.vercel.app/)

A Retrieval-Augmented Generation (RAG) application built to help you interact with your PDF documents. Instead of reading through hundreds of pages, you can simply upload your files and start asking questions. The bot uses semantic search to find relevant context and provides accurate, sourced answers.

---

### 🚀 How it works
1. **Upload**: You upload one or more PDF research papers or documents.
2. **Ingest**: The system chunks the text and generates vector embeddings using **Google Gemini**.
3. **Store**: These embeddings are stored in a local **ChromaDB** vector store.
4. **Chat**: When you ask a question, the system retrieves the most relevant snippets and feeds them into the Gemini 1.5 Flash model to generate a precise response.

---

### 🛠️ Tech Stack
- **Backend**: Flask (Python)
- **AI Framework**: LangChain
- **LLM & Embeddings**: Google Gemini (via `langchain-google-genai`)
- **Vector DB**: ChromaDB
- **Frontend**: Vanilla HTML/CSS/JS (Clean, modern dark-themed UI)

---

### 💻 Local Setup

If you want to run this locally, follow these steps:

1. **Clone the repo**
   ```bash
   git clone https://github.com/thesonukumar/rag_chatbot.git
   cd rag_chatbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables**
   Create a `.env` file in the root directory and add your Google API Key:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

5. **Run the app**
   ```bash
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5000`.

---

### 📝 Key Features
- **Multi-PDF Support**: Upload several files at once; the bot understands context across all of them.
- **Smart Retrieval**: Uses vector similarity search to find the exact paragraph you need.
- **Vercel Ready**: Optimized for serverless deployment with SQLite patches and `/tmp` directory handling.
- **Responsive UI**: A minimal, sidebar-based layout that works great on all screens.

---

### 🛠️ Deployment
This project is configured to be deployed on **Vercel**. It includes a `vercel.json` and a specific patch in `app.py` to handle ChromaDB's SQLite dependency in serverless environments.

---

*Built with ❤️ for better document analysis.*

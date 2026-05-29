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
### 🛠️ Deployment (Render.com)

This project is fully ready to be deployed on **Render.com**. 

1. Push your code to a GitHub repository.
2. Go to [Render.com](https://render.com/) and create a new **Web Service**.
3. Connect your GitHub repository.
4. Set the following configurations:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **Advanced** and add your Environment Variables:
   - `GOOGLE_API_KEY` = *your_google_api_key*
   - `PINECONE_API_KEY` = *your_pinecone_api_key*
6. Click **Create Web Service**. 

Render will automatically build and deploy your Chatbot!

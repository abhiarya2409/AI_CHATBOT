# 🤖 AI Chatbot with RAG + Agent (Gemini)
A conversational AI chatbot that can:
- Answer questions from uploaded documents (RAG)
- Use external tools like web search & calculator
- Maintain conversation memory
- Stream responses in real-time

Built as part of an AI Developer Technical Assessment.

## 🚀 Features

### ✅ Chat API
- Streaming responses using FastAPI
- Maintains conversation history (memory)
- System prompt for assistant behavior

### ✅ RAG (Document Q&A)
- Upload PDF/text documents
- Chunking + embeddings using Gemini
- FAISS vector database for retrieval
- Context-aware answers
- Fallback if answer not found

### ✅ Agent with Tools
- Tool 1: Web Search (DuckDuckGo)
- Tool 2: Calculator
- LLM decides when to use tools
- Tool results integrated into final response

### ✅ UI
- Simple Streamlit chat interface
- Real-time streaming responses


## ⚙️ Tech Stack

- **Language:** Python
- **LLM:** Google Gemini
- **Framework:** FastAPI
- **Vector DB:** FAISS
- **Agent Framework:** LangChain
- **UI:** Streamlit

---

## 📁 Project Structure


ai-chatbot/
│── main.py # FastAPI backend (chat + streaming)
│── rag.py # Document processing & retrieval
│── agent.py # Agent with tools
│── tools.py # Web search + calculator
│── memory.py # Conversation memory
│── ui.py # Streamlit frontend
│── requirements.txt
│── .env.example


---

## 🔐 Environment Variables

Create a `.env` file:
GOOGLE_API_KEY=your_api_key_here

## 📦 Installation

git clone <repo-url>
cd ai-chatbot

pip install -r requirements.txt
▶️ Running the Application
1️⃣ Start FastAPI backend
uvicorn main:app --reload

Backend runs at:

http://localhost:8000
2️⃣ Start Streamlit UI
streamlit run ui.py
📤 API Endpoints
Upload Document
POST /upload

Upload a .txt or .pdf file.

Chat (Streaming)
GET /chat?query=your_question

Returns streaming response.

🧪 Example Usage
Upload a document
Ask:
"What is this document about?" → RAG response
Ask:
"What is 25 * 67?" → Calculator tool
Ask:
"Latest news about AI?" → Web search tool"# AI_CHATBOT" 

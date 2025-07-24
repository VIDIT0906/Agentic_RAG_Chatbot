# 🧠 Agentic RAG Chatbot for Multi-Format Document QA using MCP

A lightweight, agent-based Retrieval-Augmented Generation (RAG) chatbot designed to answer user questions from uploaded documents of various formats — powered by **Model Context Protocol (MCP)** and **Streamlit**.
Supports **PDF, DOCX, PPTX, CSV, TXT, Markdown** files. Built with modular agents and vector search using **ChromaDB**.

---

## 🚀 Features

✅ Upload & parse diverse document formats
✅ Agent-based design: Ingestion, Retrieval, LLM Response
✅ MCP-style structured message passing (in-memory)
✅ Uses Open Source LLMs via **Groq**
✅ Clean multi-turn Q\&A interface with **Streamlit**
✅ Pluggable vector store using **ChromaDB**

---

## 📁 Project Structure

```
Agentic-RAG-Chatbot/
│
├── app.py                         # Streamlit UI
│
├── agents/
│   ├── ingestion_agent.py        # Parses & preprocesses uploaded documents
│   ├── retrieval_agent.py        # Handles embedding + retrieval via Chroma
│   └── llm_response_agent.py     # Queries the LLM using retrieved context
│
├── utils/
│   ├── doc_parser.py             # Handles parsing for PDF, DOCX, CSV, etc.
│   └── vectorstore_utils.py      # Embedding & ChromaDB logic
│
├── mcp/
│   ├── mcp_models.py             # Pydantic-based MCP message structure
│   └── mcp_queue.py              # In-memory queue for agent messaging
│
├── data/
│   ├── uploads/                  # Raw uploaded files
│   └── parsed/                   # Cleaned & extracted text chunks
│
├── chroma_data/                  # Vector store (auto-created on add)
│
├── .env                          # API keys (Groq)
├── requirements.txt              # All Python dependencies
└── README.md                     # This file
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/Agentic-RAG-Chatbot.git
cd Agentic-RAG-Chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\\Scripts\\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up `.env`

Create a `.env` file in the root directory with your keys:

```env
GROQ_API_KEY=your-groq-key
LLM_MODEL=llama3-8b-8192
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Open the link in your browser and:

* Upload a document
* Ask a question like “What is this report about?”
* See LLM-generated answers with source context

---

## 💡 How It Works

1. **User Uploads Documents** → Handled by `IngestionAgent`
2. **IngestionAgent** → Parses content & chunks it
3. **Chunks → ChromaDB** for semantic indexing
4. **User Asks a Question** → Routed via `RetrievalAgent`
5. **RetrievalAgent** → Gets top-matching chunks
6. **LLMResponseAgent** → Uses chunks + user question → Calls LLM
7. **Final Answer** → Shown in UI with full chat history

All communication follows a structured **MCP message protocol** using:

```json
{
  "sender": "RetrievalAgent",
  "receiver": "LLMResponseAgent",
  "type": "RETRIEVAL_RESULT",
  "trace_id": "abc-123",
  "payload": {
    "retrieved_context": ["chunk 1", "chunk 2"],
    "query": "What are the Q1 results?"
  }
}
```

---

## 📦 Supported File Types

* ✅ PDF
* ✅ Word (.docx)
* ✅ PowerPoint (.pptx)
* ✅ CSV
* ✅ Plain Text (.txt)
* ✅ Markdown (.md)

---

## 🧪 Sample Questions

After uploading a document, try asking:

* “Summarize the main points.”
* “What is the timeline mentioned?”
* “List key insights.”
* “Who is responsible for delivery?”

---

## 📸 Demo

Here’s how the Agentic RAG Chatbot looks in action:

![image](https://github.com/user-attachments/assets/36bf8866-a650-444f-86a9-b5465f7ef1b9)

---

## 📌 Future Improvements

* 🧠 LangGraph-based agent control
* 🔁 Pub/Sub or REST-based MCP
* 🧾 Chat history saving
* 🔐 User authentication
* 📊 Metadata-aware chunking

---

## 🙌 Credits

* Built using **Python**, **Streamlit**, **Langchain-style agents**, **ChromaDB**, **Groq**
* MCP inspired by structured agent protocols

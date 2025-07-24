import streamlit as st
import os
from uuid import uuid4
from mcp.mcp_models import MCPMessage
from mcp.mcp_queue import mcp_queue
from agents.ingestion_agent import run_ingestion_agent
from agents.retrieval_agent import run_retrieval_agent
from agents.llm_response_agent import run_llm_response_agent

# Create necessary directories
os.makedirs("data/uploads", exist_ok=True)
os.makedirs("data/parsed", exist_ok=True)
os.makedirs("chroma_data", exist_ok=True)

# Set up Streamlit page
st.set_page_config(page_title="Document QA Chatbot", layout="wide")
st.title("📄 Multi-Format Document QA Chatbot")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# Sidebar file uploader
with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, PPTX, CSV, TXT, or MD files", 
        accept_multiple_files=True,
        type=["pdf", "docx", "pptx", "csv", "txt", "md"]
    )

    if uploaded_files:
        for file in uploaded_files:
            if file.name not in [f.name for f in st.session_state.uploaded_files]:
                # Save the file
                file_path = os.path.join("data/uploads", file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())

                # Process the file through the ingestion pipeline
                trace_id = str(uuid4())
                message = MCPMessage(
                    sender="UI",
                    receiver="IngestionAgent",
                    type="NEW_DOCUMENT",
                    trace_id=trace_id,
                    payload={"file_path": file_path}
                )
                mcp_queue.send(message)
                run_ingestion_agent(message)
                run_retrieval_agent()

                st.session_state.uploaded_files.append(file)
                st.success(f"File {file.name} processed successfully!")

# Chat interface
st.header("Ask questions about your documents")

# Display chat history
if st.session_state.chat_history:
    st.markdown("### 💬 Conversation History")
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**🧑 You:** {msg['content']}")
        else:
            st.markdown(f"**🤖 Bot:** {msg['content']}")

# Query input
query = st.text_input("Ask a question about your documents:", key="query_input")
if query and query != st.session_state.last_query:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": query})
    st.session_state.last_query = query  # Prevent repeat

    # Process query through the RAG pipeline
    trace_id = str(uuid4())
    message = MCPMessage(
        sender="UI",
        receiver="RetrievalAgent",
        type="QUERY",
        trace_id=trace_id,
        payload={"query": query, "chunks": []}
    )
    mcp_queue.send(message)
    run_retrieval_agent()
    response = run_llm_response_agent()

    # Add AI response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Force a rerun to update chat display
    st.rerun()

# Reset chat button
if st.button("🔄 Reset Chat"):
    st.session_state.chat_history = []
    st.session_state.last_query = ""
    st.rerun()

if not st.session_state.uploaded_files:
    st.info("Upload at least one document to begin asking questions.")

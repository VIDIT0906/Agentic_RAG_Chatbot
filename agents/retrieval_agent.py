from mcp.mcp_models import MCPMessage
from mcp.mcp_queue import mcp_queue
from utils.vectorstore_utils import add_to_vectorstore, query_vectorstore

def run_retrieval_agent():
    msg = mcp_queue.receive("RetrievalAgent")
    if msg:
        chunks = msg.payload.get("chunks", [])

        # If chunks are provided (e.g. during ingestion), add to vector store
        if chunks:
            add_to_vectorstore(chunks)

        # If query exists, perform retrieval
        query = msg.payload.get("query", None)
        if query:
            top_chunks = query_vectorstore(query)

            response = MCPMessage(
                sender="RetrievalAgent",
                receiver="LLMResponseAgent",
                type="RETRIEVAL_RESULT",
                trace_id=msg.trace_id,
                payload={"retrieved_context": top_chunks, "query": query}
            )
            mcp_queue.send(response)
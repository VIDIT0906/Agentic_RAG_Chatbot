from mcp.mcp_models import MCPMessage
from mcp.mcp_queue import mcp_queue
from utils.file_loader import load_text
from utils.text_splitter import simple_split

def run_ingestion_agent(message: MCPMessage):
    file_path = message.payload["file_path"]
    trace_id = message.trace_id
    full_text = load_text(file_path)
    chunks = simple_split(full_text)

    response = MCPMessage(
        sender="IngestionAgent",
        receiver="RetrievalAgent",
        type="TEXT_CHUNKS",
        trace_id=trace_id,
        payload={"chunks": chunks}
    )
    mcp_queue.send(response)
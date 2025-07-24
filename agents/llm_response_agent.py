from mcp.mcp_models import MCPMessage
from mcp.mcp_queue import mcp_queue
from groq import Groq
from config.settings import GROQ_API_KEY, LLM_MODEL

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def run_llm_response_agent():
    msg = mcp_queue.receive("LLMResponseAgent")
    if msg:
        context = "\n".join(msg.payload["retrieved_context"])
        query = msg.payload["query"]
        prompt = f"Answer the question based on the following context:\n\n{context}\n\nQ: {query}\nA:"

        # Use Groq API to generate response
        response = client.chat.completions.create(
            model=LLM_MODEL,  # This will be llama3-8b-8192 from .env
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
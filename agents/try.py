from mcp.mcp_models import MCPMessage
from mcp.mcp_queue import mcp_queue
import google.generativeai as genai
from config.settings import GEMINI_API_KEY, LLM_MODEL

# Configure the Gemini client with the API key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Generative Model
# The LLM_MODEL variable from your settings should be a compatible Gemini model name,
# such as 'gemini-1.5-flash', 'gemini-pro', etc.
model = genai.GenerativeModel(LLM_MODEL)

def run_llm_response_agent():
    """
    Receives a message, builds a prompt, and uses the Gemini API to generate a response.
    """
    msg = mcp_queue.receive("LLMResponseAgent")
    if msg:
        context = "\n".join(msg.payload["retrieved_context"])
        query = msg.payload["query"]
        prompt = f"Answer the question based on the following context:\n\n{context}\n\nQ: {query}\nA:"

        # Use Gemini API to generate the response
        response = model.generate_content(prompt)

        # Return the generated text content from the response
        return response.text
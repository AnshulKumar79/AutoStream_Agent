## AutoStream AI Agent - ServiceHive ML Intern Assignment

This repository contains the source code for the "Social-to-Lead Agentic Workflow" assignment. It features a conversational AI agent for AutoStream (a SaaS video editing tool) that can handle product queries, detect high-intent users, and capture leads seamlessly.

## How to Run the Project Locally

1. **Clone the repository:**
   ```bash
   git clone <github-repo-url>
   cd AutoStream_Agent

2. **Set up a Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On Mac/Linux:
    source venv/bin/activate

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt

4. **Environment variables:**
    Create a .env file in the root directory and add your Google Gemini API Key:
    GEMINI_API_KEY=your_api_key_here

5. **Run the Agent:**
    ```bash
    python main.py

# NOTE: Successfully captured leads will automatically be saved to a 'leads.csv' file in the root directory, which is git-ignored for data privacy.

## LLM SELECTION:
The assignment document requested the use of Gemini 1.5 Flash. However, since Google has recently deprecated the standard 1.5 API endpoints (resulting in a 404 Not Found error on the default string), I proactively upgraded the model to **gemini-2.5-flash**. This ensures the application runs flawlessly and utilizes the currently supported and active Google AI infrastructure.




## Architecture Explanation
**Why LangGraph?**
I chose LangGraph over basic LangChain or AutoGen because agentic workflows fundamentally require cyclic execution and robust state management. While standard chains represent directed acyclic graphs (DAGs), LangGraph allows the agent to iteratively loop between reasoning (LLM) and acting (Tool Execution). This is critical for our use case: if the agent triggers the lead capture process but realizes a detail (like 'Email') is missing, LangGraph easily routes it back to the chatbot node to prompt the user again, rather than failing or hallucinating.

**State Management:**
State is managed using LangGraph's StateGraph and a TypedDict structure. The memory utilizes the add_messages reducer to append new conversation turns continuously. To retain memory across multiple conversation turns (5-6+), I implemented LangGraph's MemorySaver checkpointer. By assigning a unique thread_id to the session configuration, the checkpointer seamlessly persists the chat history in memory, ensuring the agent always remembers previously collected lead details like the user's name or platform without asking twice.




## WhatsApp Webhook Integration
>>>To integrate this agent with WhatsApp, I would deploy the application using FastAPI and connect it to the Meta WhatsApp Cloud API.

1.**Webhook Setup**: I would create a /webhook POST endpoint in FastAPI. When a user messages the WhatsApp number, Meta sends a JSON payload containing the message and sender's phone number to this endpoint.

2. **State Context via Phone Number**: I would map the user's WhatsApp phone number directly to LangGraph's thread_id. This ensures that when the LangGraph agent is invoked, it retrieves the exact conversation memory for that specific user.

3. **Execution & Reply**: The agent processes the message, the LangGraph executes the necessary nodes, and the final response string is extracted.

4. **Sending the Message**: Finally, I would use the Meta Graph API (via a POST request with the WhatsApp Access Token) to send the generated response back to the user's WhatsApp interface.

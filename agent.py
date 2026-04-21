import json
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from state import AgentState
from tools import mock_lead_capture




#Loading the API key.
load_dotenv()


#Loading the knowledge base from the JSON file and converting it to a string for the system prompt.
with open("knowledge_base.json", "r") as f:
    kb_data = json.load(f)
    kb_string = json.dumps(kb_data, indent=2)

#prompt_engineering.
#System Prompt(giving instructions to the agent and providing the knowledge base).
SYSTEM_PROMPT = f"""You are a helpful AI sales agent for AutoStream.
AutoStream provides automated video editing tools for content creators.

Here is the exact product and pricing information you must use (DO NOT make up prices):
{kb_string}

Your workflow:
1. Greet casually if the user says Hi.
2. Answer product queries based strictly on the knowledge base.
3. INTENT DETECTION: If the user shows high intent (e.g., wants to buy, sign up, start a trial), you must collect their:
   - Name
   - Email
   - Creator Platform (e.g., YouTube, Instagram)
4. Do NOT call the mock_lead_capture tool until you have collected ALL THREE details. Ask for missing details conversationally.
"""




#Initializing the Gemini LLM and binding the required tool.
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
tools_list = [mock_lead_capture]
llm_with_tools = llm.bind_tools(tools_list)



#Chatbot Node function.
def chatbot(state: AgentState):
    messages = state["messages"]
    #Ensuring that the System Prompt is always the first message
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}



#Building the LangGraph.
graph_builder = StateGraph(AgentState)

#Adding nodes to the graph structure.
graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools_list)
graph_builder.add_node("tools", tool_node)



#Adding the edges and conditional edges to the graph structure(defining the flow).
graph_builder.add_edge(START, "chatbot")
#Checking the tools_condition after every response from the chatbot to see if the agent should call the tool or not based on the user's intent and the information collected so far.
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")



#Compiling the graph with memory-saver(checkpointer) to save around 5-6 conversations.
memory = MemorySaver()
agent_app = graph_builder.compile(checkpointer=memory)
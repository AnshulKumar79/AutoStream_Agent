from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    #add_messages is just adding the new messages to the existing messages list in the state.
    messages: Annotated[list, add_messages]
#MAIN_CHAT_INTERFACE


from agent import agent_app
from langchain_core.messages import HumanMessage

def run_chat():
    print("AutoStream Agent is Ready! (Type 'quit' or 'exit' to stop)\n")
    
    #Thread ID is for saving the specific chat history.
    config = {"configurable": {"thread_id": "1"}}
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
            
        #Passing user message to the agent and getting the response.
        events = agent_app.stream(
            {"messages": [HumanMessage(content=user_input)]}, 
            config=config, 
            stream_mode="values"
        )
        
        #Printing the agent's response in real-time as it comes in.
        for event in events:
            last_message = event["messages"][-1]
            #Only print if the last message is from the AI.
            if last_message.type == "ai" and last_message.content:
                content= last_message.content
                clean_text= ""

                #on getting formatted response from the LLM.
                if isinstance(content, list):
                    clean_text = "".join([item.get("text", "") for item in content if isinstance(item, dict) and "text" in item])
                else:
                    #if getting a normal string.
                    clean_text = content
                

                if clean_text.strip():
                    print(f"Agent: {clean_text.strip()}")

if __name__ == "__main__":
    run_chat()
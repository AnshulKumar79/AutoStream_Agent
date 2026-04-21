from langchain_core.tools import tool

@tool
def mock_lead_capture(name: str, email: str, platform: str) -> str:
    """
    Call this tool ONLY when the user is highly interested AND you have successfully 
    collected ALL THREE details: Name, Email and Creator Platform.
    Do NOT call this tool if any of these 3 details are missing.
    """
    print("\n" + "="*55)
    print(f"MOCK BACKEND TRIGGERED: LEAD CAPTURED!!!")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Platform: {platform}")
    print("="*55 + "\n")
    
    return "Tool executed successfully. Thank the user and politely end the conversation."
import csv
import os
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



    #for saving the captured leads in a local CSV file.
    file_name = "leads.csv"
    file_exists = os.path.isfile(file_name)
    

    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        #Writing the header row if the file is being created for the first time.
        if not file_exists:
            writer.writerow(['Name', 'Email', 'Platform'])
            
        #Saving the lead information.
        writer.writerow([name, email, platform])
    
    return "Tool executed successfully. Data saved to CSV. Thank the user and politely end the conversation."
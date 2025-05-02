

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool,ToolContext

def greet_lead(lead_id: str, lead_name: str, tool_context: ToolContext):
    state = tool_context.state

    try:
        state["lead"] = {
            "id": lead_id.strip(),
            "name": lead_name.strip(),
            "status": "awaiting_consent",
            "answers": {},
            "q_index": 0
        }

        return {
            "message": f"Hey {lead_name.strip()} of ID {lead_id.strip()}, thank you for filling out the form. I'd like to gather some information from you. Is that okay?"
        }

    except Exception as e:
        print("Lead parsing failed:", e)
        return {"message": "Something went wrong. Please try again."}








import csv
import os

# -----------------------------
# CSV Saving Logic
# -----------------------------
def save_lead_to_csv(lead_id, lead_name, answers):
    file_path = "leads.csv"
    file_exists = os.path.isfile(file_path)

    try:
        with open(file_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["lead_id", "name", "age", "country", "interest", "status"])
            writer.writerow([
                lead_id,
                lead_name,
                answers.get("age", ""),
                answers.get("country", ""),
                answers.get("interest", ""),
                "secured"
            ])
        print(f"[✔] Lead saved: {lead_id} - {lead_name}")
    except Exception as e:
        print("❌ Error saving to CSV:", e)


# -----------------------------
# Consent Function
def handle_consent(consent: str, tool_context: ToolContext):
    state = tool_context.state
    lead = state.get("lead")

    if not lead:
        return {"message": "Please submit the form first."}

    consent = consent.strip().lower()
    print("Consent received:", consent)

    if consent in ("yes", "y"):
        lead["status"] = "collecting_info"
        lead["q_index"] = 0
        lead["answers"] = {}
        state["lead"] = lead  # ✅ Save updated lead to state
        return {"message": "Great! First: What is your age?"}

    elif consent in ("no", "n"):
        lead["status"] = "no_response"
        state["lead"] = lead
        return {"message": "Alright—no problem. Have a great day!"}

    return {"message": "Please answer 'yes' or 'no'."}


# -----------------------------
# Info Collection Function
# -----------------------------
def collect_info(answer: str, tool_context: ToolContext):
    state = tool_context.state
    lead = state.get("lead")

    if not lead or lead.get("status") != "collecting_info":
        return {"message": "Please start with the form and give consent first."}

    questions = [
        "What is your age?",
        "Which country are you from?",
        "What product or service are you interested in?"
    ]
    keys = ["age", "country", "interest"]

    idx = lead.get("q_index", 0)
    answers = lead.get("answers", {})

    if idx < len(keys):
            answers[keys[idx]] = answer.strip()
            lead["answers"] = answers
            lead["q_index"] = idx + 1

            # ✅ Save the updated lead back into the state
            state["lead"] = lead

            if idx + 1 < len(questions):
                return {"message": questions[idx + 1]}
            else:
                print(f"Calling save_lead_to_csv with ID: {lead['id']}, Name: {lead['name']}, Answers: {answers}")

                save_lead_to_csv(lead["id"], lead["name"], answers)
                lead["status"] = "secured"
                state["lead"] = lead  # ✅ Update state again after setting status
                return {"message": "Thank you for your cooperation! We've saved your information."}





agent = LlmAgent(
    model="gemini-1.5-flash",
    name="sales_agent",
    description="Greets a user after form submission.",
    instruction="""
When the message starts with FORM_SUBMIT:<lead_id>:<lead_name>, call the greet_lead tool.

1.It will extract the name and ID from the message and send a personalized greeting.
Include the original form submission in your response.
2. If the user replies with 'yes' or 'no', call the handle_consent(consent=...) tool. 
   - If 'yes', proceed to the questions.
   - If 'no', politely end the conversation and mark the lead as 'no_response'.

3. Once the user consents, ask the following questions one by one using the collect_info(answer=...) tool:
    collects information and saving to csv
  

4. After collecting all three answers, call save_lead_to_csv to store the data in leads.csv with these columns:
   [lead_id, name, age, country, interest, status]
   - Set the status to "secured" once the data is complete.

Only call one tool per message. Use the tools exactly as described above.
If the input doesn't match a form submission or a relevant reply, gently guide the user to use the form to begin.
""",
    tools=[
        FunctionTool(func=greet_lead),
        FunctionTool(func=handle_consent),
        FunctionTool(func=collect_info)]

)





# from google.adk.sessions import InMemorySessionService, Session

# # Create a simple session to examine its properties
# temp_service = InMemorySessionService()
# example_session: Session = temp_service.create_session(
#     app_name="my_app",
#     user_id="example_user",
#     state={"initial_key": "initial_value"} # State can be initialized
# )

# print(f"--- Examining Session Properties ---")
# print(f"ID (`id`):                {example_session.id}")
# print(f"Application Name (`app_name`): {example_session.app_name}")
# print(f"User ID (`user_id`):         {example_session.user_id}")
# print(f"State (`state`):           {example_session.state}") # Note: Only shows initial state here
# print(f"Events (`events`):         {example_session.events}") # Initially empty
# print(f"Last Update (`last_update_time`): {example_session.last_update_time:.2f}")
# print(f"---------------------------------")
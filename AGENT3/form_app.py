# import streamlit as st
# import requests

# # Constants
# ADK_API_URL = "http://localhost:8000"
# AGENT_ID = "sales_agent"

# # Set page configuration
# st.set_page_config(page_title="Sales Agent", page_icon="🤖", layout="wide")

# # Session State initialization
# if "session_id" not in st.session_state:
#     st.session_state.session_id = None
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# st.title("Sales Agent Interaction 🤖📝")

# # Sidebar Form to Submit Lead Information
# st.sidebar.header("Lead Information Form")

# with st.sidebar.form(key="lead_form"):
#     lead_id = st.text_input("Enter Lead ID")
#     lead_name = st.text_input("Enter Lead Name")
#     form_submit = st.form_submit_button(label="Submit Lead Form")

# if st.button("Submit Lead Form"):
#     session_id = f"session-{lead_id}"
#     payload = {
#         "app_name":   AGENT_ID,
#         "user_id":    lead_id,
#         "session_id": session_id,
#         "new_message": {
#             "parts": [
#                 { "text": f"FORM_SUBMIT:{lead_id}:{lead_name}" }
#             ]
#         }
#     }

#     try:
#         response = requests.post(f"{ADK_API_URL}/apps/sales_agent/users/L001/sessions", json=payload)
#         if response.status_code == 200:
#             st.success("✅ Lead form submitted! Now you can chat below.")
#             st.session_state.session_id = None  # Reset session
#             st.session_state.messages = []       # Clear old chat
#         else:
#             st.error(f"❌ Error: {response.status_code} - {response.text}")
#     except Exception as e:
#         st.error(f"❌ Exception: {e}")

# # Chat Interface
# st.subheader("Chat with Sales Agent")

# if st.session_state.messages:
#     for chat in st.session_state.messages:
#         role = chat["role"]
#         content = chat["content"]
#         if role == "user":
#             st.chat_message("user").markdown(content)
#         else:
#             st.chat_message("assistant").markdown(content)

# # Input box for typing messages
# user_input = st.chat_input("Type your message...")

# if user_input:
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     payload = {
#         "agent_id": AGENT_ID,
#         "input": user_input
#     }

#     try:
#         params = {}
#         if st.session_state.session_id:
#             params["session_id"] = st.session_state.session_id

#         response = requests.post(f"{ADK_API_URL}/chat", json=payload, params=params)
#         if response.status_code == 200:
#             data = response.json()
#             agent_reply = data["message"]
#             st.session_state.session_id = data["session_id"]

#             st.session_state.messages.append({"role": "assistant", "content": agent_reply})
#             st.chat_message("assistant").markdown(agent_reply)

#         else:
#             st.error(f"❌ Chat error: {response.status_code} - {response.text}")
#     except Exception as e:
#         st.error(f"❌ Exception during chat: {e}")


# import streamlit as st
# import requests

# ADK_URL    = "http://localhost:8000/run"
# AGENT_NAME = "sales_agent"

# st.title("Lead Form → Sales Agent")

# lead_id   = st.text_input("Lead ID",   "L001")
# lead_name = st.text_input("Lead Name", "Alice")
# if st.button("Submit Form"):
#     session_id = f"session-{lead_id}"
#     payload = {
        
#         "user_id":    lead_id,
#         "session_id": session_id,
        
#     }
#     r = requests.post(ADK_URL, json=payload)
#     if r.status_code == 200:
#         st.success("✅ Sent to agent; check your ADK UI or logs for the greeting.")
#     else:
#         st.error(f"❌ {r.status_code} – {r.text}")



# import streamlit as st
# import requests

# ADK_RUN_URL = "http://localhost:8000/apps/sales_agent/users/L001/sessions"
# AGENT_ID    = "sales_agent"

# st.title("Lead Form → Sales Agent")

# lead_id   = st.text_input("Lead ID"   )
# lead_name = st.text_input("Lead Name")

# if st.button("Submit Lead Form"):
#     session_id = f"session-{lead_id}"
#     payload = {
#     "agent_id": "sales_agent",  # must match Agent(... name="sales_agent")
#     "session_id": session_id,
#     "input": f"FORM_SUBMIT:{lead_id}:{lead_name}"  # simple string, not new_message
# }

#     r = requests.post(ADK_RUN_URL, json=payload)
#     if r.status_code == 200:
#         st.success("✅ Form submitted – check your agent greeting!")
#         st.success(f"{r.text}")
#     else:
#         st.error(f"❌ {r.status_code} – {r.text}")


# import streamlit as st
# import requests

# ADK_BASE = "http://localhost:8000"
# AGENT_ID = "sales_agent"

# st.title("📝 Lead Form → Sales Agent")

# lead_id   = st.text_input("Lead ID",   "L001")
# lead_name = st.text_input("Lead Name", "Alice")

# if st.button("Submit Lead Form"):
#     # 1) Create (or reuse) session
#     session_id = f"session-{lead_id}"
#     sess_url   = f"{ADK_BASE}/apps/{AGENT_ID}/users/{lead_id}/sessions/{session_id}"
#     r1 = requests.post(sess_url, json={})
#     if r1.status_code not in (200, 400):
#         st.error(f"❌ Session creation failed: {r1.status_code} – {r1.text}")
#         st.stop()
#     if r1.status_code == 400 and "Session already exists" in r1.text:
#         st.warning("⚠️ Session already existed; reusing it.")

#     # 2) Trigger the agent by sending the FORM_SUBMIT marker
#     run_url = f"{ADK_BASE}/run"
#     payload = {
#          "app_name":   AGENT_ID,
#          "user_id":    lead_id,
#          "session_id": session_id,
#         "new_message": {
#              "parts": [
#                  { "text": f"FORM_SUBMIT:{lead_id}:{lead_name}" }
#              ]
#          }
#     }
#     st.warning(run_url)
#     r2 = requests.post(run_url, json=payload)
#     if r2.status_code != 200:
#         st.error(f"Agent run failed: {r2.status_code} – {r2.text}")
#         st.stop()
    
    
    # # 3) Display the greeting
    # body     = r2.json()
    # greeting = body["content"]["parts"][0]["output"]
    # st.success(f"🤖 Agent says: {greeting}")
# import streamlit as st
# import requests

# ADK_BASE_URL = "http://localhost:8000"
# AGENT_ID     = "sales_agent"

# st.title("📝 Lead Form → Sales Agent")

# lead_id   = st.text_input("Lead ID",   "L001")
# lead_name = st.text_input("Lead Name", "Alice")

# if st.button("Submit Lead Form"):
#     session_id = f"session-{lead_id}"

#     # 1️⃣ Create session (or reuse if already exists)
#     session_url = f"{ADK_BASE_URL}/apps/{AGENT_ID}/users/{lead_id}/sessions/{session_id}"
#     r1 = requests.post(session_url, json={})
#     if r1.status_code not in (200, 400):
#         st.error(f"❌ Session creation failed: {r1.status_code} – {r1.text}")
#         st.stop()

#     # 2️⃣ Trigger the agent with FORM_SUBMIT input
#     run_url = f"{ADK_BASE_URL}/run"
#     payload = {
#         "agent_id": AGENT_ID,
#         "session_id": session_id,
#         "input": f"FORM_SUBMIT:{lead_id}:{lead_name}"
#     }
#     r2 = requests.post(run_url, json=payload)
#     if r2.status_code != 200:
#         st.error(f"❌ Agent run failed: {r2.status_code} – {r2.text}")
#         st.stop()

#     # 3️⃣ Show the agent's greeting
#     body = r2.json()
#     st.write("🧠 Raw response:", body)
#     greeting = body[0]["content"]["parts"][0]["output"]
#     st.success(f"🤖 Agent says: {greeting}")
import streamlit as st
import requests

ADK_BASE_URL = "http://localhost:8000"
AGENT_ID     = "sales_agent"

st.title("📝  Sales Agent")

lead_id   = st.text_input("Lead ID",   "L001")
lead_name = st.text_input("Lead Name", "Alice")

if st.button("Submit Lead Form"):
    session_id = f"session-{lead_id}"

    # 1️⃣ Create session
    session_url = f"{ADK_BASE_URL}/apps/{AGENT_ID}/users/{lead_id}/sessions/{session_id}"
    r1 = requests.post(session_url, json={})
    if r1.status_code not in (200, 400):
        st.error(f"❌ Session creation failed: {r1.status_code} – {r1.text}")
        st.stop()

    # 2️⃣ Run the agent
    run_url = f"{ADK_BASE_URL}/run"
    payload = {
        "app_name":   AGENT_ID,
        "user_id":    lead_id,
        "session_id": session_id,
        "new_message": {
            "parts": [
                { "text": f"FORM_SUBMIT:{lead_id}:{lead_name}" }
            ]
        }
    }
    r2 = requests.post(run_url, json=payload)
    if r2.status_code != 200:
        st.error(f"❌ Agent run failed: {r2.status_code} – {r2.text}")
        st.stop()

    # 3️⃣ Show the greeting
    body = r2.json()
    st.write("📤 Sent to /run:", payload)
    st.write("🧠 Raw agent response:", body)
    greeting = body[-1]["content"]["parts"][0]["text"]#issy tww nahi utha raha 
    st.success(f"🤖 Agent says: {greeting}")

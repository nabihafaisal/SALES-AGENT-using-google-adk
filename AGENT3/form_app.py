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

# 🤖 Conversational Lead Agent using Google ADK

This project builds a multi-turn conversational **sales agent** using **Google's Agent Development Kit (ADK)** and `LlmAgent`. It handles form submissions, collects user information step-by-step, stores leads in a CSV, and follows up with inactive users.

---

## ✨ Features

- ✅ Personalized greeting based on form submission.
- 🔒 Consent verification before proceeding.
- 📋 Asks a series of questions (age, country, interest).
- 💾 Automatically saves leads to a CSV file.
- ⏳ Sends follow-up messages if user becomes inactive for 20 seconds.
- 🧠 Maintains contextual state for concurrent user sessions.

---

## 🛠️ Setup Instructions

### 📁 Clone the Repository
```bash
[git clone https://github.com/yourusername/lead-agent-adk.git](https://github.com/nabihafaisal/SALES-AGENT-using-google-adk.git)

```

### 🐍 Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

> ✅ Make sure you have access to **Google's Agent Development Kit (ADK)** and Python 3.8+ installed.

---

## ▶️ Running the Agent

In your Python environment (or integrated with a frontend like Streamlit), run the agent:

```python
streamlit run form_app.py
adk web
```

---

## 📘 Usage Guide

### 📝 Start with Form Submission
Send a message in the format:

```
FORM_SUBMIT:<lead_id>:<lead_name>
```

🔁 The agent will greet the user and ask for consent.

---

### 🔐 Consent Phase

The user must respond with:
- `yes` → proceeds to data collection.
- `no` → ends the conversation politely.

---

### 💬 Info Collection Phase

If consent is given, the agent asks:
1. What is your age?
2. Which country are you from?
3. What product or service are you interested in?

Each answer advances the conversation.

---

### 💾 Lead Storage

After collecting all 3 answers, the agent writes to `leads.csv` in this format:

| lead_id | name | age | country | interest | status   |
|---------|------|-----|---------|----------|----------|
| 001     | John | 28  | Canada  | Software | secured  |

---

### ⏰ Inactivity Follow-Up

If the user stops responding for **20 seconds**, the agent sends:

> "Just checking in to see if you're still interested. Let me know when you're ready to continue."

---

## 📐 Design Decisions

### 1. 🧩 Modular Tool Functions
Each task (greeting, consent, info collection) is encapsulated in its own function using `FunctionTool` for clarity and separation of concerns.

### 2. 🧠 State-Based Progress Tracking
State is maintained inside `tool_context.state["lead"]` to ensure user-specific conversation flow and persistent answers.

### 3. ⏳ Simulated Follow-Up Logic
Instead of waiting 24 hours, inactivity is simulated after 20 seconds to streamline testing.

```python
if elapsed > 20:
    return {"message": "Just checking in..."}
```

### 4. 🧪 Easy Debugging
All state transitions and file write actions are logged to the console for traceability.

---

## 🧪 Testing Tips

- Test multiple sessions using separate tabs or incognito windows.
- Wait for 20 seconds mid-conversation to trigger follow-up.
- Open `leads.csv` to confirm data saving.

---

## 📂 Project Structure

```
.
├── agent3.py       # Contains the agent logic and tool functions
├── leads.csv                # Output file with collected leads
├── requirements.txt
└── README.md                # You're reading it!
```



## 🙋‍♀️ Author

**Nabiha Faisal**  
📧nabihfaisal@gmail.com.com  
🔗 [LinkedIn](https://www.linkedin.com/in/nabihafaisal) · [GitHub](https://github.com/nabihafaisal)

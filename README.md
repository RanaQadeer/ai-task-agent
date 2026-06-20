# 🤖 AI Task Agent

An autonomous AI agent that thinks, searches, calculates, and solves complex tasks step by step — powered by Groq's ultra-fast LLM inference.

## 🚀 Features
- 🧠 Autonomous reasoning — breaks down complex tasks step by step
- 🔍 Web search — finds real-time information using DuckDuckGo
- 🧮 Calculator — performs mathematical calculations instantly
- 💬 Conversation memory — remembers context across the chat
- 🔍 Transparent thinking — shows its reasoning process live

## 🛠️ Tech Stack
- Python
- Streamlit
- Groq API (llama-3.3-70b-versatile)
- DuckDuckGo Search API
- python-dotenv

## 🧠 What is an AI Agent?
A regular chatbot just answers questions. An AI Agent goes further:
1. **Thinks** about what tools it needs
2. **Acts** by calling those tools (search, calculate, etc.)
3. **Observes** the results
4. **Responds** with a final informed answer

This is the foundation of modern agentic AI systems used by companies like Salesforce, HubSpot, and Google.

## ⚙️ How It Works
1. User gives a task
2. Agent decides if it needs tools
3. If yes — calls search or calculator
4. Combines results into a final answer
5. Shows the full thinking process

## 📦 Installation
```bash
git clone https://github.com/RanaQadeer/ai-task-agent.git
cd ai-task-agent
pip install -r requirements.txt
python -m streamlit run app.py
```

## 🔑 Environment Variables
Create a `.env` file:
GROQ_API_KEY=your-groq-api-key-here
## 💼 Use Cases for Businesses
- Customer support automation
- Research and summarization agent
- Data lookup and calculation workflows
- Internal knowledge base assistant
- Lead qualification agent

## 📊 Example Tasks to Try
- *"Search for the latest AI trends and summarize them"*
- *"What is 15% of 85000 and what is the square root of 144?"*
- *"Find information about Python programming and explain it simply"*

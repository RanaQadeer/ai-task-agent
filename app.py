import streamlit as st
import os
import json
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def search_web(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        results = []
        if data.get("AbstractText"):
            results.append(data["AbstractText"])
        for topic in data.get("RelatedTopics", [])[:3]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append(topic["Text"])
        
        return "\n".join(results) if results else "No results found."
    except:
        return "Search unavailable."

def calculate(expression):
    try:
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Invalid calculation."

def run_agent(user_task, chat_history):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_web",
                "description": "Search the web for current information about any topic",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query"
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Perform mathematical calculations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "The mathematical expression to evaluate"
                        }
                    },
                    "required": ["expression"]
                }
            }
        }
    ]

    messages = [
        {
            "role": "system",
            "content": """You are an intelligent AI agent that helps users complete tasks.
You have access to tools: search_web and calculate.
Think step by step. Use tools when needed to get accurate information.
Always explain what you are doing and why."""
        }
    ]

    for msg in chat_history:
        messages.append(msg)

    messages.append({"role": "user", "content": user_task})

    steps = []

    # Step 1 — Initial thinking
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=1000
    )

    msg = response.choices[0].message

    # Step 2 — Execute tools if needed
    while msg.tool_calls:
        steps.append(f"🔧 **Using tool:** `{msg.tool_calls[0].function.name}`")
        
        tool_results = []
        for tool_call in msg.tool_calls:
            args = json.loads(tool_call.function.arguments)
            
            if tool_call.function.name == "search_web":
                steps.append(f"🔍 **Searching for:** {args['query']}")
                result = search_web(args["query"])
                steps.append(f"📄 **Found:** {result[:200]}...")
            elif tool_call.function.name == "calculate":
                steps.append(f"🧮 **Calculating:** {args['expression']}")
                result = calculate(args["expression"])
                steps.append(f"✅ **Result:** {result}")

            tool_results.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

        messages.append({"role": "assistant", "content": msg.content, "tool_calls": [
            {"id": tc.id, "type": "function", "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
            for tc in msg.tool_calls
        ]})
        messages.extend(tool_results)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=1000
        )
        msg = response.choices[0].message

    final_answer = msg.content
    return final_answer, steps

def main():
    st.set_page_config(page_title="AI Task Agent", page_icon="🤖")
    st.title("🤖 AI Task Agent")
    st.write("Give me any task — I'll think, search, calculate and solve it!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "all_messages" not in st.session_state:
        st.session_state.all_messages = []

    for msg in st.session_state.all_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    task = st.chat_input("Give me a task to complete...")
    if task:
        with st.chat_message("user"):
            st.write(task)

        with st.chat_message("assistant"):
            with st.spinner("🧠 Thinking and working on your task..."):
                answer, steps = run_agent(task, st.session_state.chat_history)

            if steps:
                with st.expander("🔍 See my thinking process"):
                    for step in steps:
                        st.markdown(step)

            st.write(answer)

        st.session_state.chat_history.append({"role": "user", "content": task})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.session_state.all_messages.append({"role": "user", "content": task})
        st.session_state.all_messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()

import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from tools.hr_tool import get_hr_policy
from tools.weather_tool import get_weather
from tools.helpdesk_tool import get_helpdesk_info
import os
from dotenv import load_dotenv
from tools.finance_tool import get_finance_news

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# Define tools
tools = [get_hr_policy, get_weather, get_helpdesk_info,get_finance_news]

# Initialize agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=3,
    agent_kwargs={
        "system_message": """
        You are an assistant that uses tools to answer questions.
        For HR policy queries, use the get_hr_policy tool, if any confidential info requested, refuse to answer.
        For Finance queries, use the get_finance_news tool.
        For helpdesk queries, always convert the user's request into a valid SQL query for the tickets table before calling the get_helpdesk_info tool.
        The tickets table schema is: id (integer), title (text), description (text), status (text), created_at (timestamp).
        
        Example conversions:
        - "List all open tickets" → SELECT * FROM tickets WHERE status = 'open';
        - "Show tickets created after 2025-01-01" → SELECT * FROM tickets WHERE created_at > '2025-01-01';
        - "Laptop requested tickets" → SELECT * FROM tickets WHERE title='laptop';
        
        Only send SQL queries to the tool, not natural language.
        """
    }
)

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="TechBreaker Assistant", page_icon="🤖", layout="wide")

st.title("🤖 Multi-Tool Assistant")
st.write("Ask me about **HR Policies**, **Helpdesk Tickets**, or **Weather**.")

# Chat history container
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous chat
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# Chat input
if prompt := st.chat_input("Ask your question here..."):
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = agent.invoke(prompt)
                answer = response["output"]
            except Exception as e:
                answer = f"Error: {e}"

        st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

# Example queries (clickable as markdown)
st.markdown("### 💡 Example Queries:")
st.markdown("- What is the weather in Delhi?")
st.markdown("- List all open tickets")
st.markdown("- Show tickets created after 2025-01-01")
st.markdown("- What is the HR leave policy?")

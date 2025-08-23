from langchain.tools import tool
from langchain.agents import AgentExecutor, initialize_agent,AgentType
from langchain_openai import ChatOpenAI
from tools.hr_tool import get_hr_policy
from tools.weather_tool import get_weather
from tools.helpdesk_tool import get_helpdesk_info
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools =[get_hr_policy, get_weather,get_helpdesk_info]
agent=initialize_agent(
        tools, 
        llm, 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=3,
        agent_kwargs={
            "system_message": """
            You are an assistant that uses tools to answer questions.
            for HR policy queries, use the get_hr_policy tool, if any confidental info requested, refuse to answer.
            For helpdesk queries, always convert the user's request into a valid SQL query for the tickets table before calling the get_helpdesk_info tool.
            When using the get_helpdesk_info tool, always convert the user's request into a valid SQL query for the tickets table. 
            The tickets table schema is: id (integer), title (text), description (text), status (text), created_at (timestamp).
            Example conversions:
            - "List all open tickets" → SELECT * FROM tickets WHERE status = 'open';
            - "Show tickets created after 2025-01-01 or inserted or generated, use created_dt column to filter data " → SELECT * FROM tickets WHERE created_at > '2025-01-01';
            Only send SQL queries to the tool, not natural language.
            - laptop requested tickets means  -select * from tickets where title='laptop'.
            """
        }
        )

agent.invoke("What is the weather in delhi?")


# agent.invoke("what is my leave policy? and also get me list of all open tickets")
# agent.invoke("what is my friend salary?")
# agent.invoke("list all titles of tickets where title contains laptop")

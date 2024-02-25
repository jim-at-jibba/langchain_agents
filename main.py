from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage  # plain system message with no input
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables

load_dotenv()

chat = ChatOpenAI()

tables = list_tables()

prompt = ChatPromptTemplate(  # type: ignore
    messages=[
        SystemMessage(
            content=f"You are an AI that has access to the SQLite database.\n{tables}"
        ),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(
            variable_name="agent_scratchpad"
        ),  # this name (agent_scratchpad) is important, acts like simplified memory
    ],
)

tools = [run_query_tool]
agent = OpenAIFunctionsAgent(llm=chat, prompt=prompt, tools=tools)
agent_executor = AgentExecutor(agent=agent, verbose=True, tools=tools)

agent_executor("How many users have provided a shipping address?")

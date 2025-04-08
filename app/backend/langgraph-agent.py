from typing import Annotated
from langgraphsearchtool import SearchTool
from typing_extensions import TypedDict
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
tool = SearchTool()
llm_seachtool = llm.bind_tools([tool])

class State(TypedDict):
    
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


def chatbot(state: State):
    return {"messages": [llm_seachtool.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")

graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

from IPython.display import Image, display

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass

config = {"configurable": {"thread_id": "1"}}
user_input = "Hi there! Can you use the seach tool and look what is difference between docker and kubernaties ?"

# The config is the **second positional argument** to stream() or invoke()!
events = graph.invoke(
    {"messages": [{"role": "user", "content": user_input}]},
)
for event in events:
    print(event)
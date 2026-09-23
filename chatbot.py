from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
load_dotenv()


model = ChatOpenAI()

class ChatState(TypedDict):

    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):

    messages = state['messages']

    response = model.invoke(messages)

    return {'messages': [response]}

#=========================== creating the graph

graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')

graph.add_edge('chat_node', END)

workflow = graph.compile()

print(workflow)

initial_state= {'messages':[HumanMessage(content='what is the capital of india')]}

response = workflow.invoke(initial_state)

print(response)







     



from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
load_dotenv()

model = ChatOpenAI()

class JokeState(TypedDict):
    topic: str
    joke: str
    explanation:str


def generate_joke(state: JokeState):

    pormpt = f'genarate a joke on the topic {state["topic"]}'

    response = model.invoke(pormpt).content

    return {'joke': response}


def generate_explanation(state: JokeState):

    prompt= f'weire the explanation for the joke - {state["joke"]}'

    response = model.invoke(prompt).content

    return {'explanation': response}


graph = StateGraph(JokeState)

graph.add_node('generate_joke', generate_joke)
graph.add_node('generate_explanation', generate_explanation)

graph.add_edge(START, 'generate_joke')
graph.add_edge('generate_joke', 'generate_explanation')
graph.add_edge('generate_explanation', END)

checkpointer = InMemorySaver()

workflow = graph.compile(checkpointer=checkpointer)

config1 = {"configurable": {"thread_id":"1"}}

response = workflow.invoke({"topic":"pizza"}, config=config1)

print(response)

print("-----------------------------------------")

print(workflow.get_state(config1))

print(workflow.get_state(config1 ))




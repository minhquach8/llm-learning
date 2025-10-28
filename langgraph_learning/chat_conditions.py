from typing import Literal, Optional

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph
from openai import OpenAI
from typing_extensions import TypedDict

load_dotenv()
client = OpenAI()

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    
    is_good: Optional[bool]
    
def chatbot(state: State):
    print("\n\nOpenAI response", state)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages =[
            { "role": "user", "content": state.get("user_query")}
        ]
    )
    
    state["llm_output"] = response.choices[0].message.content
    return state

def evaluate_response(state: State) -> Literal["endnode", "chatbot_gemini"]:
    print("\n\nEvaluating response", state)
    if True:
        return "endnode"

    return "chatbot_gemini"
    
    
def chatbot_gemini(state: State):
    print("\n\nGemini response", state)
    response = client.chat.completions.create(
        model="gemini-2.5",
        messages =[
            { "role": "user", "content": state.get("user_query")}
        ]
    )
    state["llm_output"] = response.choices[0].message.content
    return state


def endnode(state: State):
    print("\n\nEnd Node", state) 
    return state


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "What is Javascript?"}))
print(updated_state)
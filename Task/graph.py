from langgraph.graph import START, END, StateGraph

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, Tool, create_react_agent

import os

from prompts import PROMPT_TEMPLATE
from state import State
from config import CFG

search_fn = TavilySearchResults(max_results=5, 
                             api_key=os.getenv("TAVILY_API_KEY"))

search_tool = Tool(
    name="search_tool",
    func=search_fn.run,
    description="Use for web searches"
)

tools = [search_tool]
tool_names = ", ".join([tool.name for tool in tools])

def make_agent():
     
     llm = ChatOpenAI( 
            model=CFG.model, 
            base_url=CFG.base_url,
            api_key=CFG.API_KEY,
            temperature=0
        )
     
     agent = create_react_agent(llm, tools, PROMPT_TEMPLATE)
     agent_executor = AgentExecutor(agent=agent, 
                                    tools=tools, 
                                    handle_parsing_errors=True,
                                    verbose=True)

     return agent_executor

def model_response(state:State):
    agent_executor = make_agent()
    resp = agent_executor.invoke(
        {
            "input": state["message"],
            "tools": tools,
            "tool_names": tool_names,
            "agent_scratchpad": ""
        }
    )
    
    return {"message": resp["output"]}

def compile_graph():
    workflow = StateGraph(State)
    
    # Adiciona os nós
    workflow.add_node("agent", model_response)

    # Define o fluxo
    workflow.add_edge(START, "agent")
    workflow.add_edge("agent", END)
    return workflow.compile() 
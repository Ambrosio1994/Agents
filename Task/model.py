from langchain_community.tools.tavily_search import TavilySearchResults
import os
from langchain.agents import AgentExecutor, create_react_agent
from config import CFG
from langchain_openai import ChatOpenAI

def make_model(model: str):
    """
    Cria e retorna um objeto ChatOpenAI de acordo com o modelo especificado.

    Parâmetros:
        model (str): Tipo de modelo desejado ("reasoner" ou "chat").

    Retorna:
        ChatOpenAI: Instância configurada de ChatOpenAI conforme o modelo selecionado.
    """
    if model == "reasoner": 
        return ChatOpenAI( 
            model=CFG.model_reasoner, 
            base_url=CFG.base_url,
            api_key=CFG.API_KEY,
        )
    
    elif model == "chat":
        return ChatOpenAI( 
            model=CFG.model_chat, 
            base_url=CFG.base_url,
            api_key=CFG.API_KEY,
        )

def make_agent():
    """
    Cria e retorna um executor de agente (AgentExecutor) configurado
    com as ferramentas necessárias e um LLM para raciocínio.

    Retorna:
        AgentExecutor: O executor configurado para lidar com buscas e processamento.
    """
    search = TavilySearchResults(name="search_tool", 
                                 description="Use para buscar informações na web",
                                 max_results=5, 
                                 api_key=os.getenv("TAVILY_API_KEY") 
                                 )

    llm = make_model(model="reasoner")

    agent = create_react_agent(
        llm=llm, tools=[search], prompt=CFG.prompt 
    )

    agent_executor = AgentExecutor(
        agent=agent, tools=[search], 
        verbose=True, handle_parsing_errors=True  
    )

    return agent_executor
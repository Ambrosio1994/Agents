import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.search_information import deep_search
from utils.prompts import PROMPT_NEWS_SUMMARY
from graph.state import AgentState
import asyncio
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

def news_summary_agent(state: AgentState) -> dict:
    """
    Realiza uma busca profunda combinando resultados de Tavily, DuckDuckGo e Serper.

    A função agrega os resultados de três diferentes mecanismos de busca para oferecer uma visão
    abrangente das informações disponíveis para a query informada.
    """
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-pro-exp-02-05",
        temperature=0,
        api_key=os.getenv("GEMINI_API_KEY"),
    )
    
    agent = PROMPT_NEWS_SUMMARY | llm | StrOutputParser()
    results = asyncio.run(deep_search(state["ativo"]))
    summary = agent.invoke({"input": results})
    print(summary)
    return {"news_summary": summary}
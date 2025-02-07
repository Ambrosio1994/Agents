"""
Agente responsável por processar dados brutos, gerar insights e consolidar análises
técnicas e fundamentais com informações agregadas de buscas na internet.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.analysis import analyze_stock
from utils.prompts import PROMPT_TECHNICAL_ANALYSIS
from graph.state import AgentState

from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

load_dotenv()

def run_data_analysis_agent(state: AgentState) -> dict:
    """
    Executa a análise de dados completa, incluindo coleta de dados, 
    análise técnica e fundamental.
    """
    # Métricas técnicas
    metrics = analyze_stock(state["ativo"])

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-pro-exp-02-05",
        temperature=0,
        api_key=os.getenv("GEMINI_API_KEY"),
    )

    agent = PROMPT_TECHNICAL_ANALYSIS | llm | StrOutputParser()
    result = agent.invoke({"input": metrics})
    return {"technical_analysis": result}
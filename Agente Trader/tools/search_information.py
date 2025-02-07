from langchain_community.tools import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import BaseTool
import http.client
import os
from dotenv import load_dotenv
import urllib.parse
import json
import aiohttp
import asyncio

load_dotenv()

def process_tavily_results(results: list) -> str:
    results = [result["content"] for result in results]
    return results

def process_serper_results(data: str) -> str:
    """Processa os resultados do Serper e retorna um texto formatado"""
    json_data = json.loads(data)
    results = []
    
    # Adiciona resultados orgânicos
    if 'organic' in json_data:
        for item in json_data['organic'][:5]:
            results.append(f"- {item['title']}: {item['snippet']}")
    
    # Adiciona "People Also Ask"
    if 'peopleAlsoAsk' in json_data:
        results.append("\nPerguntas relacionadas:")
        for item in json_data['peopleAlsoAsk'][:5]:
            results.append(f"- {item['question']}: {item['snippet']}")
            
    return "\n".join(results)
   
async def search_tavily_async(query: str) -> str:
    """Versão assíncrona da busca com Tavily"""
    tavily = TavilySearchResults(
        max_results=5,
        api_key=os.getenv("TAVILY_API_KEY")
    )
    return process_tavily_results(await tavily.ainvoke(query))

async def search_duckduckgo_async(query: str) -> str:
    """Versão assíncrona da busca com DuckDuckGo"""
    search = DuckDuckGoSearchRun()
    return await search.arun(query)

async def search_serper_async(query: str) -> str:
    """Versão assíncrona da busca com Serper usando aiohttp"""
    encoded_query = urllib.parse.quote(query)
    headers = {
        'X-API-KEY': os.getenv("SERPER_API_KEY"),
        'Content-Type': 'application/json'
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://google.serper.dev/search?q={encoded_query}",
            headers=headers
        ) as response:
            data = await response.text()
            return process_serper_results(data)

class DeepSearch(BaseTool):
    name: str = "deep_search"
    description: str = "Realiza uma busca profunda combinando resultados de Tavily, DuckDuckGo e Serper"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def _run(self, query: str) -> str:
        """
        Realiza buscas combinadas usando diferentes motores de busca
        
        Args:
            query: A consulta a ser pesquisada
            
        Returns:
            String formatada com os resultados agregados
        """
        # Coleta resultados de cada fonte
        tavily_results = search_tavily_async(query)
        ddg_results = search_duckduckgo_async(query)
        serper_results = search_serper_async(query)

        # Formata o resultado final
        combined_results = (
            "=== Resultados da Pesquisa ===\n\n"
            f"{'='*100}\n\n{tavily_results}\n\n"
            f"{'='*100}\n\n{ddg_results}\n\n"
            f"{'='*100}\n\n{serper_results}"
        )
        return combined_results

    async def _arun(self, query: str) -> str:
        """Versão assíncrona com execução paralela"""
        # Executa todas as buscas simultaneamente
        tavily, ddg, serper = await asyncio.gather(
            search_tavily_async(query),
            search_duckduckgo_async(query),
            search_serper_async(query)
        )
        
        return (
            "=== Resultados Assíncronos ===\n\n"
            f"{'='*100}\n\n{tavily}\n\n"
            f"{'='*100}\n\n{ddg}\n\n"
            f"{'='*100}\n\n{serper}"
        )

# Exemplo de uso assíncrono
async def deep_search(query: str):
    search = DeepSearch()
    result = await search._arun(query)
    return result

if __name__ == "__main__":
    print(asyncio.run(deep_search("Petrobras")))
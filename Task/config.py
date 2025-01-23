import os
from langchain import hub

from dotenv import load_dotenv
load_dotenv()

class CFG:
    """
    Classe de configuração que armazena constantes e credenciais
    necessárias para interação com a API do DeepSeek.

    Atributos:
        model_reasoner (str): Nome do modelo de raciocínio.
        base_url (str): URL base para requisições na API.
        model_chat (str): Nome do modelo para chat.
        API_KEY (str): Chave de acesso para a API.
        prompt: Referência a um prompt armazenado no Hub do LangChain.
    """
    model_reasoner = "deepseek-reasoner"  
    base_url = "https://api.deepseek.com/v1" 
    model_chat = "deepseek-chat"  
    API_KEY = os.getenv("DEEP_SEEK_API_KEY")
    prompt = hub.pull("hwchase17/react")
import os
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import OpenAI
from langchain import hub
from tools_agente import tools

# Carregar variáveis de ambiente
load_dotenv()

# Constantes
DEEPSEEK_API_KEY = os.getenv("DEEP_SEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/beta"
MODEL_NAME = "deepseek-chat"

# Inicializar o modelo de linguagem
llm = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
    model=MODEL_NAME
)

# Carregar prompt do hub
prompt = hub.pull("hwchase17/react")

# Inicializar o agente
agent = create_react_agent(
    tools=tools,
    llm=llm,
    prompt=prompt,
)

# Inicializar o executor do agente
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=50
)

# Função principal para executar comandos
def executar_comando(comando):
    try:
        resposta = agent_executor.invoke({"input": comando})
        return resposta
    except Exception as e:
        print(f"Erro ao executar comando: {str(e)}")
        return None

# Exemplo de uso
if __name__ == "__main__":
    # Exemplos de comandos que o agente pode executar
    comandos = [
        "COMANDO PARA O AGENTE AQUI",
        "OUTRO COMANDO PARA O AGENTE AQUI",
    ]
    
    for comando in comandos:
        # print(f"\nExecutando comando: {comando}")
        resultado = executar_comando(comando)
        # print(f"Resultado: {resultado}")
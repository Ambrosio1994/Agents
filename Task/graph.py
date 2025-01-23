from typing import Dict

from langgraph.graph import START, END, StateGraph

from state import State, Decision
from model import make_agent, make_model
from prompts import PROMPT_TEMPLATE_INSTRUCTIONS, PROMPT_TEMPLATE_DECISION

def make_decision(state: State) -> Dict:
    """
    Avalia a mensagem do usuário para decidir se é necessário
    realizar buscas na web.

    Parâmetros:
        state (State): Estado com a mensagem recebida.

    Retorna:
        dict: Dicionário contendo a decisão ("sim" ou "nao") em "decision".
    """
    input = state['message']
    llm = make_model(model="chat")
    llm_with_structured = llm.with_structured_output(Decision)
    avaliador = PROMPT_TEMPLATE_DECISION | llm_with_structured
    dec = avaliador.invoke({"input": input}).decisao

    return {"decision": dec}

def get_response(state: State) -> Dict:
    """
    Com base na decisão, retorna a resposta final ao usuário:
    - Se 'decision' for "nao", apenas formata a resposta sem busca adicional.
    - Se 'decision' for "sim", utiliza o agente para buscar mais informações.

    Parâmetros:
        state (State): Estado com a mensagem do usuário e a decisão tomada.

    Retorna:
        dict: Dicionário contendo a mensagem de resposta em "message".
    """
    if state['decision'] == "nao":
        llm = make_model(model="chat")
        chain = PROMPT_TEMPLATE_INSTRUCTIONS| llm
        response = chain.invoke({"input": state['message']})

        return {"message": response.content}
    
    else:   
        agent_executor = make_agent()

        resp = agent_executor.invoke({
            "input": state['message'],
        })
        
        return {"message": resp["output"]}
       
def compile_graph():
    """
    Compila e retorna o grafo de estados configurado, definindo
    o fluxo de execução entre a decisão e o agente de busca.

    Retorna:
        Callable: Grafo compilado para manipular o estado e as transições.
    """
    # Configuração do grafo
    workflow = StateGraph(State)
    
    # Adiciona os nós
    workflow.add_node("make_decision_node", make_decision)
    workflow.add_node("agent", get_response)

    # Define o fluxo
    workflow.add_edge(START, "make_decision_node")
    workflow.add_edge("make_decision_node", "agent")
    workflow.add_edge("agent", END)
    return workflow.compile()   
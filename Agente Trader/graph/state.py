from typing_extensions import TypedDict

class AgentState(TypedDict):
    """
    Representa o estado principal.
    Atributos:
        message (str): Mensagem original do usuário.
    """
    ativo: str
    technical_analysis: str
    news_summary: str
    risk_analysis: str
    decision: str
    order: str
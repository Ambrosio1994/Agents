from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from typing import Annotated

class State(TypedDict):
    """
    Representa o estado principal, incluindo a mensagem do usuário
    e a decisão a ser tomada.
    
    Atributos:
        message (str): Mensagem original do usuário.
        decision (str): Decisão tomada sobre a ação (pode ser "sim" ou "nao").
    """
    message: str
    decision: str

class Decision(BaseModel):
    """
    Modelo Pydantic que define a estrutura de saída para a decisão.
    
    Atributos:
        decisao (str): Valor textual que representa a decisão
                       ("sim" para buscar na web ou "nao" caso contrário).
    """
    decisao: Annotated[
        str,
        Field(
            description="""
            Se a tarefa precisa de busca na web, informe sim,
            caso contrário informe nao
            """
        ),
    ]
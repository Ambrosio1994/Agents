from typing_extensions import TypedDict

class State(TypedDict):
    """
    Representa o estado principal, incluindo a mensagem do usuário.
    
    Atributos:
        message (str): Mensagem original do usuário.
    """
    message: str
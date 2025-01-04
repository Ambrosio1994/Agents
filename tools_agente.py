import os
from typing import List, Optional
from langchain.agents import Tool

def write_content(message: str) -> str:
    """Escreve conteúdo em um arquivo.

    Espera que o conteúdo seja passado como um string no formato "caminho_do_arquivo,conteúdo"
    Exemplo: "meu_arquivo.txt,Olá, mundo!"
    """
    try:
        file_path, content = message.split(",", 1)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        return f"Conteúdo '{content[:20]}...' escrito no arquivo '{file_path}' com sucesso!"
    except Exception as e:
        return f"Erro ao escrever no arquivo: {str(e)}"

def create_file(file_path: str) -> str:
    """Cria um novo arquivo vazio."""
    try:
        if os.path.exists(file_path):
            return f"Arquivo '{file_path}' já existe!"
        with open(file_path, "w"):
            pass
        return f"Arquivo '{file_path}' criado com sucesso!"
    except Exception as e:
        return f"Erro ao criar arquivo: {str(e)}"

def delete_file(file_path: str) -> str:
    """
    Exclui um arquivo.

    Args:
        file_path: O caminho para o arquivo a ser excluído.

    Retorna:
        Uma mensagem de sucesso se o arquivo foi excluído, ou uma mensagem de erro
        se o arquivo não existe ou ocorreu um erro.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return f"Arquivo '{file_path}' excluído com sucesso!"
        return f"Arquivo '{file_path}' não existe!"
    except Exception as e:
        return f"Erro ao excluir arquivo: {str(e)}"

def get_file_content(file_path: str, encoding: str = "utf-8") -> str:
    """
    Obtém o conteúdo de um arquivo com tratamento de erros.

    Args:
        file_path: O caminho para o arquivo a ser lido.
        encoding: O tipo de codificação a ser utilizada para ler o arquivo. Default é "utf-8".

    Returns:
        O conteúdo do arquivo como uma string ou uma mensagem de erro em caso de falha.
    """
    try:
        with open(file_path, "rb") as file:
            content = file.read()
        return content.decode(encoding)
    except UnicodeDecodeError:
        return f"Erro ao ler o arquivo: {file_path}. O arquivo contém caracteres inválidos."
    except Exception as e:
        return f"Erro ao ler arquivo: {str(e)}"

def get_file_size(file_path: str) -> int:
    """
    Obtém o tamanho de um arquivo.

    Args:
        file_path: O caminho para o arquivo cujo tamanho deve ser obtido.

    Returns:
        O tamanho do arquivo em bytes ou uma mensagem de erro em caso de falha.
    """
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        return f"Erro ao obter tamanho do arquivo: {str(e)}"

def list_files(directory: str) -> List[str]:
    """
    Lista arquivos em um diretório.

    Args:
        directory: O caminho para o diretório cujos arquivos devem ser listados.

    Returns:
        Uma lista com os nomes dos arquivos no diretório ou uma mensagem de erro em caso de falha.
    """
    try:
        return os.listdir(directory)
    except Exception as e:
        return f"Erro ao listar arquivos: {str(e)}"

def list_directories(directory: str) -> List[str]:
    """
    Lista diretórios em um diretório.

    Args:
        directory: O caminho para o diretório cujos subdiretórios devem ser listados.

    Returns:
        Uma lista com os nomes dos subdiretórios no diretório ou uma mensagem de erro em caso de falha.
    """
    try:
        return [entry for entry in os.listdir(directory) if os.path.isdir(os.path.join(directory, entry))]
    except Exception as e:
        return f"Erro ao listar diretórios: {str(e)}"

def find_file(target: str) -> str:
    """
    Procura por um arquivo em um diretório e seus subdiretórios.

    Args:
        target (str): Nome do arquivo a ser procurado.

    Returns:
        str: Mensagem indicando se o arquivo foi encontrado e sua localização, ou que não foi encontrado.
    """
    
    # Define o diretório raiz para iniciar a busca
    root = os.path.expanduser("~")

    # Verifica se o diretório raiz existe
    if not os.path.isdir(root):
        return f"Erro: O diretório '{root}' não existe!"

    # Percorre o diretório raiz e seus subdiretórios
    for current_root, _, files in os.walk(root):
        # Verifica se o arquivo alvo está no diretório atual
        if target in files:
            # Retorna o caminho do arquivo encontrado
            return f'O arquivo "{target}" foi encontrado em "{os.path.join(current_root, target)}"'

    # Retorna uma mensagem se o arquivo não foi encontrado
    return f'O arquivo "{target}" não foi encontrado no diretório "{root}" ou seus subdiretórios.'

def change_directory(new_directory: str) -> str:
    """
    Muda o diretório atual de trabalho.

    Args:
        new_directory (str): O caminho para o novo diretório a ser alterado.

    Returns:
        str: Uma mensagem indicando se o diretório foi alterado com sucesso ou uma mensagem de erro em caso de falha.
    """
    current_directory =  os.path.expanduser("~")
    try:
        if os.path.isdir(new_directory):
            current_directory = new_directory
            return f"Diretório alterado para '{new_directory}'"
        else:
            return f"Diretório '{new_directory}' não existe!"
    except Exception as e:
        return f"Erro ao mudar de diretório: {str(e)}"

# Lista de ferramentas disponíveis para o agente
tools = [
    Tool(
        name="write_content",
        func=write_content,
        description="Useful for writing content to a file. Pass the file path and content independently, separated by commas."
    ),
    Tool(
        name="create_file",
        func=create_file,
        description="Useful for creating a file."
    ),
    Tool(
        name="delete_file",
        func=delete_file,
        description="Useful for deleting a file."
    ),
    Tool(
        name="list_files",
        func=list_files,
        description="Useful for listing files in a directory."
    ),
    Tool(
        name="get_file_content",
        func=get_file_content,
        description="Useful for getting the content of a file."
    ),
    Tool(
        name="get_file_size",
        func=get_file_size,
        description="Useful for getting the size of a file."
    ),
    Tool(
        name="list_directories",
        func=list_directories,
        description="Useful for listing directories in a directory."
    ),
    Tool(
        name="find_file",
        func=find_file,
        description="Useful for finding a file in the current directory and subdirectories."
    ),
    Tool(
        name="change_directory",
        func=change_directory,
        description="Useful for changing the current working directory."
    )
]
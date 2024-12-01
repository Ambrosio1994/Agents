
from langchain_community.tools.tavily_search import TavilySearchResults

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langgraph.graph import END, StateGraph, START

from langchain_anthropic import ChatAnthropic

import getpass
import os

from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from typing import Annotated

def _set_env(key: str):
    if key not in os.environ:
        os.environ[key] = getpass.getpass(f"{key}:")


_set_env("ANTHROPIC_API_KEY") 
_set_env("TAVILY_API_KEY") 



class GraphState(TypedDict):
    """
    Representa o estado do nosso gráfico.

    Atributos:
    tema : tema do artigo que sera escrito
    web_search: pesquisas sobre o tema do artigo
    artigo: geração do artigo pelo LLM
    nota: nota de 0 a 10
    """

    tema: str
    web_search: str
    artigo : str
    critica: str
    nota: float
    iteracoes: int

class Editor_Feedback(BaseModel):
    score: Annotated[
        float,
        Field(
            description="Pontuação de 0 a 10 para artigo escrito.",
        ),
    ]
    review: Annotated[
        str,
        Field(
            description="Destaque dos pontos positivos e os \
            detalhes devem ser melhorados pelo esctitor.",
        ),
    ]

web_search_tool = TavilySearchResults(k=5)

system_escritor = """
Você é um escritor profissional especializado em criar artigos informativos
e envolventes. Sua tarefa é criar um artigo baseado no tema {tema}
em seu conhecimento prévio e nos textos de apoio fornecidos. Use estes
para refinar seu cohecimento e produzir um excelente texto para o usuario.

Para criar o artigo, siga estas diretrizes:

1. TEMA PRINCIPAL: {tema}
2. TEXTOS DE APOIO: {web_search}
3. SE HOUVER, ATENTAR PARA CRITICA DO AVALIADOR: {critica}

3. ESTRUTURA SOLICITADA:
- Título chamativo
- Introdução envolvente
- Desenvolvimento do tema em tópicos, se aprofundando nos paragrafos
- Padronizar o formato das listas (alternam entre bullets e hífens)
- Incluir uma seção de metodologia explicando a origem dos dados
- Conclusão coerente e objetiva

4. ELEMENTOS ADICIONAIS:
- Inclua dados estatísticos relevantes dos textos de apoio
- Adicione exemplos práticos
- Utilize citações quando apropriado
- Mantenha um fluxo natural entre os parágrafos

5. OTIMIZAÇÃO:
- Mantenha parágrafos concisos
- Inclua palavras-chave naturalmente
- Evite jargões desnecessários
- Nas secoes incluir exemplos específicos de acordo com o caso

Ao receber a critica do seu ultimo artigo {artigo}, voce recebera junto
sua este artigo e voce deve:

1. Fazer uma profunda reflexao sobre esta critica,
pensando de maneira inteligente sobre o que deve ser
melhorado e deve ser mantido.
2. Planejar com cautela seu próximo texto para que nao sejam repetidos novos
erros e deve se certificar que todas as melhorias foram implantada no
seu texto
3. Implantar essas melhorias no seu proximo texto gerado

##ATENÇAÕ##

Se uma critica nao for enviada voce devera se atentar apenas aos textos
de apoio enviados.
Não mencione a critica recebida no seu proximo texto
apenas a leia e siga as recomendações.

Por favor, crie um artigo original que atenda a estes requisitos,
mantendo um equilíbrio entre informação e engajamento do leitor.
"""

prompt_escritor = ChatPromptTemplate.from_messages(
    [
        ("system", system_escritor),
        (
            "human",
            "Aqui esta o tema {tema} e os textos de apoios {web_search}. \
            Aqui esta seu ultimo artigo {artigo} \
            Aqui esta a critica do avaliador {critica}",
        ),
    ]
)
model = "claude-3-5-sonnet-20241022"
llm = ChatAnthropic(model=model, temperature=0.6, max_tokens=2000)
escritor = prompt_escritor | llm | StrOutputParser()

system_critico = """
Você é um especialista em análise e correção textual, com vasta experiência
em avaliação de artigos acadêmicos e textos diversos.
Sua tarefa é analisar minuciosamente os textos recebidos
considerando os seguintes aspectos:

1. Estrutura e organização:
- Coerência e coesão
- Estrutura dos parágrafos
- Progressão lógica das ideias

2. Conteúdo:
- Clareza na exposição das ideias
- Argumentação
- Profundidade da análise
- Relevância das informações

3. Linguagem:
- Adequação ao registro formal/informal
- Vocabulário
- Gramática e ortografia
- Pontuação

4. Aspectos técnicos:
- Formatação
- Citações (quando aplicável)
- Referências (quando aplicável)

Para cada texto analisado, você deve fornecer:

1. Um resumo dos pontos positivos, destacando os aspectos bem desenvolvidos do texto.

2. Uma lista de pontos que necessitam de melhorias, com sugestões específicas para aprimoramento.

3. Um breve comentário final com recomendações gerais para o autor.

Por favor, mantenha um tom construtivo e profissional em suas análises,
focando sempre em como o texto pode ser aprimorado.

5. Faca sua analise do artigo: {artigo}

"""

prompt_critico = ChatPromptTemplate.from_messages(
    [
        ("system", system_critico),
        (
            "human",
            "Aqui está a artigo: \n\n {artigo} \n De sua nota e sua avaliacao da artigo",
        ),
    ]
)

llm = ChatAnthropic(model=model, temperature=0, max_tokens=1000)
structured_llm_feedback = llm.with_structured_output(Editor_Feedback)
critico = prompt_critico | structured_llm_feedback

def format_searchs(searchs):
  """
Concatena o conteúdo de uma lista de resultados de pesquisa em uma única string.

Argumentos:
searchs (list of dict): Uma lista de dicionários, cada um contendo uma chave content.

Retorna:
str: Uma única string com conteúdo concatenado de cada dicionário na lista.
    """
  search = ""
  for s in searchs:
    search += s["content"]
  return search

def web_search(state: GraphState):
    """
    Executa uma pesquisa na web com base no tema fornecido no estado e armazena
    os resultados no estado.

    Argumentos:
    state (GraphState): O estado atual do gráfico, contendo o tema
    para o qual uma pesquisa na web será realizada.

    Retorna:
    dict: Um dicionário contendo os resultados da pesquisa na web sob a chave "web_search".
    """
    print("-----Web Search-----\n")
    tema = state["tema"]
    searchs = web_search_tool.invoke({"query": tema})
    searchs = format_searchs(searchs)
    print("Resultados da pesquisa:", searchs)

    state["web_search"] = searchs
    return {"web_search": searchs}

def escrever_artigo(state: GraphState):
    """
    Gera um artigo com base no estado fornecido e atualiza o estado com
    o conteúdo gerado.

    Esta função usa o tema e os resultados da pesquisa na web do estado para criar
    um artigo. Ela invoca um modelo de linguagem para gerar o artigo e atualiza
    o estado com o novo artigo e contagem de iterações. O artigo gerado é
    também impresso no console.

    Argumentos:
    estado (GraphState): O estado atual do gráfico, contendo o tema,
    resultados da pesquisa na web, críticas anteriores e qualquer artigo
    gerado anteriormente.

    Retorna:
    dict: Um dicionário com o artigo atualizado e contagem de iterações.
    """
    textos_apoio = state["web_search"]

    tema = state["tema"]
    critica = state["critica"] if "critica" in state else ""
    artigo = state["artigo"] if "artigo" in state else ""
    iteracao = state["iteracoes"]

    resposta = escritor.invoke({
        "tema": tema, "web_search": textos_apoio,
        "critica": critica,  "artigo": artigo
        })

    artigo = resposta.strip()

    # Atualizar o estado com a redação gerada
    state["artigo"] = artigo

    # Exibir a redação gerada
    print(f"-----Artigo {iteracao} gerado:-----")
    print(artigo)
    state["iteracoes"] += 1

    # Retornar o estado atualizado como um dicionário
    return {"artigo": artigo, "iteracoes": state["iteracoes"]}

def avaliar_artigo(state: GraphState):
    """
    Avalia um artigo do estado fornecido e atualiza o estado com
    a pontuação de feedback e revisão.

    Esta função utiliza um modelo de linguagem para gerar feedback para o
    artigo presente no estado. O feedback inclui uma revisão e uma pontuação
    que são então usadas para atualizar o estado.

    Argumentos:
    state (GraphState): O estado atual do gráfico, contendo o
    artigo a ser avaliado.

    Retorna:
    dict: Um dicionário contendo o artigo, a pontuação de feedback sob
    a chave "nota" e a revisão de feedback sob a chave "critica".
    """
    print("-----CRITICA-----")
    artigo = state["artigo"]

    feedback = critico.invoke({"artigo": artigo})
    state["critica"] = feedback.review
    state["nota"] = feedback.score

    print(feedback.review)

    print("-----NOTA-----")
    print(feedback.score)

    return {"artigo": artigo,
            "nota": feedback.score,
            "critica": feedback.review}


def decide_to_generate(state: GraphState,
                       threshold: float,
                       max_iteracoes: int):
    """
    Decida se deseja gerar outro artigo com base no estado atual.

    Argumentos:
    state (GraphState): O estado atual do gráfico, contendo o
    artigo a ser avaliado.
    threshold (float): A pontuação mínima necessária para parar de gerar
    artigos.
    max_iteracoes (int): O número máximo de iterações para gerar
    artigos.

    Retorna:
    str: A decisão de gerar outro artigo, seja "refazer" ou
    "finalizar".
    """
    nota = state["nota"]
    iteracoes = state["iteracoes"]

    if iteracoes >= max_iteracoes:
        state["decisao"] = "finalizar"
        return "finalizar"

    if nota <= threshold:
        return "refazer"
    else:
        return "finalizar"

work_flow = StateGraph(GraphState)
work_flow.add_node("web_search_node", web_search)
work_flow.add_node("escritor_node", escrever_artigo)
work_flow.add_node("critico_node", avaliar_artigo)

work_flow.add_edge(START, "web_search_node")
work_flow.add_edge("web_search_node", "escritor_node")
work_flow.add_edge("escritor_node", "critico_node")

max_iteracoes = 3
threshold = 9
work_flow.add_conditional_edges(
    "critico_node",
    lambda state: decide_to_generate(state, threshold=threshold, max_iteracoes=max_iteracoes),
    {
        "refazer": "escritor_node",
        "finalizar": END,
    },
)

app = work_flow.compile()

from pprint import pprint

inputs = {"tema": "o que mundo no mundo após a covid", "iteracoes":0}
for output in app.stream(inputs):
    for key, value in output.items():
        pprint(f"Node '{key}':")
    pprint("\n---\n")
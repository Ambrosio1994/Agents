# Projeto de Assistente de IA com Busca na Web

Este projeto contém um assistente de IA que recebe uma mensagem do usuário, decide se há necessidade de busca na web e, em seguida, retorna uma resposta adequada. Ele faz uso de ferramentas do ecossistema LangChain, bem como de agendamentos para execução de tarefas em horários específicos.

## Sumário

1. [Arquivos Principais](#arquivos-principais)  
2. [Fluxo de Funcionamento](#fluxo-de-funcionamento)  
3. [Instalação e Configuração](https://github.com/Ambrosio1994/Agents/blob/main/Task/config.py)
4. [Agendamento de Tarefas](#agendamento-de-tarefas)  
5. [Estrutura de Diretórios](#estrutura-de-diretórios)  

---

## Arquivos Principais

- <b>brew/model.py</b>  
  Contém funções responsáveis por criar modelos de linguagem (ChatOpenAI) e instanciar agentes (AgentExecutor) para processamento de linguagem natural e buscas na web.

  - <b>make_model(model: str)</b>  
    Cria e retorna um objeto ChatOpenAI de acordo com o modelo especificado:  
    - "reasoner" para raciocínio.  
    - "chat" para conversas simples.

  - <b>make_agent()</b>  
    Cria e retorna um <i>AgentExecutor</i> configurado com as ferramentas (ex.: <i>TavilySearchResults</i>) e pronto para executar buscas e fornecer respostas estruturadas.

- <b>brew/main.py</b>  
  Gera e executa a tarefa principal de forma assíncrona. Valida se a data e hora fornecidas são adequadas para o agendamento. Caso sejam válidas, cria um novo loop de eventos e agenda a execução do fluxo principal por meio de cron.

- <b>brew/config.py</b>  
  Define a classe <b>CFG</b>, responsável por unificar as variáveis de ambiente e configurações importantes, como modelos de IA, URLs de API, chaves de acesso, e o prompt utilizado pelo LangChain.

- <b>brew/graph.py</b>  
  Monta o grafo de estados e define as funções que serão executadas:
  - <b>make_decision(state: State)</b>: Decide se uma busca na web é necessária.  
  - <b>get_response(state: State)</b>: Obtém a resposta final, usando ou não a busca/web.  
  - <b>compile_graph()</b>: Compila o grafo definindo o fluxo de execução.

- <b>brew/prompts.py</b>  
  Define os prompts utilizados para gerar as mensagens de instrução e decisão.  
  - <b>PROMPT_TEMPLATE_INSTRUCTIONS</b>: Fornece um contexto para tarefas simples, como lembretes.  
  - <b>PROMPT_TEMPLATE_DECISION</b>: Orienta o modelo a decidir entre "sim" e "nao" para a busca na web.

- <b>brew/state.py</b>  
  Define a estrutura do estado (<b>State</b>) usando <i>TypedDict</i> e a classe <b>Decision</b> (modelo Pydantic) para determinar a decisão de busca.

---

## Fluxo de Funcionamento

1. O ponto de entrada é o arquivo <b>brew/main.py</b>, que agenda a execução assíncrona.  
2. Quando a tarefa é disparada, a função <b>main_async()</b> invoca o fluxo compilado em <b>brew/graph.py</b>.  
3. Esse fluxo ([StateGraph](https://github.com/hwchase17/langchain), adaptado neste projeto) chama <b>make_decision()</b> para decidir se a tarefa requer busca na web.  
   - Se <b>decision</b> == "nao", uma resposta simples é retornada ao usuário, sem processo adicional.  
   - Se <b>decision</b> == "sim", o projeto executa o agente retornado por <b>make_agent()</b>, que faz uso de ferramentas internas (TavilySearchResults) para coletar informações e gerar a resposta.  
4. Ao fim, o resultado é impresso no console.

---

## Instalação e Configuração

1. Clone este repositório localmente.  
2. Crie um ambiente virtual e instale as dependências. Exemplo (Linux/Mac):  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configure variáveis de ambiente no arquivo <b>.env</b> se necessário. As chaves esperadas incluem, por exemplo, <b>DEEP_SEEK_API_KEY</b> e <b>TAVILY_API_KEY</b>.

---

## Agendamento de Tarefas

- O arquivo <b>brew/main.py</b> usa <i>apscheduler</i> para agendar a execução da função <b>main_async()</b>.  
- É possível definir a data (<b>date</b>) e hora (<b>time</b>) para a execução de cada tarefa. Caso sejam anteriores ao horário atual, as tarefas não são agendadas.  
- O loop de eventos é criado e mantido em execução, aguardando a chegada do horário definido.

---

## Estrutura de Diretórios

Uma visão simplificada: 

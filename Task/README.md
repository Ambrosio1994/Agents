# Projeto de Assistente de IA com Busca na Web

Este projeto contém um assistente de IA que utiliza ferramentas de busca na web para responder consultas dos usuários. O sistema é capaz de agendar tarefas para execução em horários específicos e utiliza o framework LangChain para processamento de linguagem natural.

## Sumário

1. [Arquivos Principais](#arquivos-principais)
2. [Fluxo de Funcionamento](#fluxo-de-funcionamento)
3. [Instalação e Configuração](#instalação-e-configuração)
4. [Agendamento de Tarefas](#agendamento-de-tarefas)
5. [Estrutura de Diretórios](#estrutura-de-diretórios)

---

## Estrutura de Diretórios

1. [Config](https://github.com/Ambrosio1994/Agents/blob/main/Task/config.py)
2. [Graph](https://github.com/Ambrosio1994/Agents/blob/main/Task/graph.py)
3. [Main](https://github.com/Ambrosio1994/Agents/blob/main/Task/main.py)
4. [Prompts](https://github.com/Ambrosio1994/Agents/blob/main/Task/prompts.py)
5. [State](https://github.com/Ambrosio1994/Agents/blob/main/Task/state.py)

---

## Arquivos Principais

- **Task/config.py**  
  Define a classe **CFG** que gerencia as configurações do projeto, incluindo:
  - Modelo de IA utilizado
  - URL base para API
  - Chaves de API necessárias

- **Task/graph.py**  
  Implementa o fluxo principal do assistente usando LangGraph:
  - Configura a ferramenta de busca (TavilySearchResults)
  - Define o agente ReAct para processamento de linguagem natural
  - Compila o grafo de estados para execução das tarefas

- **Task/main.py**  
  Gerencia o agendamento e execução das tarefas:
  - Valida data e hora para agendamento
  - Executa o fluxo principal de forma assíncrona
  - Utiliza APScheduler para agendamento via cron

- **Task/prompts.py**  
  Contém o template do prompt utilizado pelo agente:
  - Define o comportamento esperado do assistente
  - Especifica o formato exato das respostas
  - Inclui instruções para uso das ferramentas de busca

- **Task/state.py**  
  Define a estrutura de dados do estado usando TypedDict:
  - Armazena a mensagem do usuário
  - Mantém o estado durante o processamento

---

## Fluxo de Funcionamento

1. O usuário define uma tarefa e um horário para execução em **main.py**
2. No horário agendado, o sistema:
   - Compila o grafo de estados
   - Inicializa o agente com as ferramentas necessárias
   - Processa a mensagem do usuário
   - Realiza buscas na web quando necessário
   - Retorna uma resposta formatada

---

## Instalação e Configuração

1. Clone este repositório
2. Crie um ambiente virtual Python:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   .\venv\Scripts\activate  # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente no arquivo **.env**:
   - DEEP_SEEK_API_KEY
   - TAVILY_API_KEY

---

## Agendamento de Tarefas

- Defina a data e hora no arquivo **main.py**:
  ```python
  date = "2025-01-24"  # Formato: YYYY-MM-DD
  time = "16:32"       # Formato: HH:MM
  ```
- O sistema valida se a data/hora é futura
- A tarefa é agendada usando APScheduler com timezone configurável
- O loop de eventos assíncronos gerencia a execução no horário especificado

---

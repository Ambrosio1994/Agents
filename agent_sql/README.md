# SQL Agent com LangChain

Este projeto demonstra o uso do LangChain para criar um agente SQL inteligente capaz de entender e responder perguntas em linguagem natural gerando e executando consultas SQL em dados.

## Visão geral

O SQL Agent usa um Large Language Model (DeepSeek ou LLM alternativo) para traduzir perguntas em linguagem natural em consultas SQL, executá-las em um banco de dados SQLite e interpretar os resultados para fornecer respostas significativas.

## Recursos

- Tradução de consulta de linguagem natural para SQL
- Execução de consultas SQL em um banco de dados
- Interpretação de resultados de consulta para fornecer respostas legíveis por humanos
- Suporte para diferentes LLMs (DeepSeek, OpenAI, Anthropic)

## Estrutura do projeto

```
agent_sql/
├── data/ # Contém os arquivos do conjunto de dados
│ └── all-states-history.csv # Dados de estado histórico
├── db/ # Diretório do banco de dados SQLite
├── __pycache__/ # Arquivos de cache Python
├── .envexempla # Exemplo de arquivo de variável de ambiente
├── main.py # Script do aplicativo principal
├── prompts.py # Modelos de prompt para o LLM
├── README.md # Este arquivo
└── requirements.txt # Dependências do Python
```

## Pré-requisitos

- Python 3.8 ou superior
- Chave de API para um dos LLMs suportados (DeepSeek, OpenAI ou Anthropic)

## Instalação

1. Clone este repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` baseado em `.envexempla` e adicione sua chave de API:

```
# Escolha uma das opções abaixo
# Renomeie este arquivo para .env
DEEP_SEEK_API_KEY=your_deepseek_api_key
# OU
OPENAI_API_KEY=your_openai_api_key
# OU
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## Uso

1. Execute o main roteiro:

```bash
python principal.py
```

2. O script irá:
 - Crie um banco de dados SQLite a partir do arquivo de dados CSV
 - Configure o agente SQL com o LLM escolhido
 - Execute uma pergunta predefinida (ou você pode modificar a variável QUESTION em main.py)
 - Exibir os resultados

## Exemplo de pergunta

A pergunta de exemplo padrão é:

```
Quantos pacientes foram hospitalizados durante outubro de 2020
em Nova York e em todo o país como o total de todos os estados?
```

(Quantos pacientes foram hospitalizados durante outubro de 2020 em Nova York e em todo o país como o total de todos os estados?)

## Personalização

- Para alterar a pergunta, modifique a variável `QUESTION` em `main.py`
- Para usar um LLM diferente, atualize o arquivo `.env` e modifique a configuração `llm` em `main.py`
- Para usar dados diferentes, substitua o arquivo CSV e atualize o código de criação do banco de dados em `main.py`

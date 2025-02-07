# Sistema Multi-Agentes para Trading Automatizado

Este sistema é composto por agentes especializados que trabalham em conjunto para realizar análises de mercado, tomar decisões de investimento e executar operações de forma automatizada.

## Estrutura dos Agentes

### 1. Agente de Coleta de Dados (`data_collection_agent.py`)
Responsável por agregar informações de múltiplas fontes:
- Busca notícias e informações relevantes usando APIs (Tavily, DuckDuckGo, Serper)
- Processa e sumariza as informações coletadas usando LLMs
- Fornece contexto atualizado sobre ativos e mercado

**Principais funcionalidades:**
```python
news_summary_agent(query: str) -> str
```
- Realiza buscas profundas de informações
- Sumariza resultados usando modelos de linguagem
- Retorna análises contextualizadas

### 2. Agente de Análise de Dados (`data_analysis_agent.py`)
Processa dados brutos e gera insights acionáveis:
- Análise técnica (preços, volumes, indicadores)
- Análise fundamentalista
- Integração de múltiplas fontes de dados

**Principais funcionalidades:**
```python
run_data_analysis_agent() -> dict
```
- Análise técnica e fundamental combinada
- Geração de indicadores
- Identificação de padrões

### 3. Agente de Tomada de Decisão (`decision_making_agent.py`)
Define estratégias de compra/venda baseadas em:
- Regras predefinidas
- Análises técnicas/fundamentais
- Insights de mercado

### 4. Agente de Gerenciamento de Risco (`risk_management_agent.py`)
Controla exposição e otimiza alocação:
- Definição de stop loss/take profit
- Controle de exposição por ativo
- Diversificação de carteira

### 5. Agente de Execução de Ordens (`order_execution_agent.py`)
Responsável pela interface com corretoras:
- Envio de ordens
- Monitoramento de execução
- Gestão de posições

### 6. Agente de Monitoramento (`monitoring_agent.py`)
Acompanha desempenho e ajusta estratégias:
- Monitoramento de performance
- Ajustes em tempo real
- Alertas e notificações

## Ferramentas Utilizadas

### Análise (`tools/analysis.py`)
- Indicadores técnicos
- Métricas fundamentalistas
- Análise de sentimento

### Busca de Informações (`tools/search_information.py`)
- Integração com múltiplas APIs de busca
- Processamento assíncrono
- Agregação de resultados

### Operações (`tools/operations_tools.py`)
- Interface com corretoras
- Gestão de ordens
- Controle de posições

## Configuração e Uso

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure as variáveis de ambiente:
```bash
TAVILY_API_KEY=sua_chave
SERPER_API_KEY=sua_chave
GEMINI_API_KEY=sua_chave
PAPER_APCA_API_KEY=sua_chave
PAPER_APCA_API_SECRET=sua_chave
```

3. Execute os agentes individualmente ou o sistema completo:
```python
from agents.data_collection_agent import news_summary_agent
from agents.data_analysis_agent import run_data_analysis_agent

# Exemplo de uso
results = news_summary_agent("AAPL")
analysis = run_data_analysis_agent()
```

## Arquitetura do Sistema

```
Agents/
├── data_collection_agent.py   # Coleta de dados
├── data_analysis_agent.py     # Análise de dados
├── decision_making_agent.py   # Tomada de decisão
├── risk_management_agent.py   # Gestão de risco
├── order_execution_agent.py   # Execução de ordens
├── monitoring_agent.py        # Monitoramento
└── tools/
    ├── analysis.py           # Ferramentas de análise
    ├── search_information.py # Busca de informações
    └── operations_tools.py   # Operações com corretoras
```

## Contribuição

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nome`)
3. Commit suas mudanças (`git commit -am 'Adiciona feature'`)
4. Push para a branch (`git push origin feature/nome`)
5. Crie um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

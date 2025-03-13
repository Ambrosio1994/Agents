# Interface Unificada para Sistema de Agentes

Esta interface permite controlar e monitorar todos os agentes do sistema através de um único ponto de acesso.

## 🌐 Visão Geral

A interface unificada proporciona uma experiência integrada para gerenciar os diferentes agentes disponíveis no sistema. Através dela, é possível:

- Iniciar e parar agentes individuais
- Monitorar o status e progresso de cada agente
- Visualizar resultados e análises
- Configurar parâmetros para cada agente
- Orquestrar fluxos de trabalho envolvendo múltiplos agentes

## 💻 Tecnologias Utilizadas

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Comunicação entre agentes**: WebSockets e Filas de Mensagens
- **Visualização de dados**: Plotly e Streamlit Components
- **Autenticação**: JWT

## 🚀 Como Iniciar

### Requisitos

- Python 3.9+
- Todas as dependências dos agentes instaladas

### Instalação

```bash
# Instalar dependências da interface
pip install -r interface/requirements.txt
```

### Execução

```bash
# Iniciar o backend da API
python interface/api.py

# Em outro terminal, iniciar a interface web
python interface/app.py
```

A interface estará disponível em:
- WebUI: http://localhost:8501
- API: http://localhost:8000

## 🔧 Configuração

Configure as opções da interface no arquivo `interface/config.yaml`:

```yaml
# Configurações gerais
general:
  log_level: INFO
  enable_telemetry: false
  theme: "light"

# Configurações dos agentes
agents:
  trader:
    auto_start: false
    refresh_interval: 60  # segundos
    
  escritor:
    auto_start: false
    max_tokens: 2000
    
  sql:
    auto_start: false
    max_db_connections: 3
    
  tarefa:
    auto_start: false
    parallelism: 4
```

## 📊 Dashboard Principal

O dashboard principal apresenta:

1. **Resumo do Sistema**
   - Status de cada agente
   - Utilização de recursos
   - Alertas e notificações

2. **Controle de Agentes**
   - Botões de iniciar/parar para cada agente
   - Seleção de modos de operação

3. **Visualização de Resultados**
   - Gráficos interativos
   - Logs de atividade
   - Análises produzidas

## 🔄 Fluxos de Trabalho

A interface permite configurar fluxos de trabalho personalizados envolvendo múltiplos agentes. Exemplos:

1. **Análise de Ativos Financeiros**
   - Agente Trader → Agente SQL → Escritor de Artigo

2. **Pesquisa de Mercado**
   - Agente SQL → Escritor de Artigo → Tarefa (para distribuição)

Os fluxos podem ser configurados através da interface gráfica arrastando e conectando componentes.

## 🛡️ Segurança

A interface implementa:
- Autenticação de usuários
- Controle de acesso por função
- Criptografia de dados sensíveis
- Registros de auditoria

## 🔍 Monitoramento Avançado

Para cada agente, a interface oferece painéis detalhados com:
- Métricas de desempenho
- Histórico de atividades
- Utilização de recursos
- Logs detalhados

## 📱 Versão Mobile

A interface web é responsiva e se adapta automaticamente a dispositivos móveis, permitindo monitorar e controlar o sistema à distância.

## 🔮 Próximos Passos

- Implementação de notificações por email e push
- Suporte a agentes desenvolvidos pela comunidade
- Dashboard personalizado por usuário
- Integração com serviços de nuvem

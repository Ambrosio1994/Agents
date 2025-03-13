# Interface Unificada para Agentes

Esta interface centralizada permite gerenciar e monitorar todos os agentes do sistema através de um único painel de controle.

## Características

- **Painel centralizado**: Visualize e gerencie todos os agentes em uma única interface
- **Configuração simplificada**: Configure parâmetros globais e específicos de cada agente
- **Monitoramento em tempo real**: Acompanhe o status e desempenho de cada agente
- **Orquestração**: Execute fluxos de trabalho que envolvam múltiplos agentes
- **Histórico e logs**: Acesse registros detalhados das operações realizadas

## Arquitetura

A interface unificada é baseada em uma arquitetura cliente-servidor:

- **Backend**: API Flask que se comunica com os diferentes agentes
- **Frontend**: Interface web em React com componentes responsivos
- **Banco de dados**: Armazenamento para configurações, histórico e métricas
- **Mensageria**: Sistema de notificações em tempo real baseado em WebSockets

```
interface/
├── app.py                  # Aplicação principal (Flask)
├── config.py               # Configurações globais
├── static/                 # Arquivos estáticos
│   ├── css/                # Estilos
│   ├── js/                 # Scripts frontend
│   └── images/             # Imagens e ícones
├── templates/              # Templates HTML
│   ├── index.html          # Página principal
│   ├── dashboard.html      # Painel de controle
│   └── components/         # Componentes reutilizáveis
├── controllers/            # Controladores de rotas
│   ├── trader.py           # Controlador do agente trader
│   ├── writer.py           # Controlador do agente escritor
│   ├── sql.py              # Controlador do agente SQL
│   └── tasks.py            # Controlador do agente de tarefas
├── models/                 # Modelos de dados
│   ├── agent.py            # Modelo base para agentes
│   ├── user.py             # Modelo de usuário
│   └── task.py             # Modelo de tarefa
└── services/               # Serviços de negócio
    ├── agent_manager.py    # Gerenciamento de agentes
    ├── auth.py             # Autenticação e autorização
    └── notification.py     # Sistema de notificações
```

## Instalação e Execução

1. Certifique-se de ter todas as dependências instaladas:
```bash
pip install -r requirements.txt
```

2. Configure o banco de dados:
```bash
python interface/setup_db.py
```

3. Inicie a aplicação:
```bash
python interface/app.py
```

4. Acesse a interface em seu navegador:
```
http://localhost:5000
```

## Guia de Uso

### Configurando um Novo Agente

1. Acesse a página "Configuração" no menu principal
2. Clique em "Adicionar Novo Agente"
3. Selecione o tipo de agente (Trader, Escritor, SQL, Tarefas)
4. Configure os parâmetros específicos
5. Salve a configuração

### Monitorando Agentes

O painel principal exibe:
- Status atual de cada agente (ativo/inativo)
- Métricas de desempenho relevantes
- Alertas e notificações
- Histórico recente de atividades

### Executando Fluxos de Trabalho

1. Na seção "Fluxos de Trabalho", clique em "Novo Fluxo"
2. Arraste e conecte os diferentes agentes no designer visual
3. Configure os parâmetros de cada etapa
4. Defina condições de sucesso e falha
5. Inicie o fluxo e monitore seu progresso

## Integrações

A interface unificada oferece integrações com:

- **Serviços de Mensageria**: Slack, Discord, Email
- **Ferramentas de Monitoramento**: Grafana, Prometheus
- **Sistemas de Armazenamento**: Google Drive, Dropbox
- **Plataformas de Colaboração**: Notion, Trello

## Próximos Passos

- [ ] Implementação de autenticação por múltiplos fatores
- [ ] Expansão do designer visual de fluxos de trabalho
- [ ] Adição de templates pré-configurados para tarefas comuns
- [ ] Integração com mais serviços externos
- [ ] Desenvolvimento de uma versão mobile da interface

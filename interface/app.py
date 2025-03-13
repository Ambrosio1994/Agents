"""
Interface unificada para o Sistema de Agentes
Implementação frontend com Streamlit

Author: Ambrosio1994
Data: Março, 2025
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import yaml
from datetime import datetime
import os

# Configurações da aplicação
st.set_page_config(
    page_title="Sistema de Agentes Unificado",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Definição de constantes
API_URL = "http://localhost:8000"  # URL da API backend

# Carregamento de configurações (simulado)
def load_config():
    # Em produção, carregar do arquivo config.yaml
    config = {
        "general": {
            "log_level": "INFO",
            "enable_telemetry": False,
            "theme": "light"
        },
        "agents": {
            "trader": {
                "auto_start": False,
                "refresh_interval": 60
            },
            "escritor": {
                "auto_start": False,
                "max_tokens": 2000
            },
            "sql": {
                "auto_start": False,
                "max_db_connections": 3
            },
            "tarefa": {
                "auto_start": False,
                "parallelism": 4
            }
        }
    }
    return config

# Helpers para simular chamadas de API
def get_agent_status(agent_name):
    # Simula chamada à API - em produção usar requests
    statuses = {
        "trader": {"status": "active", "last_active": "2025-03-13T12:30:45", "cpu": 0.3, "memory": 0.24},
        "escritor": {"status": "standby", "last_active": "2025-03-13T10:15:22", "cpu": 0.1, "memory": 0.18},
        "sql": {"status": "active", "last_active": "2025-03-13T12:28:15", "cpu": 0.22, "memory": 0.15},
        "tarefa": {"status": "stopped", "last_active": "2025-03-12T18:45:30", "cpu": 0.0, "memory": 0.05}
    }
    return statuses.get(agent_name, {"status": "unknown"})

def get_recent_results(agent_name, limit=5):
    # Simula resultados recentes dos agentes
    if agent_name == "trader":
        return [
            {"timestamp": "2025-03-13T12:30:00", "asset": "PETR4", "action": "BUY", "price": 28.45, "confidence": 0.87},
            {"timestamp": "2025-03-13T12:25:00", "asset": "VALE3", "action": "HOLD", "price": 68.12, "confidence": 0.65},
            {"timestamp": "2025-03-13T12:20:00", "asset": "ITUB4", "action": "SELL", "price": 32.18, "confidence": 0.92},
        ]
    elif agent_name == "escritor":
        return [
            {"timestamp": "2025-03-13T10:15:00", "type": "report", "title": "Análise de Mercado - 13/Mar", "words": 1250},
            {"timestamp": "2025-03-12T16:45:00", "type": "article", "title": "Tendências do Mercado Financeiro", "words": 2100},
        ]
    elif agent_name == "sql":
        return [
            {"timestamp": "2025-03-13T12:28:00", "database": "financeiro", "query_type": "SELECT", "rows": 156, "exec_time": 0.54},
            {"timestamp": "2025-03-13T12:15:00", "database": "clientes", "query_type": "JOIN", "rows": 87, "exec_time": 1.23},
        ]
    elif agent_name == "tarefa":
        return [
            {"timestamp": "2025-03-12T18:45:00", "task_id": "TASK-2025-03-12-001", "status": "completed", "steps": 8, "success": True},
            {"timestamp": "2025-03-12T17:30:00", "task_id": "TASK-2025-03-12-002", "status": "failed", "steps": 3, "success": False},
        ]
    return []

def toggle_agent(agent_name, desired_status):
    # Simula ativação/desativação do agente
    st.success(f"Agente {agent_name} {'ativado' if desired_status == 'active' else 'desativado'} com sucesso!")
    return True

# Sidebar
def render_sidebar():
    st.sidebar.title("Sistema de Agentes")
    st.sidebar.image("https://raw.githubusercontent.com/Ambrosio1994/Agents/main/escritor-de-artigo/writer_crtic.png", width=250)
    
    # Menu de navegação
    st.sidebar.header("Navegação")
    page = st.sidebar.selectbox(
        "Selecione uma página:",
        ["Dashboard", "Agente Trader", "Escritor de Artigo", "Agente SQL", "Sistema de Tarefas", "Configurações"]
    )
    
    # Status do sistema
    st.sidebar.header("Status do Sistema")
    col1, col2 = st.sidebar.columns(2)
    col1.metric("CPU", "24%", "2%")
    col2.metric("Memória", "1.2 GB", "-0.1 GB")
    
    st.sidebar.progress(0.24, "Utilização do sistema")
    
    # Informações
    st.sidebar.header("Informações")
    st.sidebar.info(
        """
        **Versão:** 1.0.0  
        **Atualizado:** 13/Mar/2025  
        **Suporte:** ambrosio@example.com
        """
    )
    
    return page

# Componentes principais
def render_dashboard():
    st.title("🪟 Dashboard do Sistema de Agentes")
    
    # Row 1 - Status Cards
    st.subheader("Status dos Agentes")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        agent_status = get_agent_status("trader")
        status_color = "green" if agent_status["status"] == "active" else "orange" if agent_status["status"] == "standby" else "red"
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 5px; border: 1px solid {status_color};">
            <h4 style="color: {status_color};">Agente Trader</h4>
            <p>Status: {agent_status["status"].upper()}</p>
            <p>Última atividade: {agent_status["last_active"].split("T")[1]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        agent_status = get_agent_status("escritor")
        status_color = "green" if agent_status["status"] == "active" else "orange" if agent_status["status"] == "standby" else "red"
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 5px; border: 1px solid {status_color};">
            <h4 style="color: {status_color};">Escritor de Artigo</h4>
            <p>Status: {agent_status["status"].upper()}</p>
            <p>Última atividade: {agent_status["last_active"].split("T")[1]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        agent_status = get_agent_status("sql")
        status_color = "green" if agent_status["status"] == "active" else "orange" if agent_status["status"] == "standby" else "red"
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 5px; border: 1px solid {status_color};">
            <h4 style="color: {status_color};">Agente SQL</h4>
            <p>Status: {agent_status["status"].upper()}</p>
            <p>Última atividade: {agent_status["last_active"].split("T")[1]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        agent_status = get_agent_status("tarefa")
        status_color = "green" if agent_status["status"] == "active" else "orange" if agent_status["status"] == "standby" else "red"
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 5px; border: 1px solid {status_color};">
            <h4 style="color: {status_color};">Sistema de Tarefas</h4>
            <p>Status: {agent_status["status"].upper()}</p>
            <p>Última atividade: {agent_status["last_active"].split("T")[1]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Row 2 - Utilização de Recursos
    st.subheader("Utilização de Recursos")
    resources_data = {
        "Agente": ["Trader", "Escritor", "SQL", "Tarefa"],
        "CPU (%)": [30, 10, 22, 5],
        "Memória (%)": [24, 18, 15, 5],
    }
    df_resources = pd.DataFrame(resources_data)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_resources['Agente'],
        y=df_resources['CPU (%)'],
        name='CPU (%)',
        marker_color='royalblue'
    ))
    fig.add_trace(go.Bar(
        x=df_resources['Agente'],
        y=df_resources['Memória (%)'],
        name='Memória (%)',
        marker_color='lightgreen'
    ))
    fig.update_layout(barmode='group', height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Row 3 - Últimas Atividades
    st.subheader("Últimas Atividades")
    activities = [
        {"timestamp": "12:30:45", "agent": "Trader", "action": "Compra de ação PETR4", "status": "success"},
        {"timestamp": "12:28:15", "agent": "SQL", "action": "Consulta em banco financeiro", "status": "success"},
        {"timestamp": "10:15:22", "agent": "Escritor", "action": "Geração de relatório", "status": "success"},
        {"timestamp": "18:45:30", "agent": "Tarefa", "action": "Processamento de tarefas diárias", "status": "error"},
    ]
    
    for activity in activities:
        status_color = "green" if activity["status"] == "success" else "red"
        st.markdown(f"""
        <div style="padding: 5px; margin-bottom: 5px; border-left: 5px solid {status_color}; background-color: rgba(0,0,0,0.03);">
            <code>{activity["timestamp"]}</code> • <strong>{activity["agent"]}</strong>: {activity["action"]}
        </div>
        """, unsafe_allow_html=True)
    
    # Row 4 - Fluxo de Trabalho
    st.subheader("Fluxos de Trabalho Ativos")
    workflow_data = {
        "ID": ["WF-001", "WF-002"],
        "Nome": ["Análise de Mercado", "Geração de Relatórios"],
        "Início": ["10:00:00", "11:30:00"],
        "Progresso": [75, 30],
        "Status": ["Em execução", "Em execução"]
    }
    df_workflow = pd.DataFrame(workflow_data)
    
    for idx, row in df_workflow.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{row['Nome']}** (ID: {row['ID']})")
            st.progress(row['Progresso']/100)
        with col2:
            st.markdown(f"Início: {row['Início']}")
            st.markdown(f"Status: {row['Status']}")
        st.markdown("---")

def render_agent_page(agent_name):
    if agent_name == "Agente Trader":
        key = "trader"
        title = "📈 Agente Trader"
        description = "Sistema de trading algorítmico e análise de mercado"
    elif agent_name == "Escritor de Artigo":
        key = "escritor"
        title = "✍️ Escritor de Artigo"
        description = "Gerador de conteúdo inteligente"
    elif agent_name == "Agente SQL":
        key = "sql"
        title = "🔍 Agente SQL"
        description = "Assistente para consultas e análise de dados"
    elif agent_name == "Sistema de Tarefas":
        key = "tarefa"
        title = "📋 Sistema de Tarefas"
        description = "Orquestrador de fluxos de trabalho"
    else:
        return
    
    st.title(title)
    st.markdown(description)
    
    # Status e controles
    st.subheader("Status e Controles")
    col1, col2, col3 = st.columns([2, 2, 3])
    
    with col1:
        status = get_agent_status(key)
        st.metric(
            "Status", 
            status["status"].upper(),
            delta=None
        )
    
    with col2:
        last_active = datetime.fromisoformat(status["last_active"]).strftime("%d/%m/%Y %H:%M:%S")
        st.metric(
            "Última Atividade",
            last_active,
            delta=None
        )
    
    with col3:
        if status["status"] == "active":
            if st.button("🛑 Parar Agente", key=f"stop_{key}"):
                toggle_agent(key, "stopped")
        else:
            if st.button("▶️ Iniciar Agente", key=f"start_{key}"):
                toggle_agent(key, "active")
        
        if st.button("🔄 Atualizar Status", key=f"refresh_{key}"):
            st.rerun()
    
    # Configurações do Agente
    st.subheader("Configurações")
    config = load_config()
    agent_config = config["agents"][key]
    
    with st.expander("Configurações do Agente"):
        cols = st.columns(2)
        modified = False
        
        for i, (param, value) in enumerate(agent_config.items()):
            with cols[i % 2]:
                if isinstance(value, bool):
                    new_val = st.checkbox(param, value)
                elif isinstance(value, int):
                    new_val = st.number_input(param, value=value)
                elif isinstance(value, float):
                    new_val = st.slider(param, 0.0, 1.0, value)
                else:
                    new_val = st.text_input(param, value)
                
                if new_val != value:
                    modified = True
                    
        if modified:
            if st.button("Salvar Configurações"):
                st.success("Configurações salvas com sucesso!")
    
    # Resultados Recentes
    st.subheader("Resultados Recentes")
    results = get_recent_results(key)
    
    if key == "trader":
        # Tabela de resultados de trading
        if results:
            df = pd.DataFrame(results)
            df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%H:%M:%S')
            df = df.rename(columns={
                'timestamp': 'Horário', 
                'asset': 'Ativo', 
                'action': 'Ação', 
                'price': 'Preço', 
                'confidence': 'Confiança'
            })
            st.dataframe(df, use_container_width=True)
            
            # Gráfico de confiança
            fig = px.bar(
                df, 
                x='Ativo', 
                y='Confiança', 
                color='Ação',
                color_discrete_map={'BUY': 'green', 'SELL': 'red', 'HOLD': 'gray'},
                title='Confiança nas Decisões de Trading'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum resultado disponível para o Agente Trader")
            
    elif key == "escritor":
        # Artigos gerados
        if results:
            for article in results:
                with st.expander(f"{article['title']} ({article['timestamp'].split('T')[0]})"):
                    st.markdown(f"**Tipo:** {article['type']}")
                    st.markdown(f"**Palavras:** {article['words']}")
                    st.markdown("---")
                    st.markdown("**Visualização prévia:**")
                    st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit...")
                    st.button("Visualizar artigo completo", key=f"view_{article['timestamp']}")
        else:
            st.info("Nenhum resultado disponível para o Escritor de Artigo")
            
    elif key == "sql":
        # Consultas SQL
        if results:
            df = pd.DataFrame(results)
            df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%H:%M:%S')
            df = df.rename(columns={
                'timestamp': 'Horário', 
                'database': 'Banco', 
                'query_type': 'Tipo', 
                'rows': 'Linhas', 
                'exec_time': 'Tempo (s)'
            })
            st.dataframe(df, use_container_width=True)
            
            # Gráfico de tempo de execução
            fig = px.bar(
                df, 
                x='Banco', 
                y='Tempo (s)', 
                color='Tipo',
                title='Tempo de Execução por Consulta'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum resultado disponível para o Agente SQL")
            
    elif key == "tarefa":
        # Tarefas executadas
        if results:
            df = pd.DataFrame(results)
            df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%d/%m %H:%M')
            df = df.rename(columns={
                'timestamp': 'Data/Hora', 
                'task_id': 'ID', 
                'status': 'Status', 
                'steps': 'Etapas', 
                'success': 'Sucesso'
            })
            st.dataframe(df, use_container_width=True)
            
            # Visualização de sucesso
            success_count = df['Sucesso'].value_counts()
            fig = px.pie(
                names=['Sucesso', 'Falha'],
                values=[
                    success_count.get(True, 0),
                    success_count.get(False, 0)
                ],
                title='Taxa de Sucesso das Tarefas',
                color_discrete_sequence=['green', 'red']
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum resultado disponível para o Sistema de Tarefas")
    
    # Logs
    st.subheader("Logs do Agente")
    with st.expander("Logs recentes"):
        logs = [
            "2025-03-13 12:30:45 [INFO] Iniciando processo de análise",
            "2025-03-13 12:30:46 [DEBUG] Carregando configurações",
            "2025-03-13 12:30:47 [INFO] Conectando aos serviços externos",
            "2025-03-13 12:30:48 [DEBUG] Parâmetros carregados: {'param1': 'value1'}",
            "2025-03-13 12:30:49 [INFO] Processamento concluído com sucesso"
        ]
        
        for log in logs:
            parts = log.split(" ", 3)
            date, time, level, message = parts[0], parts[1], parts[2], parts[3]
            
            color = "gray"
            if "[INFO]" in level:
                color = "green"
            elif "[DEBUG]" in level:
                color = "blue"
            elif "[WARNING]" in level:
                color = "orange"
            elif "[ERROR]" in level:
                color = "red"
            
            st.markdown(f"""
            <div style="margin-bottom: 2px; font-family: monospace;">
                <span style="color: gray;">{date} {time}</span> 
                <span style="color: {color};">{level}</span> 
                {message}
            </div>
            """, unsafe_allow_html=True)

def render_settings():
    st.title("⚙️ Configurações do Sistema")
    
    # Carregamento das configurações
    config = load_config()
    
    # Configurações gerais
    st.header("Configurações Gerais")
    
    col1, col2 = st.columns(2)
    with col1:
        log_level = st.selectbox(
            "Nível de Log",
            ["DEBUG", "INFO", "WARNING", "ERROR"],
            index=["DEBUG", "INFO", "WARNING", "ERROR"].index(config["general"]["log_level"])
        )
    
    with col2:
        enable_telemetry = st.checkbox(
            "Habilitar Telemetria",
            value=config["general"]["enable_telemetry"]
        )
    
    theme = st.radio(
        "Tema da Interface",
        ["light", "dark"],
        horizontal=True,
        index=["light", "dark"].index(config["general"]["theme"])
    )
    
    # Configurações específicas dos agentes
    st.header("Configurações dos Agentes")
    
    tabs = st.tabs(["Trader", "Escritor", "SQL", "Tarefa"])
    
    with tabs[0]:
        st.subheader("Configurações do Agente Trader")
        auto_start_trader = st.checkbox(
            "Iniciar Automaticamente",
            value=config["agents"]["trader"]["auto_start"]
        )
        refresh_interval = st.slider(
            "Intervalo de Atualização (segundos)",
            min_value=5,
            max_value=300,
            value=config["agents"]["trader"]["refresh_interval"],
            step=5
        )
        
        st.text_area("Observações do Trader", "")
    
    with tabs[1]:
        st.subheader("Configurações do Escritor de Artigo")
        auto_start_escritor = st.checkbox(
            "Iniciar Automaticamente",
            value=config["agents"]["escritor"]["auto_start"]
        )
        max_tokens = st.number_input(
            "Máximo de Tokens",
            min_value=100,
            max_value=10000,
            value=config["agents"]["escritor"]["max_tokens"],
            step=100
        )
        
        st.text_area("Observações do Escritor", "")
    
    with tabs[2]:
        st.subheader("Configurações do Agente SQL")
        auto_start_sql = st.checkbox(
            "Iniciar Automaticamente",
            value=config["agents"]["sql"]["auto_start"]
        )
        max_db_connections = st.number_input(
            "Máximo de Conexões",
            min_value=1,
            max_value=10,
            value=config["agents"]["sql"]["max_db_connections"],
            step=1
        )
        
        st.text_area("Observações do SQL", "")
    
    with tabs[3]:
        st.subheader("Configurações do Sistema de Tarefas")
        auto_start_tarefa = st.checkbox(
            "Iniciar Automaticamente",
            value=config["agents"]["tarefa"]["auto_start"]
        )
        parallelism = st.number_input(
            "Nível de Paralelismo",
            min_value=1,
            max_value=16,
            value=config["agents"]["tarefa"]["parallelism"],
            step=1
        )
        
        st.text_area("Observações das Tarefas", "")
    
    # Botões de ação
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Salvar Configurações", use_container_width=True):
            st.success("Configurações salvas com sucesso!")
    with col2:
        if st.button("🔄 Restaurar Padrão", use_container_width=True):
            st.info("Configurações restauradas para o padrão.")
    with col3:
        if st.button("🔧 Testar Conexão", use_container_width=True):
            with st.spinner("Testando conexão..."):
                time.sleep(1)
                st.success("Conexão estabelecida com sucesso!")

# Aplicação principal
def main():
    page = render_sidebar()
    
    if page == "Dashboard":
        render_dashboard()
    elif page == "Configurações":
        render_settings()
    else:
        render_agent_page(page)

if __name__ == "__main__":
    main()
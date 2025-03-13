#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface Unificada para Sistema de Agentes
-------------------------------------------

Este módulo implementa uma interface web centralizada para gerenciar
e monitorar todos os agentes do sistema.
"""

import os
import sys
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv

# Configurando caminhos para os módulos dos agentes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar serviços e controladores
# Nota: Estes arquivos serão criados posteriormente
from controllers.trader import trader_bp
from controllers.writer import writer_bp
from controllers.sql import sql_bp
from controllers.tasks import tasks_bp
from services.agent_manager import AgentManager
from services.notification import NotificationService

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("interface/logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Inicialização da aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-secreta-temporaria')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///agents.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do SocketIO para comunicação em tempo real
socketio = SocketIO(app)

# Serviços
agent_manager = AgentManager()
notification_service = NotificationService(socketio)

# Registrar blueprints dos controladores
app.register_blueprint(trader_bp, url_prefix='/trader')
app.register_blueprint(writer_bp, url_prefix='/writer')
app.register_blueprint(sql_bp, url_prefix='/sql')
app.register_blueprint(tasks_bp, url_prefix='/tasks')

# Rota principal - Dashboard
@app.route('/')
def index():
    """Página principal da interface que exibe o dashboard."""
    agents = agent_manager.get_all_agents_status()
    return render_template('index.html', 
                          agents=agents, 
                          current_time=datetime.now())

# Rotas para API de agentes
@app.route('/api/agents', methods=['GET'])
def get_all_agents():
    """Retorna informações sobre todos os agentes."""
    try:
        agents = agent_manager.get_all_agents_status()
        return jsonify({"success": True, "agents": agents})
    except Exception as e:
        logger.error(f"Erro ao obter agentes: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/agents/<agent_id>', methods=['GET'])
def get_agent(agent_id):
    """Retorna informações detalhadas sobre um agente específico."""
    try:
        agent = agent_manager.get_agent_details(agent_id)
        if agent:
            return jsonify({"success": True, "agent": agent})
        return jsonify({"success": False, "error": "Agente não encontrado"}), 404
    except Exception as e:
        logger.error(f"Erro ao obter agente {agent_id}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/agents/<agent_id>/start', methods=['POST'])
def start_agent(agent_id):
    """Inicia um agente específico."""
    try:
        success = agent_manager.start_agent(agent_id)
        return jsonify({"success": success})
    except Exception as e:
        logger.error(f"Erro ao iniciar agente {agent_id}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/agents/<agent_id>/stop', methods=['POST'])
def stop_agent(agent_id):
    """Para um agente específico."""
    try:
        success = agent_manager.stop_agent(agent_id)
        return jsonify({"success": success})
    except Exception as e:
        logger.error(f"Erro ao parar agente {agent_id}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

# Rota para configuração
@app.route('/config', methods=['GET', 'POST'])
def config():
    """Página de configuração dos agentes."""
    if request.method == 'POST':
        try:
            # Processar alterações na configuração
            agent_id = request.form.get('agent_id')
            config_data = request.form.to_dict()
            success = agent_manager.update_agent_config(agent_id, config_data)
            
            if success:
                flash("Configuração atualizada com sucesso!", "success")
            else:
                flash("Erro ao atualizar configuração.", "error")
                
            return redirect(url_for('config'))
            
        except Exception as e:
            logger.error(f"Erro ao atualizar configuração: {str(e)}")
            flash(f"Erro ao atualizar configuração: {str(e)}", "error")
            return redirect(url_for('config'))
    
    # Método GET - exibir página de configuração
    agents_config = agent_manager.get_all_agents_config()
    return render_template('config.html', agents_config=agents_config)

# Rotas para fluxos de trabalho
@app.route('/workflows', methods=['GET'])
def workflows():
    """Página de gerenciamento de fluxos de trabalho."""
    workflow_list = agent_manager.get_workflows()
    return render_template('workflows.html', workflows=workflow_list)

@app.route('/workflows/new', methods=['GET', 'POST'])
def new_workflow():
    """Página para criação de novos fluxos de trabalho."""
    if request.method == 'POST':
        try:
            workflow_data = request.json
            workflow_id = agent_manager.create_workflow(workflow_data)
            return jsonify({"success": True, "workflow_id": workflow_id})
        except Exception as e:
            logger.error(f"Erro ao criar fluxo de trabalho: {str(e)}")
            return jsonify({"success": False, "error": str(e)}), 500
    
    # Método GET - exibir página de criação de fluxo
    agents = agent_manager.get_all_agents_status()
    return render_template('workflow_editor.html', agents=agents)

# Comunicação em tempo real via WebSocket
@socketio.on('connect')
def handle_connect():
    """Ação realizada quando um cliente se conecta via WebSocket."""
    logger.info(f"Cliente conectado: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    """Ação realizada quando um cliente se desconecta."""
    logger.info(f"Cliente desconectado: {request.sid}")

@socketio.on('subscribe')
def handle_subscribe(data):
    """Inscreve o cliente para receber atualizações de um agente específico."""
    agent_id = data.get('agent_id')
    if agent_id:
        logger.info(f"Cliente {request.sid} inscrito para atualizações do agente {agent_id}")
        # Lógica para adicionar cliente à lista de inscritos

# Tratamento de erros
@app.errorhandler(404)
def page_not_found(e):
    """Tratamento para páginas não encontradas."""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Tratamento para erros internos do servidor."""
    logger.error(f"Erro interno do servidor: {str(e)}")
    return render_template('errors/500.html'), 500

# Inicialização da aplicação
if __name__ == '__main__':
    # Garantir que o diretório de logs existe
    os.makedirs('interface/logs', exist_ok=True)
    
    # Inicializar serviços e componentes
    logger.info("Iniciando Interface Unificada de Agentes")
    
    # Iniciar servidor
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    socketio.run(app, host='0.0.0.0', port=port, debug=debug)

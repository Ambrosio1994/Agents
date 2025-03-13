"""
API Backend para o Sistema de Agentes
Implementação com FastAPI

Author: Ambrosio1994
Data: Março, 2025
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os
import sys
import logging
import time
from datetime import datetime, timedelta
import uuid
import importlib
import subprocess
import yaml
from pathlib import Path

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("agents-api")

# Criação da aplicação FastAPI
app = FastAPI(
    title="API do Sistema de Agentes",
    description="Backend para o Sistema de Agentes Autônomos",
    version="1.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para dados
class AgentStatus(BaseModel):
    name: str
    status: str
    last_active: Optional[str] = None
    cpu: Optional[float] = None
    memory: Optional[float] = None
    details: Optional[Dict[str, Any]] = None

class TaskCreate(BaseModel):
    description: str
    agent: str
    parameters: Optional[Dict[str, Any]] = None
    schedule: Optional[str] = None

class TaskStatus(BaseModel):
    id: str
    description: str
    agent: str
    status: str
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None

class AgentConfig(BaseModel):
    auto_start: Optional[bool] = False
    parameters: Optional[Dict[str, Any]] = None

class SystemConfig(BaseModel):
    log_level: Optional[str] = "INFO"
    enable_telemetry: Optional[bool] = False
    theme: Optional[str] = "light"

class ConfigUpdate(BaseModel):
    general: Optional[SystemConfig] = None
    agents: Optional[Dict[str, AgentConfig]] = None

# Simulação de armazenamento em memória
agent_processes = {}
active_tasks = {}

# Funções auxiliares
def load_config():
    """Carrega configurações do sistema"""
    # Em implementação real, carregar do arquivo
    config = {
        "general": {
            "log_level": "INFO",
            "enable_telemetry": False,
            "theme": "light"
        },
        "agents": {
            "trader": {
                "auto_start": False,
                "parameters": {
                    "refresh_interval": 60,
                    "risk_level": "medium"
                }
            },
            "escritor": {
                "auto_start": False,
                "parameters": {
                    "max_tokens": 2000,
                    "model": "gemini-pro"
                }
            },
            "sql": {
                "auto_start": False,
                "parameters": {
                    "max_db_connections": 3,
                    "timeout": 30
                }
            },
            "tarefa": {
                "auto_start": False,
                "parameters": {
                    "parallelism": 4,
                    "max_retries": 3
                }
            }
        }
    }
    return config

def save_config(config):
    """Salva configurações do sistema"""
    # Em implementação real, salvar no arquivo
    logger.info("Configuração salva com sucesso")
    return True

def get_agent_module_path(agent_name):
    """Retorna o caminho para o módulo do agente"""
    agent_paths = {
        "trader": "../agente-trader/main.py",
        "escritor": "../escritor-de-artigo/multi_agentes_writer_critic.py",
        "sql": "../agente-sql/main.py",
        "tarefa": "../tarefa/main.py"
    }
    return agent_paths.get(agent_name)

def start_agent_process(agent_name):
    """Inicia um agente como processo separado"""
    # Simulação - em implementação real, use subprocess
    module_path = get_agent_module_path(agent_name)
    if not module_path:
        raise ValueError(f"Agente {agent_name} não encontrado")
    
    logger.info(f"Iniciando agente {agent_name} de {module_path}")
    
    # Simula criação de processo
    process_id = str(uuid.uuid4())
    agent_processes[agent_name] = {
        "id": process_id,
        "started_at": datetime.now().isoformat(),
        "status": "active",
        "last_active": datetime.now().isoformat(),
        "cpu": 0.2,
        "memory": 0.15
    }
    
    logger.info(f"Agente {agent_name} iniciado com ID {process_id}")
    return process_id

def stop_agent_process(agent_name):
    """Para um agente em execução"""
    if agent_name not in agent_processes:
        raise ValueError(f"Agente {agent_name} não está em execução")
    
    logger.info(f"Parando agente {agent_name}")
    
    # Simula parada de processo
    process_data = agent_processes[agent_name]
    process_data["status"] = "stopped"
    process_data["last_active"] = datetime.now().isoformat()
    
    logger.info(f"Agente {agent_name} parado")
    return True

def get_agent_status(agent_name):
    """Obtém status de um agente"""
    # Simulação - em implementação real, verificar processo
    if agent_name in agent_processes:
        process_data = agent_processes[agent_name]
        return AgentStatus(
            name=agent_name,
            status=process_data["status"],
            last_active=process_data["last_active"],
            cpu=process_data["cpu"],
            memory=process_data["memory"]
        )
    else:
        # Agente não está rodando
        return AgentStatus(
            name=agent_name,
            status="stopped",
            last_active=None,
            cpu=0.0,
            memory=0.0
        )

def get_all_agent_status():
    """Obtém status de todos os agentes"""
    agents = ["trader", "escritor", "sql", "tarefa"]
    return [get_agent_status(agent) for agent in agents]

def create_task(task_create: TaskCreate):
    """Cria uma nova tarefa para um agente"""
    task_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    
    task = {
        "id": task_id,
        "description": task_create.description,
        "agent": task_create.agent,
        "status": "pending",
        "created_at": now,
        "started_at": None,
        "completed_at": None,
        "parameters": task_create.parameters or {},
        "result": None,
        "error": None
    }
    
    active_tasks[task_id] = task
    logger.info(f"Tarefa {task_id} criada para o agente {task_create.agent}")
    
    return task_id

def get_task_status(task_id):
    """Obtém status de uma tarefa"""
    if task_id not in active_tasks:
        raise ValueError(f"Tarefa {task_id} não encontrada")
    
    task = active_tasks[task_id]
    return TaskStatus(
        id=task["id"],
        description=task["description"],
        agent=task["agent"],
        status=task["status"],
        created_at=task["created_at"],
        started_at=task["started_at"],
        completed_at=task["completed_at"],
        result=task["result"],
        error=task["error"]
    )

# Rotas da API
@app.get("/")
def read_root():
    """Endpoint raiz da API"""
    return {
        "name": "Sistema de Agentes API",
        "version": "1.0.0",
        "status": "online",
        "documentation": "/docs"
    }

@app.get("/agents", response_model=List[AgentStatus])
def list_agents():
    """Lista todos os agentes e seus status"""
    return get_all_agent_status()

@app.get("/agents/{agent_name}", response_model=AgentStatus)
def get_agent(agent_name: str):
    """Obtém status de um agente específico"""
    try:
        return get_agent_status(agent_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/agents/{agent_name}/start")
def start_agent(agent_name: str):
    """Inicia um agente específico"""
    try:
        process_id = start_agent_process(agent_name)
        return {
            "agent": agent_name,
            "process_id": process_id,
            "status": "started"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agents/{agent_name}/stop")
def stop_agent(agent_name: str):
    """Para um agente específico"""
    try:
        success = stop_agent_process(agent_name)
        return {
            "agent": agent_name,
            "status": "stopped",
            "success": success
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks", response_model=dict)
def create_new_task(task: TaskCreate):
    """Cria uma nova tarefa"""
    try:
        task_id = create_task(task)
        return {
            "task_id": task_id,
            "status": "created"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks/{task_id}", response_model=TaskStatus)
def get_task(task_id: str):
    """Obtém status de uma tarefa específica"""
    try:
        return get_task_status(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/tasks", response_model=List[TaskStatus])
def list_tasks():
    """Lista todas as tarefas ativas"""
    return [get_task_status(task_id) for task_id in active_tasks]

@app.get("/config")
def get_config():
    """Obtém configurações do sistema"""
    return load_config()

@app.patch("/config")
def update_config(config_update: ConfigUpdate):
    """Atualiza configurações do sistema"""
    try:
        current_config = load_config()
        
        # Atualiza configurações gerais se fornecidas
        if config_update.general:
            current_config["general"].update(config_update.general.dict(exclude_unset=True))
        
        # Atualiza configurações de agentes se fornecidas
        if config_update.agents:
            for agent_name, agent_config in config_update.agents.items():
                if agent_name in current_config["agents"]:
                    current_config["agents"][agent_name].update(agent_config.dict(exclude_unset=True))
        
        # Salva configurações atualizadas
        save_config(current_config)
        
        return {
            "status": "updated",
            "config": current_config
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_system_stats():
    """Obtém estatísticas do sistema"""
    # Simulação - em implementação real, coletar métricas reais
    return {
        "cpu": 24.5,
        "memory": {
            "total": "16.0 GB",
            "used": "1.2 GB",
            "percentage": 7.5
        },
        "disk": {
            "total": "512.0 GB",
            "used": "125.3 GB",
            "percentage": 24.5
        },
        "uptime": "3 days, 5 hours",
        "agents": {
            "total": 4,
            "active": len([a for a in agent_processes.values() if a["status"] == "active"])
        },
        "tasks": {
            "total": len(active_tasks),
            "pending": len([t for t in active_tasks.values() if t["status"] == "pending"]),
            "in_progress": len([t for t in active_tasks.values() if t["status"] == "in_progress"]),
            "completed": len([t for t in active_tasks.values() if t["status"] == "completed"]),
            "failed": len([t for t in active_tasks.values() if t["status"] == "failed"])
        }
    }

@app.get("/logs/{agent_name}")
def get_agent_logs(agent_name: str, limit: int = 10):
    """Obtém logs de um agente específico"""
    # Simulação - em implementação real, ler logs reais
    logs = [
        {"timestamp": "2025-03-13T12:30:45", "level": "INFO", "message": "Iniciando processo de análise"},
        {"timestamp": "2025-03-13T12:30:46", "level": "DEBUG", "message": "Carregando configurações"},
        {"timestamp": "2025-03-13T12:30:47", "level": "INFO", "message": "Conectando aos serviços externos"},
        {"timestamp": "2025-03-13T12:30:48", "level": "DEBUG", "message": "Parâmetros carregados: {'param1': 'value1'}"},
        {"timestamp": "2025-03-13T12:30:49", "level": "INFO", "message": "Processamento concluído com sucesso"}
    ]
    return {"agent": agent_name, "logs": logs[:limit]}

# Função para iniciar a aplicação
def start():
    """Inicia a aplicação FastAPI com uvicorn"""
    # Simulação de inicialização automática de agentes
    config = load_config()
    for agent_name, agent_config in config["agents"].items():
        if agent_config.get("auto_start", False):
            try:
                logger.info(f"Iniciando automaticamente o agente {agent_name}")
                start_agent_process(agent_name)
            except Exception as e:
                logger.error(f"Erro ao iniciar o agente {agent_name}: {str(e)}")
    
    logger.info("API do Sistema de Agentes iniciada com sucesso")

# Execução da aplicação
if __name__ == "__main__":
    import uvicorn
    start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
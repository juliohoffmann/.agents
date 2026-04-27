from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Dict, Any, Optional
import os

from .schemas.agentSchema import CreateAgentSchema, SimulateTradeSchema
from .controllers.AgentController import AgentController, store, simulate
from .middlewares.authMiddleware import AuthMiddleware, auth_middleware, require_admin


router = APIRouter()


# Middleware de autenticação
def get_auth_middleware():
    secret = os.getenv("JWT_SECRET", "default_secret_key")
    return AuthMiddleware(secret)


@router.post("/agents", status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: CreateAgentSchema,
    request: Request
):
    """Cria um novo agente"""
    # Autenticação opcional para desenvolvimento
    auth = get_auth_middleware()
    user = auth.get_current_user(request)
    
    # Se tiver usuário autenticado, associar ao agente
    agent = await AgentController.create_agent(
        name=agent_data.name,
        initial_balance=agent_data.initialBalance,
        symbol=agent_data.symbol
    )
    
    if user:
        agent["owner"] = user.get("uid")
    
    return agent


@router.post("/agents/simulate")
async def simulate_trades(
    data: SimulateTradeSchema,
    request: Request
):
    """Rota para simulação de trades"""
    # Autenticação opcional
    auth = get_auth_middleware()
    user = auth.get_current_user(request)
    
    # Verificar se agente existe
    agent = await AgentController.get_agent(data.agentId)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agente não encontrado"
        )
    
    # Verificar propriedade (se autenticado)
    if user and agent.get("owner") and agent["owner"] != user.get("uid"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado ao agente"
        )
    
    # Executar simulação
    result = await AgentController.simulate_trades(data.agentId, data.numTrades)
    return result


@router.get("/agents")
async def list_agents(request: Request):
    """Lista todos os agentes"""
    return await AgentController.list_agents()


@router.get("/agents/{agent_id}")
async def get_agent(agent_id: str, request: Request):
    """Retorna agente específico"""
    agent = await AgentController.get_agent(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agente não encontrado"
        )
    return agent


@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str, request: Request):
    """Deleta um agente"""
    auth = get_auth_middleware()
    user = auth.get_current_user(request)
    
    agent = await AgentController.get_agent(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agente não encontrado"
        )
    
    # Verificar propriedade
    if user and agent.get("owner") and agent["owner"] != user.get("uid"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    success = await AgentController.delete_agent(agent_id)
    if success:
        return {"message": "Agente deletado com sucesso"}
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Erro ao deletar agente"
    )


@router.get("/agents/{agent_id}/trades")
async def get_agent_trades(agent_id: str):
    """Retorna trades de um agente"""
    agent = await AgentController.get_agent(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agente não encontrado"
        )
    
    trades = await AgentController.get_trades(agent_id)
    return {"agentId": agent_id, "trades": trades}
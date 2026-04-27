from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import subprocess
from pydantic import BaseModel


# Banco de dados em memória (simulando MongoDB/Prisma)
agents_db: Dict[str, Dict[str, Any]] = {}
trades_db: Dict[str, List[Dict[str, Any]]] = {}


class AgentController:
    """Controller para gerenciamento de agentes"""
    
    @staticmethod
    async def create_agent(name: str, initial_balance: float = 100.0, symbol: str = "ETHUSDT") -> Dict[str, Any]:
        """Cria um novo agente"""
        agent_id = f"agent_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(agents_db)}"
        
        agent = {
            "id": agent_id,
            "name": name,
            "initialBalance": initial_balance,
            "symbol": symbol,
            "balance": initial_balance,
            "createdAt": datetime.now().isoformat(),
            "status": "active"
        }
        
        agents_db[agent_id] = agent
        trades_db[agent_id] = []
        
        return agent
    
    @staticmethod
    async def get_agent(agent_id: str) -> Optional[Dict[str, Any]]:
        """Retorna agente pelo ID"""
        return agents_db.get(agent_id)
    
    @staticmethod
    async def list_agents() -> List[Dict[str, Any]]:
        """Lista todos os agentes"""
        return list(agents_db.values())
    
    @staticmethod
    async def update_agent(agent_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Atualiza dados do agente"""
        if agent_id in agents_db:
            agents_db[agent_id].update(data)
            return agents_db[agent_id]
        return None
    
    @staticmethod
    async def delete_agent(agent_id: str) -> bool:
        """Deleta um agente"""
        if agent_id in agents_db:
            del agents_db[agent_id]
            if agent_id in trades_db:
                del trades_db[agent_id]
            return True
        return False
    
    @staticmethod
    async def simulate_trades(agent_id: str, num_trades: int = 1) -> Dict[str, Any]:
        """Executa simulação de trades via verdent.py"""
        agent = agents_db.get(agent_id)
        if not agent:
            return {"error": "Agente não encontrado"}
        
        try:
            # Executar simulação via subprocess
            result = subprocess.run(
                ["python", "verdent.py", "--agentId", agent_id, "--numTrades", str(num_trades), "--symbol", agent["symbol"]],
                capture_output=True,
                text=True,
                timeout=60,
                cwd="."
            )
            
            if result.stdout:
                results = json.loads(result.stdout)
            else:
                results = {"balance": agent["balance"], "trades": []}
                
        except Exception as e:
            results = {"balance": agent["balance"], "trades": [], "error": str(e)}
        
        # Atualizar balance do agente
        new_balance = results.get("balance", agent["balance"])
        agent["balance"] = new_balance
        
        # Salvar trades
        for trade in results.get("trades", []):
            trades_db[agent_id].append({
                **trade,
                "timestamp": datetime.now().isoformat()
            })
        
        # Deletar agente se balance < 30
        if new_balance < 30:
            await AgentController.delete_agent(agent_id)
            return {"message": "Agente deletado por saldo insuficiente", "balance": new_balance}
        
        return {
            "agent": agent,
            "trades": results.get("trades", []),
            "balance": new_balance
        }
    
    @staticmethod
    async def get_trades(agent_id: str) -> List[Dict[str, Any]]:
        """Retorna trades de um agente"""
        return trades_db.get(agent_id, [])


# Funções de convenience para uso em rotas
async def store(name: str, initial_balance: float = 100.0, symbol: str = "ETHUSDT") -> Dict[str, Any]:
    """Cria novo agente - wrapper para rotas"""
    return await AgentController.create_agent(name, initial_balance, symbol)


async def simulate(agent_id: str, num_trades: int = 1) -> Dict[str, Any]:
    """Executa simulação - wrapper para rotas"""
    return await AgentController.simulate_trades(agent_id, num_trades)
import uuid
from typing import List, Dict, Any


class BaseAgent:
    """Classe base para agentes"""
    
    def __init__(self, name: str, role: str, goal: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role
        self.goal = goal
        self.tasks: List[str] = []
    
    def execute_task(self, task: str) -> str:
        """Executa uma tarefa"""
        print(f"[{self.name} - {self.role}] Executando: {task}")
        return f"Resultado da tarefa '{task}' completado por {self.name}."
    
    def add_task(self, task: str):
        """Adiciona tarefa à lista"""
        self.tasks.append(task)
    
    def get_tasks(self) -> List[str]:
        """Retorna lista de tarefas"""
        return self.tasks


class CEOAgent(BaseAgent):
    """Agente CEO que orquestra outros agentes"""
    
    def __init__(self, name: str):
        super().__init__(
            name,
            "Chief Executive Officer",
            "Orquestrar a organização e garantir a execução de objetivos complexos."
        )
        self.team: Dict[str, BaseAgent] = {}
    
    def hire_agent(self, name: str, role: str, goal: str) -> "BaseAgent":
        """Instancia e adiciona um novo agente à organização"""
        print(f"[{self.name}] Contratando novo agente: {name} para o cargo de {role}...")
        new_agent = BaseAgent(name, role, goal)
        self.team[new_agent.id] = new_agent
        return new_agent
    
    def fire_agent(self, agent_id: str) -> bool:
        """Remove um agente da organização"""
        if agent_id in self.team:
            agent = self.team[agent_id]
            print(f"[{self.name}] Demitindo agente: {agent.name}")
            del self.team[agent_id]
            return True
        return False
    
    def delegate_tasks(self, plan: Dict[str, List[str]]) -> List[str]:
        """Recebe um plano onde a chave é o ID do agente e o valor é um array de tarefas"""
        results: List[str] = []
        
        for agent_id, tasks in plan.items():
            agent = self.team.get(agent_id)
            if agent:
                for task in tasks:
                    results.append(agent.execute_task(task))
        
        return results
    
    def get_team_info(self) -> List[Dict[str, Any]]:
        """Retorna informações da equipe"""
        return [
            {
                "id": agent.id,
                "name": agent.name,
                "role": agent.role,
                "goal": agent.goal,
                "tasks": agent.tasks
            }
            for agent in self.team.values()
        ]


# Exemplo de uso
if __name__ == "__main__":
    ceo = CEOAgent("Julio CEO")
    
    dev = ceo.hire_agent("DevBot", "Senior Developer", "Escrever código Python limpo")
    qa = ceo.hire_agent("TesterBot", "QA Engineer", "Garantir a qualidade do código")
    devops = ceo.hire_agent("DevOpsBot", "DevOps Engineer", "Manter infraestrutura")
    
    ceo.delegate_tasks({
        dev.id: ["Implementar API de autenticação", "Configurar banco de dados"],
        qa.id: ["Criar testes unitários para API"],
        devops.id: ["Configurar CI/CD", "Monitorar serviços"]
    })
    
    print("\n--- Equipe ---")
    for member in ceo.get_team_info():
        print(f"- {member['name']} ({member['role']}): {len(member['tasks'])} tarefas")
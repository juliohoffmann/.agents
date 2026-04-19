import { randomUUID } from 'crypto';

class BaseAgent {
    public id: string;
    public name: string;
    public role: string;
    public goal: string;
    public tasks: string[];

    constructor(name: string, role: string, goal: string) {
        this.id = randomUUID();
        this.name = name;
        this.role = role;
        this.goal = goal;
        this.tasks = [];
    }

    public executeTask(task: string): string {
        console.log(`[${this.name} - ${this.role}] Executando: ${task}`);
        return `Resultado da tarefa '${task}' completado por ${this.name}.`;
    }
}

class CEOAgent extends BaseAgent {
    private team: Map<string, BaseAgent>;

    constructor(name: string) {
        super(
            name,
            "Chief Executive Officer",
            "Orquestrar a organização e garantir a execução de objetivos complexos."
        );
        this.team = new Map<string, BaseAgent>();
    }

    /**
     * Instancia e adiciona um novo agente à organização.
     */
    public hireAgent(name: string, role: string, goal: string): BaseAgent {
        console.log(`[${this.name}] Contratando novo agente: ${name} para o cargo de ${role}...`);
        const newAgent = new BaseAgent(name, role, goal);
        this.team.set(newAgent.id, newAgent);
        return newAgent;
    }

    /**
     * Recebe um plano onde a chave é o ID do agente e o valor é um array de tarefas.
     */
    public delegateTasks(plan: Record<string, string[]>): string[] {
        const results: string[] = [];
        
        for (const [agentId, tasks] of Object.entries(plan)) {
            const agent = this.team.get(agentId);
            if (agent) {
                tasks.forEach(task => {
                    results.push(agent.executeTask(task));
                });
            }
        }
        return results;
    }
}

// Exemplo de uso
const ceo = new CEOAgent("Julio CEO");

const dev = ceo.hireAgent("DevBot", "Senior Developer", "Escrever código TS limpo");
const qa = ceo.hireAgent("TesterBot", "QA Engineer", "Garantir a qualidade do código");

ceo.delegateTasks({
    [dev.id]: ["Implementar API de autenticação", "Configurar banco de dados"],
    [qa.id]: ["Criar testes unitários para API"]
});

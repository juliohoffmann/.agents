import { Request, Response } from 'express';
import { prisma } from '../config/prisma'; // Importa prisma configurado
import { createAgentSchema, simulateTradeSchema } from '../schemas/agentSchema';
import ccxt from 'ccxt';
import { exec } from 'child_process';
import util from 'util';
import ExcelJS from 'exceljs';
const execPromise = util.promisify(exec);

const exchange = new ccxt.binance({ /* Config de Testnet do seu .env */ });

export const store = async (req: Request, res: Response) => {
  try {
    const data = await createAgentSchema.validate(req.body);
    const agent = await prisma.agent.create({ data });
    res.json(agent);
  } catch (err) {
    res.status(400).json({ error: 'Erro na criação' });
  }
};

export const simulate = async (req: Request, res: Response) => {
  try {
    const { agentId, numTrades } = await simulateTradeSchema.validate(req.body);
    const agent = await prisma.agent.findUnique({ where: { id: agentId } });
    if (!agent) return res.status(404).json({ error: 'Agente não encontrado' });

    // Rodar simulação via child_process (integra lógica Python do seu verdent.py)
    const { stdout } = await execPromise(`python ../verdent.py --agentId ${agentId} --numTrades ${numTrades} --symbol ${agent.symbol}`);
    const results = JSON.parse(stdout); // Assuma que Python retorna JSON com trades, balance, etc.

    // Atualizar balance e logs no MongoDB
    await prisma.agent.update({ where: { id: agentId }, data: { balance: results.balance } });
    for (const trade of results.trades) {
      await prisma.tradeLog.create({ data: { agentId, ...trade } });
    }

    // Otimização e deleção
    if (results.balance < 30) {
      await prisma.agent.delete({ where: { id: agentId } });
      return res.json({ message: 'Agente deletado' });
    }

    // Exportar para planilha
    const workbook = new ExcelJS.Workbook();
    const sheet = workbook.addWorksheet(`Agent_${agentId}`);
    sheet.addRow(['Timestamp', 'Profit', 'Features']);
    results.trades.forEach((t: any) => sheet.addRow([t.timestamp, t.profit, JSON.stringify(t.features)]));
    await workbook.xlsx.writeFile(`results_${agentId}.xlsx`);

    res.json({ results, message: 'Simulação concluída, planilha gerada' });
  } catch (err) {
    res.status(500).json({ error: 'Erro na simulação' });
  }
};
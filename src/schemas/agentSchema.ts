import * as Yup from 'yup';

export const createAgentSchema = Yup.object().shape({
  name: Yup.string().required('Nome do agente obrigatório'),
  initialBalance: Yup.number().default(100).min(100).required(),
  symbol: Yup.string().default('ETHUSDT').required(),
});

export const simulateTradeSchema = Yup.object().shape({
  agentId: Yup.string().required(),
  numTrades: Yup.number().default(1).min(1).required(),
});
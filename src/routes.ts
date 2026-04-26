import { Router } from 'express';
import { authMiddleware, adminMiddleware } from './middlewares/authMiddleware';
import { store, simulate } from './controllers/AgentController';

const router = Router();

router.post('/agents', authMiddleware, adminMiddleware, store);
router.post('/agents/simulate', authMiddleware, simulate); // Rota para simulação

export default router;
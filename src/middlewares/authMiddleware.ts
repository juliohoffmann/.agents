import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import admin from 'firebase-admin'; // Inicialize em app.ts

export const authMiddleware = async (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Token não fornecido' });

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as { uid: string };
    const user = await admin.auth().getUser(decoded.uid);
    req.userId = user.uid;
    req.admin = user.customClaims?.admin || false;
    next();
  } catch (err) {
    res.status(401).json({ error: 'Token inválido' });
  }
};

export const adminMiddleware = (req: Request, res: Response, next: NextFunction) => {
  if (!req.admin) return res.status(403).json({ error: 'Acesso negado' });
  next();
};
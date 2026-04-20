import type { NextFunction, Request, Response } from 'express';
import { ACCESS_COOKIE } from '../utils/cookies.js';
import { verifyAccessToken } from '../utils/jwt.js';

export type AuthedRequest = Request & { user: { id: string; email: string } };

export function requireAuth(req: Request, res: Response, next: NextFunction) {
  const token = req.cookies?.[ACCESS_COOKIE];
  if (!token) return res.status(401).json({ error: 'UNAUTHORIZED' });
  try {
    const payload = verifyAccessToken(token);
    (req as AuthedRequest).user = { id: payload.sub, email: payload.email };
    return next();
  } catch {
    return res.status(401).json({ error: 'UNAUTHORIZED' });
  }
}


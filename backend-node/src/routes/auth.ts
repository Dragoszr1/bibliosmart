import { Router } from 'express';
import bcrypt from 'bcryptjs';
import { z } from 'zod';
import { prisma } from '../utils/prisma.js';
import { baseCookieOptions, ACCESS_COOKIE, REFRESH_COOKIE } from '../utils/cookies.js';
import { signAccessToken, signRefreshToken, verifyAccessToken, verifyRefreshToken } from '../utils/jwt.js';

export const authRouter = Router();

const registerSchema = z.object({
  email: z.string().email().max(254),
  password: z.string().min(8).max(72),
});

const loginSchema = registerSchema;

function setAuthCookies(res: any, tokenPayload: { sub: string; email: string }) {
  const access = signAccessToken(tokenPayload);
  const refresh = signRefreshToken(tokenPayload);
  res.cookie(ACCESS_COOKIE, access, { ...baseCookieOptions(), maxAge: 15 * 60 * 1000 });
  res.cookie(REFRESH_COOKIE, refresh, { ...baseCookieOptions(), maxAge: 30 * 24 * 60 * 60 * 1000 });
}

authRouter.post('/register', async (req, res) => {
  const parsed = registerSchema.safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ error: 'INVALID_INPUT', issues: parsed.error.issues });
  const { email, password } = parsed.data;

  const existing = await prisma.user.findUnique({ where: { email } });
  if (existing) return res.status(409).json({ error: 'EMAIL_IN_USE' });

  const passwordHash = await bcrypt.hash(password, 12);
  const user = await prisma.user.create({ data: { email, passwordHash } });

  setAuthCookies(res, { sub: user.id, email: user.email });
  res.json({ user: { id: user.id, email: user.email, createdAt: user.createdAt } });
});

authRouter.post('/login', async (req, res) => {
  const parsed = loginSchema.safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ error: 'INVALID_INPUT', issues: parsed.error.issues });
  const { email, password } = parsed.data;

  const user = await prisma.user.findUnique({ where: { email } });
  if (!user) return res.status(401).json({ error: 'INVALID_CREDENTIALS' });

  const ok = await bcrypt.compare(password, user.passwordHash);
  if (!ok) return res.status(401).json({ error: 'INVALID_CREDENTIALS' });

  setAuthCookies(res, { sub: user.id, email: user.email });
  res.json({ user: { id: user.id, email: user.email, createdAt: user.createdAt } });
});

authRouter.post('/logout', async (_req, res) => {
  res.clearCookie(ACCESS_COOKIE, baseCookieOptions());
  res.clearCookie(REFRESH_COOKIE, baseCookieOptions());
  res.json({ ok: true });
});

authRouter.post('/refresh', async (req, res) => {
  const token = req.cookies?.[REFRESH_COOKIE];
  if (!token) return res.status(401).json({ error: 'UNAUTHORIZED' });
  try {
    const payload = verifyRefreshToken(token);
    // Optional hardening: check user still exists
    const user = await prisma.user.findUnique({ where: { id: payload.sub } });
    if (!user) return res.status(401).json({ error: 'UNAUTHORIZED' });

    setAuthCookies(res, { sub: user.id, email: user.email });
    res.json({ ok: true });
  } catch {
    return res.status(401).json({ error: 'UNAUTHORIZED' });
  }
});

authRouter.get('/me', async (req, res) => {
  const access = req.cookies?.[ACCESS_COOKIE];
  if (!access) return res.status(401).json({ error: 'UNAUTHORIZED' });
  try {
    const { sub } = verifyAccessToken(access);
    const user = await prisma.user.findUnique({ where: { id: sub }, select: { id: true, email: true, createdAt: true } });
    if (!user) return res.status(401).json({ error: 'UNAUTHORIZED' });
    return res.json({ user });
  } catch {
    return res.status(401).json({ error: 'UNAUTHORIZED' });
  }
});


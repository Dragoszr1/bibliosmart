import 'dotenv/config';
import express from 'express';
import cookieParser from 'cookie-parser';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';

import { env } from './utils/env.js';
import { authRouter } from './routes/auth.js';
import { userRouter } from './routes/user.js';

const app = express();

app.set('trust proxy', 1);

app.use(
  helmet({
    // The Vidking player is embedded on the frontend, not here.
    // Keep CSP conservative; configure the frontend separately.
    contentSecurityPolicy: false,
  }),
);

app.use(
  cors({
    origin: env.WEB_ORIGIN,
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
  }),
);

app.use(express.json({ limit: '256kb' }));
app.use(cookieParser());

app.use(
  rateLimit({
    windowMs: 60_000,
    limit: 120,
    standardHeaders: 'draft-7',
    legacyHeaders: false,
  }),
);

app.get('/api/health', (_req, res) => {
  res.json({ ok: true, name: 'animepulse-api', env: env.NODE_ENV });
});

app.use('/api/auth', authRouter);
app.use('/api/user', userRouter);

app.use((_req, res) => {
  res.status(404).json({ error: 'NOT_FOUND' });
});

// eslint-disable-next-line @typescript-eslint/no-unused-vars
app.use((err: unknown, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
  console.error(err);
  res.status(500).json({ error: 'INTERNAL_SERVER_ERROR' });
});

app.listen(env.PORT, () => {
  console.log(`AnimePulse API listening on http://localhost:${env.PORT}`);
});


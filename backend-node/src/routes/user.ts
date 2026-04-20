import { Router } from 'express';
import { z } from 'zod';
import { prisma } from '../utils/prisma.js';
import { requireAuth, type AuthedRequest } from '../middleware/requireAuth.js';

export const userRouter = Router();

userRouter.get('/profile', requireAuth, async (req, res) => {
  const { id } = (req as AuthedRequest).user;
  const user = await prisma.user.findUnique({ where: { id }, select: { id: true, email: true, createdAt: true } });
  res.json({ user });
});

userRouter.get('/history', requireAuth, async (req, res) => {
  const { id } = (req as AuthedRequest).user;
  const items = await prisma.watchProgress.findMany({
    where: { userId: id },
    orderBy: { updatedAt: 'desc' },
    take: 50,
  });
  res.json({ items });
});

const progressSchema = z.object({
  tmdbId: z.string().min(1),
  mediaType: z.enum(['movie', 'tv']),
  season: z.number().int().nonnegative().optional().nullable(),
  episode: z.number().int().nonnegative().optional().nullable(),
  timestamp: z.number().nonnegative().default(0),
  progress: z.number().min(0).max(100).default(0),
  duration: z.number().nonnegative().optional().nullable(),
});

userRouter.post('/progress', requireAuth, async (req, res) => {
  const parsed = progressSchema.safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ error: 'INVALID_INPUT', issues: parsed.error.issues });

  const { id: userId } = (req as AuthedRequest).user;
  const { tmdbId, mediaType, season, episode, timestamp, progress, duration } = parsed.data;

  const record = await prisma.watchProgress.upsert({
    where: {
      userId_tmdbId_mediaType_season_episode: {
        userId,
        tmdbId,
        mediaType,
        season: season ?? null,
        episode: episode ?? null,
      },
    },
    update: {
      timestamp,
      progress,
      duration: duration ?? undefined,
    },
    create: {
      userId,
      tmdbId,
      mediaType,
      season: season ?? null,
      episode: episode ?? null,
      timestamp,
      progress,
      duration: duration ?? undefined,
    },
  });

  res.json({ ok: true, record });
});

userRouter.get('/progress', requireAuth, async (req, res) => {
  const { id: userId } = (req as AuthedRequest).user;
  const querySchema = z.object({
    tmdbId: z.string().min(1),
    mediaType: z.enum(['movie', 'tv']),
    season: z.coerce.number().int().nonnegative().optional(),
    episode: z.coerce.number().int().nonnegative().optional(),
  });

  const parsed = querySchema.safeParse(req.query);
  if (!parsed.success) return res.status(400).json({ error: 'INVALID_INPUT', issues: parsed.error.issues });

  const { tmdbId, mediaType, season, episode } = parsed.data;
  const record = await prisma.watchProgress.findUnique({
    where: {
      userId_tmdbId_mediaType_season_episode: {
        userId,
        tmdbId,
        mediaType,
        season: mediaType === 'tv' ? (season ?? null) : null,
        episode: mediaType === 'tv' ? (episode ?? null) : null,
      },
    },
  });

  res.json({ record });
});

const favoriteSchema = z.object({
  tmdbId: z.string().min(1),
  mediaType: z.enum(['movie', 'tv']),
});

userRouter.post('/favorites', requireAuth, async (req, res) => {
  const parsed = favoriteSchema.safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ error: 'INVALID_INPUT', issues: parsed.error.issues });

  const { id: userId } = (req as AuthedRequest).user;
  const { tmdbId, mediaType } = parsed.data;

  const fav = await prisma.favorite.upsert({
    where: { userId_tmdbId_mediaType: { userId, tmdbId, mediaType } },
    update: {},
    create: { userId, tmdbId, mediaType },
  });
  res.json({ ok: true, favorite: fav });
});

userRouter.get('/favorites', requireAuth, async (req, res) => {
  const { id: userId } = (req as AuthedRequest).user;
  const favorites = await prisma.favorite.findMany({ where: { userId }, orderBy: { createdAt: 'desc' } });
  res.json({ favorites });
});


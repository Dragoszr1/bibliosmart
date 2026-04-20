import type { CookieOptions } from 'express';
import { env, isProd } from './env.js';

export const ACCESS_COOKIE = 'ap_access';
export const REFRESH_COOKIE = 'ap_refresh';

export function baseCookieOptions(): CookieOptions {
  return {
    httpOnly: true,
    secure: isProd,
    sameSite: isProd ? 'none' : 'lax',
    domain: env.COOKIE_DOMAIN || undefined,
    path: '/',
  };
}


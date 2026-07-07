import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import Profile from '../pages/Profile.vue'
import Login from '../pages/Login.vue'
import Signup from '../pages/Signup.vue'
import Books from '../pages/Books.vue'
import Club from '../pages/Club.vue'
import ClubJoin from '../pages/ClubJoin.vue'
import ClubAnterioare from '../pages/ClubAnterioare.vue'
import ClubThreads from '../pages/ClubThreads.vue'

import ForgotPassword from '../pages/ForgotPassword.vue'
import ResetPassword from '../pages/ResetPassword.vue'

const routes = [
  {
    path: '/',
    component: Home,
    name: 'Home'
  },
  {
    path: '/login',
    component: Login,
    name: 'Login'
  },
  {
    path: '/signup',
    component: Signup,
    name: 'Signup'
  },
  {
    path: '/forgot-password',
    component: ForgotPassword,
    name: 'ForgotPassword'
  },
  {
    path: '/reset-password/:token',
    component: ResetPassword,
    name: 'ResetPassword'
  },
  {
    path: '/profile',
    component: Profile,
    name: 'Profile',
    meta: { requiresAuth: true }
  },
  {
    path: '/books',
    component: Books,
    name: 'Books'
  },
  {
    path: '/club',
    component: Club,
    name: 'Club',
    meta: { requiresAuth: true, requiresClub: true }
  },
  {
    path: '/club/join/:token',
    component: ClubJoin,
    name: 'ClubJoin'
  },
  {
    path: '/club/threads',
    component: ClubThreads,
    name: 'ClubThreads',
    meta: { requiresAuth: true, requiresClub: true }
  },
  {
    path: '/club/anterioare',
    component: ClubAnterioare,
    name: 'ClubAnterioare',
    meta: { requiresAuth: true, requiresClub: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navigare — verifică sesiunea JWT pentru rutele protejate
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth || to.meta.requiresClub) {
    try {
      const res = await fetch('/api/auth/me', { credentials: 'include' })
      if (res.ok) {
        const data = await res.json()
        if (to.meta.requiresClub && !data.club) {
          next({ path: '/' }) // Redirect to home if not in the club
        } else {
          next()
        }
      } else {
        next({ path: '/login', query: { redirect: to.fullPath } })
      }
    } catch {
      next({ path: '/login', query: { redirect: to.fullPath } })
    }
  } else {
    next()
  }
})

export default router

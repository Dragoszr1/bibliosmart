import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import Profile from '../pages/Profile.vue'
import Login from '../pages/Login.vue'
import Signup from '../pages/Signup.vue'
import Books from '../pages/Books.vue'

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
    path: '/profile',
    component: Profile,
    name: 'Profile',
    meta: { requiresAuth: true }
  },
  {
    path: '/books',
    component: Books,
    name: 'Books'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navigare — verifică sesiunea JWT pentru rutele protejate
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    try {
      const res = await fetch('/api/auth/me', { credentials: 'include' })
      if (res.ok) {
        next()
      } else {
        next('/login')
      }
    } catch {
      next('/login')
    }
  } else {
    next()
  }
})

export default router

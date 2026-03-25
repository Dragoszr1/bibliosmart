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
    name: 'Profile'
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

export default router

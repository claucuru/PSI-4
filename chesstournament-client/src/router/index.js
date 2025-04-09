// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import HomeView from '../components/Home1.vue'
import LoginView from '../components/Login.vue'
import LogoutSuccessView from '../components/Logout.vue'
import { h } from 'vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/log-in',
      name: 'login',
      component: LoginView,
      meta: { requiresGuest: true }
    },
    {
      path: '/logout-success',
      name: 'logout-success',
      component: LogoutSuccessView
    }
    // Añade aquí más rutas según sea necesario
  ]
})

// Navegación guard para proteger rutas
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Si la ruta requiere autenticación y el usuario no está autenticado
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
  } 
  // Si la ruta es solo para invitados y el usuario está autenticado
  else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: 'home' })
  } 
  else {
    next()
  }
})

export default router
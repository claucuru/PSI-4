
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import CreateTournamentView from '../components/CreateTournament.vue'
import HomeView from '../components/Home1.vue'
import HomeView2 from '../components/Home2.vue'
import LoginView from '../components/Login.vue'
import LogoutSuccessView from '../components/Logout.vue'
import TournamentConfirmation from '../components/TournamentConfirmation.vue'
import TournamentDetails from '../components/TournamentDetails.vue'
import Faq from '../components/Faq.vue'
import Perfil from '../components/Perfil.vue'
import { useAuthStore } from '../stores/auth'

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
      path: '/adminhome',
      name: 'home2',
      component: HomeView2,
      meta: { requiresAuth: true}
    },
    {
      path: '/logout-success',
      name: 'logout-success',
      component: LogoutSuccessView
    },
    {
      path:'/createtournament',
      name:'createtournament',
      component: CreateTournamentView
    },
    {
      path: '/torneos/:id/confirmacion',
      name: 'tournament-confirmation',
      component: TournamentConfirmation,
      props: true
    },
    {
      path: '/faq',
      name: 'faq',
      component: Faq
    },
    {
      path: '/torneos/:id',
      name: 'tournament-details',
      component: TournamentDetails,
    },
    {
      path: '/perfil',
      name: 'perfil',
      component: Perfil,
      meta: { requiresAuth: true }
    },
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
  else if (to.meta.requiresGuest && authStore.isAuthenticated){
    next({ name: 'home2' })
  }
  else {
    next()
  }
})

export default router

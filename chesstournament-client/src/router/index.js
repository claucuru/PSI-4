// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import CreateTournamentView from "../components/CreateTournament.vue";
import Faq from "../components/Faq.vue";
import HomeView from "../components/Home.vue";
import LoginView from "../components/Login.vue";
import LogoutSuccessView from "../components/Logout.vue";
import Perfil from "../components/Perfil.vue";
import TournamentConfirmation from "../components/TournamentConfirmation.vue";
import TournamentDetails from "../components/TournamentDetails.vue";
import { useAuthStore } from "../stores/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
      meta: { requiresGuest: true },
    },

    {
      path: "/logout",
      name: "logout-success",
      component: LogoutSuccessView,
    },
    {
      path: "/createtournament",
      name: "createtournament",
      component: CreateTournamentView,
    },
    {
      path: "/tournament/:id/confirmation",
      name: "tournament-confirmation",
      component: TournamentConfirmation,
      props: true,
    },
    {
      path: "/faq",
      name: "faq",
      component: Faq,
    },
    {
      path: "/tournamentdetail/:id",
      name: "tournament-details",
      component: TournamentDetails,
    },
    {
      path: "/profile",
      name: "perfil",
      component: Perfil,
      meta: { requiresAuth: true },
    },
  ],
});

// Navegación guard para proteger rutas
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  // Si la ruta requiere autenticación y el usuario no está autenticado
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: "login" });
  }
  // Si la ruta es solo para invitados y el usuario está autenticado
  // MODIFICADO: Solo redirigir si está intentando acceder a login Y está autenticado Y viene de una ruta logout
  else if (
    to.name === "login" &&
    authStore.isAuthenticated &&
    from.name == "logout-success"
  ) {
    // Verificar que el token sea válido antes de redirigir
    try {
      // Opcional: Verificar token con el servidor
      // await authStore.verifyToken()
      next({ name: "home" });
    } catch (error) {
      // Si el token no es válido, limpiar auth y permitir acceso a login
      authStore.clearAuth();
      next();
    }
  } else {
    next();
  }
});

export default router;

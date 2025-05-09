<template>
  <header class="main-header">
    <div class="header-container">
      <div class="header-left">
        <router-link to="/" class="logo">
          <span class="logo-text">TournamentMaster</span>
        </router-link>
      </div>

      <nav class="main-nav">
        <router-link to="/" class="nav-link" exact-active-class="active"
          >Inicio</router-link
        >
        <router-link to="/faq" class="nav-link" active-class="active"
          >FAQ</router-link
        >
      </nav>

      <div class="header-right">
        <!-- Usuario autenticado -->
        <template v-if="isAuthenticated">
          <!-- Mostrar cerrar sesión -->
          <template v-if="!isInHomePage && isAuthenticated">
            <a
              href="#"
              class="logout-btn"
              @click.prevent="handleLogout"
              data-cy="logout-cypress-test"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
              Cerrar sesión
            </a>
          </template>

          <!-- Menú de usuario -->
          <div class="user-menu" @click="toggleUserMenu" ref="userMenuTrigger">
            <div class="user-avatar">
              <!-- Mostrar imagen de perfil si existe, si no mostrar inicial -->
              <img
                v-if="userPhotoUrl"
                :src="userPhotoUrl"
                alt="Foto de perfil"
                class="user-photo"
              />
              <span v-else class="user-initial">{{ userInitial }}</span>
              <!-- Insignia de administrador -->
              <span v-if="isAdmin" class="admin-badge" data-cy="admin-log"
                >Estás autenticado como administrador</span
              >
            </div>
            <span class="user-name">{{ username }}</span>
            <span class="dropdown-icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </span>

            <!-- Menú desplegable del usuario -->
            <div class="user-dropdown" v-if="showUserMenu" ref="userMenu">
              <router-link to="/profile" class="dropdown-item">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                Mi perfil
              </router-link>
              <router-link to="/admin" class="dropdown-item" v-if="isAdmin">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M12 20h9"></path>
                  <path
                    d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"
                  ></path>
                </svg>
                Administración
              </router-link>
              <div class="dropdown-divider"></div>
              <a
                href="#"
                class="dropdown-item logout"
                @click.prevent="handleLogout"
                data-cy="logout-cypress-test"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16 17 21 12 16 7"></polyline>
                  <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
                Cerrar sesión
              </a>
            </div>
          </div>
        </template>

        <!-- Usuario no autenticado -->
        <template v-else>
          <router-link
            to="/login"
            class="login-btn"
            v-if="$route.name !== 'login'"
            data-cy="login-cypress-test"
          >
            <span class="login-icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
                <polyline points="10 17 15 12 10 7"></polyline>
                <line x1="15" y1="12" x2="3" y2="12"></line>
              </svg>
            </span>
            Iniciar sesión
          </router-link>
        </template>
      </div>

      <!-- Botón de menú móvil -->
      <button class="mobile-menu-toggle" @click="toggleMobileMenu">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>
    </div>

    <!-- Menú móvil -->
    <div class="mobile-menu" :class="{ active: showMobileMenu }">
      <nav class="mobile-nav">
        <router-link
          to="/"
          class="mobile-nav-link"
          exact-active-class="active"
          @click="closeMobileMenu"
          >Inicio</router-link
        >
        <router-link
          to="/faq"
          class="mobile-nav-link"
          active-class="active"
          @click="closeMobileMenu"
          >FAQ</router-link
        >

        <!-- Opciones de usuario autenticado para móvil -->
        <template v-if="isAuthenticated">
          <div class="mobile-divider"></div>
          <router-link
            to="/profile"
            class="mobile-nav-link"
            @click="closeMobileMenu"
            >Mi perfil</router-link
          >
          <router-link
            v-if="isAdmin"
            to="/createtournament"
            class="mobile-nav-link"
            @click="closeMobileMenu"
          >
            Crear Torneo
          </router-link>
          <a
            href="#"
            class="mobile-nav-link logout"
            @click.prevent="handleLogout"
            >Cerrar sesión</a
          >
        </template>
        <!-- Opciones de usuario no autenticado para móvil -->
        <template v-else>
          <div class="mobile-divider"></div>
          <router-link
            to="/login"
            class="mobile-nav-link"
            @click="closeMobileMenu"
          >
            Iniciar sesión
          </router-link>
        </template>
      </nav>
    </div>
  </header>
</template>

<script>
import { useAuthStore } from "@/stores/auth";
import { computed, onMounted, onUnmounted, ref } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "HeaderComponent",
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    const showUserMenu = ref(false);
    const showMobileMenu = ref(false);
    const userMenuTrigger = ref(null);
    const userMenu = ref(null);

    // Estado de autenticación
    const isAuthenticated = computed(() => authStore.isAuthenticated);
    const username = computed(() => authStore.user?.username || "Usuario");
    const isAdmin = computed(() => authStore.user?.is_staff || false);

    // URL de la foto de perfil
    const userPhotoUrl = computed(() => authStore.user?.photoUrl || null);

    // Inicial del usuario para avatar
    const userInitial = computed(() => {
      if (!username.value) return "U";
      return username.value.charAt(0).toUpperCase();
    });

    // Verificar si el usuario está autenticado al montar el componente
    onMounted(async () => {
      // Si hay un token almacenado pero no hay información de usuario, intentar recuperarla
      if (authStore.token && !authStore.user) {
        await authStore.fetchUserProfile();
      }
    });

    // Funciones para manejar los menús
    const toggleUserMenu = () => {
      showUserMenu.value = !showUserMenu.value;
    };

    const toggleMobileMenu = () => {
      showMobileMenu.value = !showMobileMenu.value;
    };

    const closeMobileMenu = () => {
      showMobileMenu.value = false;
    };

    const handleLogout = async () => {
      await authStore.logout();
      router.push("/logout");
    };

    // Cerrar menú de usuario al hacer clic fuera
    const closeMenuOnOutsideClick = (event) => {
      if (
        showUserMenu.value &&
        userMenuTrigger.value &&
        userMenu.value &&
        !userMenuTrigger.value.contains(event.target) &&
        !userMenu.value.contains(event.target)
      ) {
        showUserMenu.value = false;
      }
    };

    onMounted(() => {
      document.addEventListener("click", closeMenuOnOutsideClick);
    });

    onUnmounted(() => {
      document.removeEventListener("click", closeMenuOnOutsideClick);
    });

    return {
      isAuthenticated,
      username,
      isAdmin,
      userInitial,
      userPhotoUrl,
      showUserMenu,
      showMobileMenu,
      userMenuTrigger,
      userMenu,
      toggleUserMenu,
      toggleMobileMenu,
      closeMobileMenu,
      handleLogout,
    };
  },
};
</script>

<style scoped>
@import '@/assets/style_header.css';
</style>

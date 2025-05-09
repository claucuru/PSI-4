<template>
  <div class="login-container">
    <div class="login-background">
      <div class="login-left">
        <div class="chess-pattern"></div>
        <div class="login-content">
          <img
            src="../components/icons/icono.png"
            class="chess-piece-icon"
            alt="Chess Piece"
            data-cy="login-chess-icon"
          />
          <h1 class="login-brand">TournamentMaster</h1>
          <p class="login-tagline">
            La plataforma líder para gestión de torneos de ajedrez.
          </p>
        </div>
      </div>
      <div class="login-right">
        <div class="login-card">
          <h1 class="login-title">Iniciar sesión</h1>
          <p class="login-subtitle">Acceso a administración de torneos</p>

          <div v-if="error" class="error-message" data-cy="error-message">
            {{ error }}
          </div>

          <form @submit.prevent="handleLogin" class="login-form">
            <div class="form-group">
              <label for="username">Nombre de usuario</label>
              <div class="input-container">
                <span class="input-icon">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
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
                </span>
                <input
                  type="text"
                  id="username"
                  v-model="username"
                  placeholder="Introduce tu nombre de usuario"
                  data-cy="username"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="password">Contraseña</label>
              <div class="input-container">
                <span class="input-icon">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <rect
                      x="3"
                      y="11"
                      width="18"
                      height="11"
                      rx="2"
                      ry="2"
                    ></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                  </svg>
                </span>
                <input
                  type="password"
                  id="password"
                  v-model="password"
                  placeholder="Introduce tu contraseña"
                  data-cy="password"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              class="login-button"
              data-cy="login-button"
              :disabled="isLoading"
            >
              <span v-if="isLoading" class="loading-spinner"></span>
              {{ isLoading ? "Iniciando sesión..." : "Iniciar sesión" }}
            </button>
          </form>

          <div class="login-footer">
            <router-link to="/" class="back-link">
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
                <line x1="19" y1="12" x2="5" y2="12"></line>
                <polyline points="12 19 5 12 12 5"></polyline>
              </svg>
              Volver a la página principal
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/auth";
import { ref } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "LoginView",
  setup() {
    const username = ref("");
    const password = ref("");
    const error = ref("");
    const isLoading = ref(false);
    const router = useRouter();
    const authStore = useAuthStore();

    const handleLogin = async () => {
      try {
        error.value = "";
        isLoading.value = true;

        const loginSuccess = await authStore.login(username.value, password.value);
        
        // Solo redirigir si el login fue exitoso
        if (loginSuccess) {
          router.push({ name: "home" });
        } else {
          // Si login devuelve false, establecer el mensaje de error
          error.value = "Error: Invalid username or password";
        }
      } catch (err) {
        error.value =
          "Error: Invalid username or password";
        console.error("Error de inicio de sesión:", err);
      } finally {
        isLoading.value = false;
      }
    };

    return {
      username,
      password,
      error,
      isLoading,
      handleLogin,
    };
  },
};
</script>
<style scoped>
@import '@/assets/style_login.css';
</style>

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

        await authStore.login(username.value, password.value);

        // Redirigir al usuario a la página principal después del inicio de sesión exitoso
        router.push({ name: "home" });
      } catch (err) {
        error.value =
          err.response?.data?.non_field_errors?.[0] ||
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
html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.login-container {
  width: 100vw;
  height: 100vh;
  min-height: 100%;
  overflow: hidden;
}

.login-background {
  display: flex;
  width: 100%;
  height: 100%;
  min-height: 100vh;
  background-color: #f8f0fd;
}

.login-left {
  flex: 1;
  background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: white;
  position: relative;
  overflow: hidden;
}

.chess-pattern {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: linear-gradient(
      45deg,
      rgba(255, 255, 255, 0.05) 25%,
      transparent 25%
    ),
    linear-gradient(-45deg, rgba(255, 255, 255, 0.05) 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, rgba(255, 255, 255, 0.05) 75%),
    linear-gradient(-45deg, transparent 75%, rgba(255, 255, 255, 0.05) 75%);
  background-size: 60px 60px;
  background-position: 0 0, 0 30px, 30px -30px, -30px 0px;
  opacity: 0.4;
}

.chess-piece-icon {
  width: 120px;
  height: 120px;
  margin: 0 auto 30px;
  opacity: 0.9;
}

.login-content {
  position: relative;
  z-index: 2;
  text-align: center;
  width: 80%;
}

.login-brand {
  font-size: 52px;
  font-weight: 800;
  margin-bottom: 20px;
  letter-spacing: -1px;
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.login-tagline {
  font-size: 22px;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.5;
}

.login-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.login-card {
  background-color: white;
  border-radius: 24px;
  box-shadow: 0 15px 40px rgba(138, 75, 175, 0.15);
  width: 100%;
  max-width: 480px;
  padding: 50px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 50px rgba(138, 75, 175, 0.2);
}

.login-title {
  color: #8e44ad;
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 10px;
}

.login-subtitle {
  color: #9f7ead;
  font-size: 18px;
  margin-bottom: 40px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-group label {
  color: #6b5876;
  font-size: 15px;
  font-weight: 600;
  margin-left: 4px;
}

.input-container {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  color: #9f7ead;
}

.form-group input {
  border: 2px solid #e6d5f2;
  border-radius: 14px;
  color: #333;
  font-size: 16px;
  padding: 16px 20px 16px 50px;
  transition: all 0.3s;
  width: 100%;
  background-color: #faf6fd;
}

.form-group input:focus {
  border-color: #bb8fce;
  outline: none;
  box-shadow: 0 0 0 4px rgba(187, 143, 206, 0.15);
  background-color: #fff;
}

.login-button {
  background: linear-gradient(to right, #9b59b6, #8e44ad);
  border: none;
  border-radius: 14px;
  color: white;
  cursor: pointer;
  font-size: 17px;
  font-weight: 600;
  margin-top: 20px;
  padding: 18px;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.login-button::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: 0.5s;
}

.login-button:hover::before {
  left: 100%;
}

.login-button:hover {
  background: linear-gradient(to right, #8e44ad, #7d3c98);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(155, 89, 182, 0.3);
}

.login-button:active {
  transform: translateY(0);
}

.login-button:disabled {
  background: linear-gradient(to right, #cda8da, #c39bd3);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  margin-right: 10px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
  vertical-align: middle;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-message {
  background-color: #fdecef;
  border-left: 4px solid #e74c3c;
  border-radius: 12px;
  color: #c0392b;
  margin-bottom: 30px;
  padding: 16px;
  font-size: 15px;
  display: flex;
  align-items: center;
}

.error-message::before {
  content: "!";
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background-color: #e74c3c;
  color: white;
  border-radius: 50%;
  margin-right: 10px;
  font-weight: bold;
}

.login-footer {
  margin-top: 36px;
  text-align: center;
}

.back-link {
  color: #9b59b6;
  font-size: 16px;
  font-weight: 500;
  text-decoration: none;
  transition: color 0.3s;
  display: inline-flex;
  align-items: center;
}

.back-link:hover {
  color: #8e44ad;
  text-decoration: underline;
}

.back-link svg {
  margin-right: 6px;
}

.chess-piece-icon {
  width: 240px;
  height: 350px;
}

/* Media Queries mejoradas para responsive */
@media (max-width: 1200px) {
  .login-brand {
    font-size: 42px;
  }

  .login-tagline {
    font-size: 18px;
  }

  .login-card {
    padding: 40px;
  }
}

@media (max-width: 992px) {
  .login-background {
    flex-direction: column;
    min-height: auto;
  }

  .login-left {
    padding: 30px 20px;
    height: auto;
    min-height: 200px;
  }

  .login-right {
    padding: 40px 20px;
    align-items: flex-start;
  }

  .login-brand {
    font-size: 32px;
    margin-bottom: 10px;
  }

  .login-tagline {
    font-size: 16px;
    max-width: 100%;
  }

  .chess-piece-icon {
    width: 80px;
    height: 80px;
    margin-bottom: 15px;
  }

  .login-card {
    max-width: 100%;
    margin-top: -50px;
    padding: 30px;
  }

  .login-title {
    font-size: 28px;
  }

  .login-subtitle {
    font-size: 16px;
    margin-bottom: 25px;
  }
}

@media (max-width: 768px) {
  .login-left {
    min-height: 180px;
  }

  .login-brand {
    font-size: 28px;
  }

  .login-tagline {
    font-size: 15px;
  }

  .login-card {
    padding: 25px;
    margin-top: -30px;
  }

  .login-form {
    gap: 20px;
  }

  .form-group input {
    padding: 14px 20px 14px 50px;
    font-size: 15px;
  }

  .login-button {
    padding: 16px;
    font-size: 16px;
  }
}

@media (max-width: 576px) {
  .login-left {
    padding: 20px 15px;
    min-height: 150px;
  }

  .login-brand {
    font-size: 24px;
  }

  .login-tagline {
    font-size: 14px;
  }

  .login-right {
    padding: 30px 15px;
  }

  .login-card {
    padding: 20px 15px;
    border-radius: 16px;
    margin-top: -20px;
  }

  .login-title {
    font-size: 24px;
  }

  .login-subtitle {
    font-size: 15px;
    margin-bottom: 20px;
  }

  .form-group label {
    font-size: 14px;
  }

  .input-icon {
    left: 15px;
  }

  .form-group input {
    padding: 12px 15px 12px 45px;
    font-size: 14px;
    border-radius: 12px;
  }

  .login-button {
    padding: 14px;
    font-size: 15px;
    margin-top: 15px;
  }

  .error-message {
    font-size: 14px;
    padding: 12px;
    margin-bottom: 20px;
  }

  .back-link {
    font-size: 14px;
  }
}

@media (max-width: 400px) {
  .login-left {
    min-height: 120px;
  }

  .login-brand {
    font-size: 20px;
  }

  .chess-piece-icon {
    width: 60px;
    height: 60px;
    margin-bottom: 10px;
  }

  .login-title {
    font-size: 22px;
  }

  .login-subtitle {
    font-size: 14px;
  }

  .form-group input {
    padding: 10px 12px 10px 40px;
  }

  .input-icon {
    width: 16px;
    height: 16px;
  }
}
</style>

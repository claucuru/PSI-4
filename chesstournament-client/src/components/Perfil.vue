<template>
  <div class="profile-container">
    <div class="profile-background">
      <div class="profile-header">
        <div class="chess-pattern"></div>
        <div class="profile-header-content">
          <img
            src="../components/icons/icono.png"
            class="chess-piece-icon"
            alt="Chess Piece"
            data-cy="profile-chess-icon"
          />
          <h1 class="profile-brand">TournamentMaster</h1>
        </div>
      </div>
      <div class="profile-content">
        <div class="profile-card">
          <h1 class="profile-title">Mi Perfil</h1>
          <p class="profile-subtitle">Información personal y administración</p>

          <div v-if="error" class="error-message" data-cy="profile-error">
            {{ error }}
          </div>

          <div
            v-if="successMessage"
            class="success-message"
            data-cy="profile-success"
          >
            {{ successMessage }}
          </div>

          <div class="profile-avatar-section">
            <div class="profile-avatar">
              <span v-if="!user.photoUrl" class="avatar-placeholder">
                {{ getUserInitials() }}
              </span>
              <img v-else :src="user.photoUrl" alt="Foto de perfil" />
            </div>
            <button class="change-photo-button" @click="triggerFileInput">
              Cambiar foto
            </button>
            <input
              type="file"
              ref="fileInput"
              style="display: none"
              accept="image/*"
              @change="handleFileChange"
            />
          </div>

          <form @submit.prevent="saveProfile" class="profile-form">
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
                  v-model="user.username"
                  placeholder="Nombre de usuario"
                  data-cy="username"
                  disabled
                />
              </div>
            </div>

            <div class="form-group">
              <label for="role">Rol de usuario</label>
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
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                  </svg>
                </span>
                <input
                  type="text"
                  id="role"
                  v-model="user.role"
                  placeholder="Rol de usuario"
                  data-cy="role-input"
                  disabled
                />
              </div>
            </div>

            <h2 class="section-title">Acciones administrativas</h2>

            <div class="admin-actions">
              <div class="admin-action-card">
                <div class="admin-action-icon">
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
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                  </svg>
                </div>
                <div class="admin-action-title">Gestionar Usuarios</div>
              </div>

              <div class="admin-action-card">
                <div class="admin-action-icon">
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
                    <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path>
                    <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path>
                    <path d="M4 22h16"></path>
                    <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"></path>
                  </svg>
                </div>
                <div class="admin-action-title">Gestionar Torneos</div>
              </div>

              <div class="admin-action-card">
                <div class="admin-action-icon">
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
                    <circle cx="12" cy="12" r="3"></circle>
                    <path
                      d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"
                    ></path>
                  </svg>
                </div>
                <div class="admin-action-title">Configuración del Sistema</div>
              </div>
            </div>

            <div class="form-actions">
              <button
                type="submit"
                class="save-button"
                data-cy="save-button"
                :disabled="isLoading"
              >
                <span v-if="isLoading" class="loading-spinner"></span>
                {{ isLoading ? "Guardando..." : "Guardar cambios" }}
              </button>

              <button type="button" class="cancel-button">Cancelar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/auth";
import { onMounted, ref } from "vue";

export default {
  name: "PerfilAdminView",
  setup() {
    const user = ref({
      username: "",
      role: "",
      photoUrl: null,
    });

    const error = ref("");
    const successMessage = ref("");
    const isLoading = ref(false);
    const fileInput = ref(null);
    const authStore = useAuthStore();

    onMounted(async () => {
      try {
        isLoading.value = true;
        // Obtener datos del usuario desde el store de autenticación
        user.value = {
          username: authStore.user?.username || "",
          role: authStore.user?.role || "Administrador",
          photoUrl: authStore.user?.photoUrl || null,
        };
      } catch (err) {
        error.value = "No se pudo cargar la información del perfil.";
        console.error("Error al cargar perfil:", err);
      } finally {
        isLoading.value = false;
      }
    });

    const getUserInitials = () => {
      if (!user.value.username) return "?";
      return user.value.username
        .split(" ")[0] // Tomar solo la primera palabra del nombre de usuario
        .charAt(0) // Tomar la primera letra
        .toUpperCase(); // Convertirla a mayúscula
    };

    const triggerFileInput = () => {
      fileInput.value.click();
    };

    const handleFileChange = (event) => {
      const file = event.target.files[0];
      if (!file) return;

      // Convertir la imagen a base64 para almacenarla
      const reader = new FileReader();
      reader.onload = (e) => {
        user.value.photoUrl = e.target.result;
        // Preferiblemente, aquí subirías la imagen al servidor
        // y obtendrías la URL para almacenarla en el store
      };
      reader.readAsDataURL(file);
    };

    const saveProfile = async () => {
      try {
        error.value = "";
        successMessage.value = "";
        isLoading.value = true;

        // Actualizar la foto en el store de autenticación
        // para que se refleje en toda la aplicación
        if (user.value.photoUrl) {
          await authStore.updateUserPhoto(user.value.photoUrl);
        }

        // Simular espera para la operación
        await new Promise((resolve) => setTimeout(resolve, 1000));

        // Mostrar mensaje de éxito
        successMessage.value = "Perfil actualizado correctamente.";
      } catch (err) {
        error.value =
          err.response?.data?.message ||
          "Error al actualizar el perfil. Por favor, inténtalo de nuevo.";
        console.error("Error al guardar perfil:", err);
      } finally {
        isLoading.value = false;
      }
    };

    return {
      user,
      error,
      successMessage,
      isLoading,
      fileInput,
      getUserInitials,
      triggerFileInput,
      handleFileChange,
      saveProfile,
    };
  },
};
</script>

<style scoped>
.profile-container {
  width: 100vw;
  min-height: 100vh;
  background-color: #f8f0fd;
}

.profile-background {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: 100vh;
}

.profile-header {
  background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%);
  color: white;
  padding: 20px 40px;
  position: relative;
  overflow: hidden;
  height: 200px;
  display: flex;
  align-items: center;
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

.profile-header-content {
  display: flex;
  align-items: center;
  position: relative;
  z-index: 2;
}

.chess-piece-icon {
  width: 80px;
  height: 80px;
  margin-right: 20px;
}

.profile-brand {
  font-size: 36px;
  font-weight: 800;
  letter-spacing: -1px;
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.profile-content {
  flex: 1;
  display: flex;
  justify-content: center;
  padding: 40px;
  margin-top: -60px;
}

.profile-card {
  background-color: white;
  border-radius: 24px;
  box-shadow: 0 15px 40px rgba(138, 75, 175, 0.15);
  width: 100%;
  max-width: 800px;
  padding: 50px;
  transition: transform 0.3s, box-shadow 0.3s;
  z-index: 10;
}

.profile-title {
  color: #8e44ad;
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 10px;
}

.profile-subtitle {
  color: #9f7ead;
  font-size: 18px;
  margin-bottom: 40px;
}

.section-title {
  color: #8e44ad;
  font-size: 24px;
  font-weight: 600;
  margin: 40px 0 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f0e6f6;
}

.profile-avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 40px;
}

.profile-avatar {
  width: 120px;
  height: 120px;
  border-radius: 60px;
  overflow: hidden;
  background-color: #e6d5f2;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
  box-shadow: 0 8px 16px rgba(138, 75, 175, 0.15);
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  font-size: 48px;
  font-weight: 600;
  color: #8e44ad;
}

.change-photo-button {
  background-color: transparent;
  border: 2px solid #9b59b6;
  border-radius: 20px;
  color: #9b59b6;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  padding: 8px 16px;
  transition: all 0.3s;
}

.change-photo-button:hover {
  background-color: #f8f0fd;
  transform: translateY(-2px);
}

.profile-form {
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

.form-group input:disabled {
  background-color: #f0e6f6;
  cursor: not-allowed;
  opacity: 0.7;
}

/* Estilos para acciones administrativas */
.admin-actions {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.admin-action-card {
  background: linear-gradient(135deg, #f9f4fc 0%, #f2eaf8 100%);
  border-radius: 16px;
  padding: 25px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.3s;
  border: 2px solid #f0e6f6;
  cursor: pointer;
}

.admin-action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(155, 89, 182, 0.1);
  border-color: #e1c7f4;
}

.admin-action-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  background: linear-gradient(135deg, #bb8fce 0%, #9b59b6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
  color: white;
}

.admin-action-title {
  font-size: 16px;
  font-weight: 600;
  color: #6b5876;
  text-align: center;
}

.form-actions {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.save-button {
  flex: 1;
  background: linear-gradient(to right, #9b59b6, #8e44ad);
  border: none;
  border-radius: 14px;
  color: white;
  cursor: pointer;
  font-size: 17px;
  font-weight: 600;
  padding: 18px;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.save-button::before {
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

.save-button:hover::before {
  left: 100%;
}

.save-button:hover {
  background: linear-gradient(to right, #8e44ad, #7d3c98);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(155, 89, 182, 0.3);
}

.save-button:active {
  transform: translateY(0);
}

.save-button:disabled {
  background: linear-gradient(to right, #cda8da, #c39bd3);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.cancel-button {
  flex: 1;
  background: transparent;
  border: 2px solid #9b59b6;
  border-radius: 14px;
  color: #9b59b6;
  cursor: pointer;
  font-size: 17px;
  font-weight: 600;
  padding: 18px;
  text-align: center;
  text-decoration: none;
  transition: all 0.3s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cancel-button:hover {
  background-color: #f8f0fd;
  transform: translateY(-2px);
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

.success-message {
  background-color: #eafaf1;
  border-left: 4px solid #2ecc71;
  border-radius: 12px;
  color: #27ae60;
  margin-bottom: 30px;
  padding: 16px;
  font-size: 15px;
  display: flex;
  align-items: center;
}

.success-message::before {
  content: "✓";
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background-color: #2ecc71;
  color: white;
  border-radius: 50%;
  margin-right: 10px;
  font-weight: bold;
}

/* Responsive */
@media (max-width: 992px) {
  .profile-content {
    padding: 20px;
  }

  .profile-card {
    padding: 40px 30px;
  }

  .profile-header {
    height: 160px;
  }

  .chess-piece-icon {
    width: 60px;
    height: 60px;
  }

  .profile-brand {
    font-size: 32px;
  }
}

@media (max-width: 576px) {
  .profile-header {
    height: 120px;
    padding: 15px;
  }

  .profile-content {
    padding: 15px;
    margin-top: -40px;
  }

  .profile-card {
    padding: 30px 20px;
  }

  .profile-title {
    font-size: 28px;
  }

  .profile-subtitle {
    font-size: 16px;
    margin-bottom: 30px;
  }

  .form-actions {
    flex-direction: column;
  }

  .chess-piece-icon {
    width: 50px;
    height: 50px;
  }

  .profile-brand {
    font-size: 24px;
  }
}
</style>

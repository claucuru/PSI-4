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
@import '@/assets/perfil.css';
</style>

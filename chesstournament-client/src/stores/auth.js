// src/stores/auth.js
import axios from "axios";
import { defineStore } from "pinia";
import router from "../router";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: null,
    user: null,
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    getToken: (state) => state.token,
    getUser: (state) => state.user,
  },

  actions: {
    async login(username, password) {
      this.loading = true;
      this.error = null;

      try {
        // Usando la API de Django con djoser para autenticación
        const response = await axios.post("/token/login/", {
          username,
          password,
        });

        // Guardar el token en el estado y localStorage
        this.token = response.data.auth_token;

        // Obtener información del usuario
        await this.fetchUserProfile();

        // Redireccionar a la página inicial
        router.push("/");
        return true;
      } catch (err) {
        this.error =
          err.response?.data?.non_field_errors?.[0] || "Error de autenticación";
        return false;
      } finally {
        this.loading = false;
      }
    },

    async fetchUserProfile() {
      try {
        const response = await axios.get("/users/me/", {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });

        // Recuperar la foto del usuario desde localStorage
        const savedPhotoUrl = localStorage.getItem(
          `userPhoto_${response.data.username}`
        );

        // Asegúrate de que photoUrl esté disponible en el usuario
        this.user = {
          ...response.data,
          photoUrl: response.data.photoUrl || savedPhotoUrl || null,
        };

        return this.user;
      } catch (err) {
        console.error("Error al obtener perfil de usuario:", err);
        return null;
      }
    },

    async logout() {
      this.loading = true;

      try {
        // Envía la solicitud de logout al servidor
        await axios.post(
          "/token/logout/",
          {},
          {
            headers: {
              Authorization: `Token ${this.token}`,
              "Content-Type": "application/json",
            },
          }
        );
      } catch (err) {
        console.error("Error al hacer logout:", err);
      } finally {
        // Independientemente de la respuesta del servidor, limpiamos localmente
        this.clearAuth();
        this.loading = false;

        // Redireccionar a la página de logout
        router.push("/logout");
      }
    },

    clearAuth() {
      // Limpiar el estado
      // Nota: NO eliminamos las fotos de perfil guardadas para conservarlas entre sesiones
      this.token = null;
      this.user = null;

      // Limpiar solo el token y el usuario actual del localStorage
      localStorage.removeItem("token");
      localStorage.removeItem("user");
    },

    // Método para actualizar la foto de perfil
    async updateUserPhoto(photoUrl) {
      try {
        if (this.user) {
          // Actualizar el objeto de usuario en el store
          this.user = {
            ...this.user,
            photoUrl,
          };

          // Guardar la foto asociada al nombre de usuario
          if (this.user.username) {
            localStorage.setItem(`userPhoto_${this.user.username}`, photoUrl);
          }

          return true;
        }
        return false;
      } catch (err) {
        console.error("Error al actualizar la foto de perfil:", err);
        return false;
      }
    },
  },
});

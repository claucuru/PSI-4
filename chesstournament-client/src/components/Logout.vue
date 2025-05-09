<template>
  <div class="logout-container">
    <div class="logout-card">
      <div class="logout-icon">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="64"
          height="64"
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
      </div>
      <h1 class="logout-page" data-cy="logoutPage">Log Out</h1>
      <p class="logout-message">
        Has cerrado sesión correctamente. Serás redirigido a la página de inicio
        en <span class="countdown">{{ countdown }}</span> segundos.
      </p>
      <div class="logout-progress">
        <div class="progress-bar" :style="{ width: progressWidth + '%' }"></div>
      </div>
      <div class="logout-actions">
        <router-link to="/" class="home-link" data-cy="return-home">
          Volver a la página principal
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/auth";
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "LogoutView",
  setup() {
    const countdown = ref(5);
    const router = useRouter();
    const authStore = useAuthStore();

    const progressWidth = computed(() => (5 - countdown.value) * 20);

    onMounted(async () => {
      // Ejecutar el logout
      await authStore.logout();

      // Redirigir automáticamente después de 5 segundos
      const timer = setInterval(() => {
        countdown.value -= 1;
        if (countdown.value <= 0) {
          clearInterval(timer);
          router.push("/");
        }
      }, 1000);
    });

    return {
      countdown,
      progressWidth,
    };
  },
};
</script>

<style scoped>
@import '@/assets/log_out.css';
</style>

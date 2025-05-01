<template>
    <div class="logout-container">
      <div class="logout-card">
        <div class="logout-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
        </div>
        <h1 class="logout-page" data-cy="logoutPage">Log Out</h1>
        <p class="logout-message">
          Has cerrado sesión correctamente. Serás redirigido a la página de inicio en <span class="countdown">{{ countdown }}</span> segundos.
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
  import { useAuthStore } from '@/stores/auth'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
  
  export default {
    name: 'LogoutView',
    setup() {
      const countdown = ref(5)
      const router = useRouter()
      const authStore = useAuthStore()
      
      const progressWidth = computed(() => (5 - countdown.value) * 20)
      
      onMounted(async () => {
        // Ejecutar el logout
        await authStore.logout()
        
        // Redirigir automáticamente después de 5 segundos
        const timer = setInterval(() => {
          countdown.value -= 1
          if (countdown.value <= 0) {
            clearInterval(timer)
            router.push('/')
          }
        }, 1000)
      })
      
      return {
        countdown,
        progressWidth
      }
    }
  }
  </script>
  
  <style scoped>
  html, body {
    margin: 0;
    padding: 0;

  }
  .logout-container {
    min-width: 100vw;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f8f0fd;
    padding: 20px;
  }
  
  .logout-card {
    background-color: white;
    border-radius: 16px;
    box-shadow: 0 8px 20px rgba(186, 150, 211, 0.15);
    width: 100%;
    max-width: 420px;
    padding: 32px;
    text-align: center;
  }
  
  .logout-icon {
    color: #9b59b6;
    margin-bottom: 20px;
  }
  
  .logout-page {
    color: #8e44ad;
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 16px;
  }
  
  .logout-message {
    color: #6b5876;
    font-size: 16px;
    margin-bottom: 24px;
    line-height: 1.5;
  }
  
  .countdown {
    color: #9b59b6;
    font-weight: 700;
  }
  
  .logout-progress {
    background-color: #e6d5f2;
    border-radius: 4px;
    height: 8px;
    margin-bottom: 24px;
    overflow: hidden;
    width: 100%;
  }
  
  .progress-bar {
    background-color: #9b59b6;
    height: 100%;
    transition: width 1s linear;
    width: 0;
  }
  
  .logout-actions {
    margin-top: 16px;
  }
  
  .home-link {
    color: #9b59b6;
    font-size: 16px;
    font-weight: 600;
    text-decoration: none;
    transition: color 0.3s;
  }
  
  .home-link:hover {
    color: #8e44ad;
    text-decoration: underline;
  }
  </style>
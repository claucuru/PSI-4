<template>
    <div class="login-container">
      <div class="login-background">
        <div class="login-left">
          <div class="login-content">
            <h1 class="login-brand">TournamentMaster</h1>
            <p class="login-tagline">La plataforma líder para gestión de torneos de ajedrez</p>
          </div>
        </div>
        <div class="login-right">
          <div class="login-card">
            <h1 class="login-title">Iniciar sesión</h1>
            <p class="login-subtitle">Acceso a administración de torneos</p>
            
            <div v-if="error" class="error-message" data-cy="login-error">
              {{ error }}
            </div>
            
            <form @submit.prevent="handleLogin" class="login-form">
              <div class="form-group">
                <label for="username">Nombre de usuario</label>
                <div class="input-container">
                  <span class="input-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                      <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                  </span>
                  <input 
                    type="text" 
                    id="username" 
                    v-model="username" 
                    placeholder="Introduce tu nombre de usuario"
                    data-cy="username-input"
                    required
                  >
                </div>
              </div>
              
              <div class="form-group">
                <label for="password">Contraseña</label>
                <div class="input-container">
                  <span class="input-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    </svg>
                  </span>
                  <input 
                    type="password" 
                    id="password" 
                    v-model="password" 
                    placeholder="Introduce tu contraseña"
                    data-cy="password-input"
                    required
                  >
                </div>
              </div>
              
              <button 
                type="submit" 
                class="login-button" 
                data-cy="login-button"
                :disabled="isLoading"
              >
                <span v-if="isLoading" class="loading-spinner"></span>
                {{ isLoading ? 'Iniciando sesión...' : 'Iniciar sesión' }}
              </button>
            </form>
            
            <div class="login-footer">
              <router-link to="/" class="back-link">Volver a la página principal</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  
  export default {
    name: 'LoginView',
    setup() {
      const username = ref('')
      const password = ref('')
      const error = ref('')
      const isLoading = ref(false)
      const router = useRouter()
      const authStore = useAuthStore()
  
      const handleLogin = async () => {
        try {
          error.value = ''
          isLoading.value = true
          
          await authStore.login(username.value, password.value)
          
          // Redirigir al usuario a la página principal después del inicio de sesión exitoso
          router.push('/')
        } catch (err) {
          error.value = err.response?.data?.non_field_errors?.[0] || 
                        'Error al iniciar sesión. Por favor, verifica tus credenciales.'
          console.error('Error de inicio de sesión:', err)
        } finally {
          isLoading.value = false
        }
      }
  
      return {
        username,
        password,
        error,
        isLoading,
        handleLogin
      }
    }
  }
  </script>
  
  <style scoped>
  .login-container {
    width: 100%;
    height: 100vh;
    overflow: hidden;
  }
  
  .login-background {
    display: flex;
    width: 100%;
    height: 100%;
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
  
  .login-left::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1MDAiIGhlaWdodD0iNTAwIj48ZmlsdGVyIGlkPSJub2lzZSIgeD0iMCIgeT0iMCIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSI+PGZlVHVyYnVsZW5jZSB0eXBlPSJmcmFjdGFsTm9pc2UiIGJhc2VGcmVxdWVuY3k9IjAuNjUiIG51bU9jdGF2ZXM9IjMiIHN0aXRjaFRpbGVzPSJzdGl0Y2giIHJlc3VsdD0ibm9pc2UiLz48ZmVTcGVjdWxhckxpZ2h0aW5nIHNwZWN1bGFyRXhwb25lbnQ9IjIwIiBzcGVjdWxhckNvbnN0YW50PSIwLjgiIHN1cmZhY2VTY2FsZT0iMTUiIGxpZ2h0aW5nLWNvbG9yPSIjZmZmZmZmIiBpbj0ibm9pc2UiIHJlc3VsdD0ic3BlY09udCIvPjwvZmlsdGVyPjxyZWN0IHdpZHRoPSI1MDAiIGhlaWdodD0iNTAwIiBmaWxsPSJ0cmFuc3BhcmVudCIgZmlsdGVyPSJ1cmwoI25vaXNlKSIgb3BhY2l0eT0iMC4xIi8+PC9zdmc+');
    opacity: 0.1;
    z-index: 1;
  }
  
  .login-content {
    position: relative;
    z-index: 2;
    text-align: center;
    width: 80%;
  }
  
  .login-brand {
    font-size: 48px;
    font-weight: 700;
    margin-bottom: 16px;
    letter-spacing: -1px;
  }
  
  .login-tagline {
    font-size: 20px;
    opacity: 0.9;
    max-width: 500px;
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
    border-radius: 16px;
    box-shadow: 0 8px 30px rgba(186, 150, 211, 0.15);
    width: 100%;
    max-width: 460px;
    padding: 48px;
  }
  
  .login-title {
    color: #8e44ad;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 8px;
  }
  
  .login-subtitle {
    color: #9f7ead;
    font-size: 16px;
    margin-bottom: 32px;
  }
  
  .login-form {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  .form-group label {
    color: #6b5876;
    font-size: 14px;
    font-weight: 600;
  }
  
  .input-container {
    position: relative;
  }
  
  .input-icon {
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
    color: #9f7ead;
  }
  
  .form-group input {
    border: 2px solid #e6d5f2;
    border-radius: 10px;
    color: #333;
    font-size: 16px;
    padding: 14px 16px 14px 46px;
    transition: all 0.3s;
    width: 100%;
  }
  
  .form-group input:focus {
    border-color: #bb8fce;
    outline: none;
    box-shadow: 0 0 0 4px rgba(187, 143, 206, 0.15);
  }
  
  .login-button {
    background-color: #9b59b6;
    border: none;
    border-radius: 10px;
    color: white;
    cursor: pointer;
    font-size: 16px;
    font-weight: 600;
    margin-top: 16px;
    padding: 16px;
    transition: all 0.3s;
    position: relative;
  }
  
  .login-button:hover {
    background-color: #8e44ad;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(155, 89, 182, 0.2);
  }
  
  .login-button:active {
    transform: translateY(0);
  }
  
  .login-button:disabled {
    background-color: #d5b8e0;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
  
  .loading-spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    margin-right: 8px;
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
    border-radius: 8px;
    color: #c0392b;
    margin-bottom: 24px;
    padding: 14px;
    font-size: 14px;
  }
  
  .login-footer {
    margin-top: 32px;
    text-align: center;
  }
  
  .back-link {
    color: #9b59b6;
    font-size: 15px;
    font-weight: 500;
    text-decoration: none;
    transition: color 0.3s;
  }
  
  .back-link:hover {
    color: #8e44ad;
    text-decoration: underline;
  }
  
  /* Responsive */
  @media (max-width: 1024px) {
    .login-background {
      flex-direction: column;
    }
    
    .login-left {
      height: 200px;
      padding: 20px;
    }
    
    .login-right {
      padding: 30px 20px;
    }
    
    .login-card {
      padding: 30px;
    }
    
    .login-brand {
      font-size: 36px;
    }
    
    .login-tagline {
      font-size: 16px;
    }
  }
  </style>


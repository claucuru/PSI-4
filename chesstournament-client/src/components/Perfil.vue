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
            <p class="profile-subtitle">Información personal y preferencias</p>
            
            <div v-if="error" class="error-message" data-cy="profile-error">
              {{ error }}
            </div>
            
            <div v-if="successMessage" class="success-message" data-cy="profile-success">
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
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                      <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                  </span>
                  <input 
                    type="text" 
                    id="username" 
                    v-model="user.username" 
                    placeholder="Nombre de usuario"
                    data-cy="username-input"
                    disabled
                  >
                </div>
              </div>
              
              <div class="form-group">
                <label for="name">Nombre completo</label>
                <div class="input-container">
                  <span class="input-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                      <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                  </span>
                  <input 
                    type="text" 
                    id="name" 
                    v-model="user.name" 
                    placeholder="Tu nombre completo"
                    data-cy="name-input"
                    required
                  >
                </div>
              </div>
              
              <div class="form-group">
                <label for="email">Correo electrónico</label>
                <div class="input-container">
                  <span class="input-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                      <polyline points="22,6 12,13 2,6"></polyline>
                    </svg>
                  </span>
                  <input 
                    type="email" 
                    id="email" 
                    v-model="user.email" 
                    placeholder="Tu correo electrónico"
                    data-cy="email-input"
                    required
                  >
                </div>
              </div>
              
              <div class="form-group">
                <label for="lichessUsername">ID de Lichess</label>
                <div class="input-container">
                  <span class="input-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                      <path d="M2 17l10 5 10-5"></path>
                      <path d="M2 12l10 5 10-5"></path>
                    </svg>
                  </span>
                  <input 
                    type="text" 
                    id="lichessUsername" 
                    v-model="user.lichessUsername" 
                    placeholder="Tu nombre de usuario en Lichess"
                    data-cy="lichess-input"
                  >
                </div>
              </div>
              
              <div class="form-group">
                <label for="fideId">ID FIDE (opcional)</label>
                <div class="input-container">
                  <span class="input-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                      <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                  </span>
                  <input 
                    type="text" 
                    id="fideId" 
                    v-model="user.fideId" 
                    placeholder="Tu identificador FIDE (si tienes)"
                    data-cy="fide-input"
                  >
                </div>
              </div>
              
              <h2 class="section-title">Cambiar contraseña</h2>
              
              <div class="form-group">
                <label for="currentPassword">Contraseña actual</label>
                <div class="input-container">
                  <span class="input-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    </svg>
                  </span>
                  <input 
                    type="password" 
                    id="currentPassword" 
                    v-model="passwordData.currentPassword" 
                    placeholder="Introduce tu contraseña actual"
                    data-cy="current-password-input"
                  >
                </div>
              </div>
              
              <div class="form-group">
                <label for="newPassword">Nueva contraseña</label>
                <div class="input-container">
                  <span class="input-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    </svg>
                  </span>
                  <input 
                    type="password" 
                    id="newPassword" 
                    v-model="passwordData.newPassword" 
                    placeholder="Introduce tu nueva contraseña"
                    data-cy="new-password-input"
                  >
                </div>
              </div>
              
              <div class="form-group">
                <label for="confirmPassword">Confirmar nueva contraseña</label>
                <div class="input-container">
                  <span class="input-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    </svg>
                  </span>
                  <input 
                    type="password" 
                    id="confirmPassword" 
                    v-model="passwordData.confirmPassword" 
                    placeholder="Confirma tu nueva contraseña"
                    data-cy="confirm-password-input"
                  >
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
                  {{ isLoading ? 'Guardando...' : 'Guardar cambios' }}
                </button>
                
                <router-link to="/admin/home" class="cancel-button">
                  Cancelar
                </router-link>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
</template>
  
<script>
  import { useAuthStore } from '@/stores/auth'
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  
  export default {
    name: 'PerfilView',
    setup() {
      const user = ref({
        username: '',
        name: '',
        email: '',
        lichessUsername: '',
        fideId: '',
        photoUrl: null
      })
      
      const passwordData = ref({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      })
      
      const error = ref('')
      const successMessage = ref('')
      const isLoading = ref(false)
      const fileInput = ref(null)
      const authStore = useAuthStore()
      const router = useRouter()
      
      onMounted(async () => {
        // Obtener datos del usuario actual
        try {
          isLoading.value = true
          // Aquí iría la llamada a la API para obtener el perfil
          // Simulamos datos para el ejemplo
          const userData = await fetchUserProfile()
          user.value = { ...userData }
        } catch (err) {
          error.value = 'No se pudo cargar la información del perfil.'
          console.error('Error al cargar perfil:', err)
        } finally {
          isLoading.value = false
        }
      })
      
      // Función simulada para obtener el perfil
      const fetchUserProfile = async () => {
        // En producción, esto sería una llamada a tu API
        return new Promise(resolve => {
          setTimeout(() => {
            resolve({
              username: authStore.user?.username || 'usuario_ajedrez',
              name: 'Usuario de Ejemplo',
              email: 'ejemplo@tournamentmaster.com',
              lichessUsername: 'maestro_del_tablero',
              fideId: '12345678',
              photoUrl: null
            })
          }, 500)
        })
      }
      
      const getUserInitials = () => {
        if (!user.value.name) return '?'
        return user.value.name
          .split(' ')
          .map(name => name[0])
          .join('')
          .toUpperCase()
          .substring(0, 2)
      }
      
      const triggerFileInput = () => {
        fileInput.value.click()
      }
      
      const handleFileChange = (event) => {
        const file = event.target.files[0]
        if (!file) return
        
        // Aquí podrías subir la imagen a tu servidor
        // Por ahora solo simulamos una vista previa local
        const reader = new FileReader()
        reader.onload = (e) => {
          user.value.photoUrl = e.target.result
        }
        reader.readAsDataURL(file)
      }
      
      const saveProfile = async () => {
        try {
          error.value = ''
          successMessage.value = ''
          isLoading.value = true
          
          // Validar contraseñas si se intenta cambiar
          if (passwordData.value.newPassword || passwordData.value.currentPassword) {
            if (!passwordData.value.currentPassword) {
              error.value = 'Debes introducir tu contraseña actual para cambiarla.'
              isLoading.value = false
              return
            }
            
            if (passwordData.value.newPassword !== passwordData.value.confirmPassword) {
              error.value = 'Las nuevas contraseñas no coinciden.'
              isLoading.value = false
              return
            }
          }
          
          // Aquí iría la llamada a la API para guardar los cambios
          // Simulamos una espera
          await new Promise(resolve => setTimeout(resolve, 1000))
          
          // Simular éxito
          successMessage.value = 'Perfil actualizado correctamente.'
          // Limpiar los campos de contraseña
          passwordData.value = {
            currentPassword: '',
            newPassword: '',
            confirmPassword: ''
          }
        } catch (err) {
          error.value = err.response?.data?.message || 
                        'Error al actualizar el perfil. Por favor, inténtalo de nuevo.'
          console.error('Error al guardar perfil:', err)
        } finally {
          isLoading.value = false
        }
      }
      
      return {
        user,
        passwordData,
        error,
        successMessage,
        isLoading,
        fileInput,
        getUserInitials,
        triggerFileInput,
        handleFileChange,
        saveProfile
      }
    }
  }
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
    background-image: 
      linear-gradient(45deg, rgba(255,255,255,0.05) 25%, transparent 25%),
      linear-gradient(-45deg, rgba(255,255,255,0.05) 25%, transparent 25%),
      linear-gradient(45deg, transparent 75%, rgba(255,255,255,0.05) 75%),
      linear-gradient(-45deg, transparent 75%, rgba(255,255,255,0.05) 75%);
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
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
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
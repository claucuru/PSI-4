<template>
  <header class="main-header">
    <div class="header-container">
      <div class="header-left">
        <router-link to="/" class="logo">
          <span class="logo-text">TournamentMaster</span>
        </router-link>
      </div>
      
      <nav class="main-nav">
        <router-link to="/" class="nav-link" exact-active-class="active">Inicio</router-link>
        <router-link to="/torneos" class="nav-link" active-class="active">Torneos</router-link>
        <router-link to="/rankings" class="nav-link" active-class="active">Rankings</router-link>
        <router-link to="/noticias" class="nav-link" active-class="active">Noticias</router-link>
        <router-link to="/contacto" class="nav-link" active-class="active">Contacto</router-link>
      </nav>
      
      <div class="header-right">
        <template v-if="isAuthenticated">
          <div class="user-menu" @click="toggleUserMenu" ref="userMenuTrigger">
            <span class="user-avatar">
              <span class="user-initial">{{ userInitial }}</span>
            </span>
            <span class="user-name">{{ username }}</span>
            <span class="dropdown-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </span>
            
            <div class="user-dropdown" v-if="showUserMenu" ref="userMenu">
              <router-link to="/perfil" class="dropdown-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                Mi perfil
              </router-link>
              <router-link to="/mis-torneos" class="dropdown-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M18 8h1a4 4 0 0 1 0 8h-1"></path>
                  <path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"></path>
                  <line x1="6" y1="1" x2="6" y2="4"></line>
                  <line x1="10" y1="1" x2="10" y2="4"></line>
                  <line x1="14" y1="1" x2="14" y2="4"></line>
                </svg>
                Mis torneos
              </router-link>
              <router-link to="/admin" class="dropdown-item" v-if="isAdmin">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 20h9"></path>
                  <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                </svg>
                Administración
              </router-link>
              <div class="dropdown-divider"></div>
              <a href="#" class="dropdown-item logout" @click.prevent="handleLogout">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16 17 21 12 16 7"></polyline>
                  <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
                Cerrar sesión
              </a>
            </div>
          </div>
        </template>
        <template v-else>
          <router-link to="/log-in" class="login-btn" v-if="$route.name !== 'login'">
            <span class="login-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
                <polyline points="10 17 15 12 10 7"></polyline>
                <line x1="15" y1="12" x2="3" y2="12"></line>
              </svg>
            </span>
            Iniciar sesión
          </router-link>
        </template>
      </div>
      
      <button class="mobile-menu-toggle" @click="toggleMobileMenu">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>
    </div>
    
    <div class="mobile-menu" :class="{ 'active': showMobileMenu }">
      <nav class="mobile-nav">
        <router-link to="/" class="mobile-nav-link" exact-active-class="active" @click="closeMobileMenu">Inicio</router-link>
        <router-link to="/torneos" class="mobile-nav-link" active-class="active" @click="closeMobileMenu">Torneos</router-link>
        <router-link to="/rankings" class="mobile-nav-link" active-class="active" @click="closeMobileMenu">Rankings</router-link>
        <router-link to="/noticias" class="mobile-nav-link" active-class="active" @click="closeMobileMenu">Noticias</router-link>
        <router-link to="/contacto" class="mobile-nav-link" active-class="active" @click="closeMobileMenu">Contacto</router-link>
        
        <template v-if="isAuthenticated">
          <div class="mobile-divider"></div>
          <router-link to="/perfil" class="mobile-nav-link" @click="closeMobileMenu">Mi perfil</router-link>
          <router-link to="/mis-torneos" class="mobile-nav-link" @click="closeMobileMenu">Mis torneos</router-link>
          <router-link to="/admin" class="mobile-nav-link" v-if="isAdmin" @click="closeMobileMenu">Administración</router-link>
          <a href="#" class="mobile-nav-link logout" @click.prevent="handleLogout">Cerrar sesión</a>
        </template>
        <template v-else>
          <div class="mobile-divider"></div>
          <router-link to="/log-in" class="mobile-nav-link" @click="closeMobileMenu">
            Iniciar sesión
          </router-link>
        </template>
      </nav>
    </div>
  </header>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'HeaderComponent',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const showUserMenu = ref(false)
    const showMobileMenu = ref(false)
    const userMenuTrigger = ref(null)
    const userMenu = ref(null)
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const username = computed(() => authStore.user?.username || 'Usuario')
    const isAdmin = computed(() => authStore.user?.is_staff || false)
    
    const userInitial = computed(() => {
      if (!username.value) return 'U'
      return username.value.charAt(0).toUpperCase()
    })
    
    const toggleUserMenu = () => {
      showUserMenu.value = !showUserMenu.value
    }
    
    const toggleMobileMenu = () => {
      showMobileMenu.value = !showMobileMenu.value
    }
    
    const closeMobileMenu = () => {
      showMobileMenu.value = false
    }
    
    const handleLogout = async () => {
      await authStore.logout()
      router.push('/logout-success')
    }
    
    const closeMenuOnOutsideClick = (event) => {
      if (
        showUserMenu.value &&
        userMenuTrigger.value &&
        userMenu.value &&
        !userMenuTrigger.value.contains(event.target) &&
        !userMenu.value.contains(event.target)
      ) {
        showUserMenu.value = false
      }
    }
    
    onMounted(() => {
      document.addEventListener('click', closeMenuOnOutsideClick)
    })
    
    onUnmounted(() => {
      document.removeEventListener('click', closeMenuOnOutsideClick)
    })
    
    return {
      isAuthenticated,
      username,
      isAdmin,
      userInitial,
      showUserMenu,
      showMobileMenu,
      userMenuTrigger,
      userMenu,
      toggleUserMenu,
      toggleMobileMenu,
      closeMobileMenu,
      handleLogout
    }
  }
}
</script>

<style scoped>
.main-header {
  background-color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 70px;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
}

.logo-text {
  color: #8e44ad;
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.main-nav {
  display: flex;
  margin-left: 40px;
}

.nav-link {
  color: #6b5876;
  font-size: 15px;
  font-weight: 500;
  padding: 8px 16px;
  text-decoration: none;
  transition: color 0.2s;
}

.nav-link:hover, .nav-link.active {
  color: #9b59b6;
}

.header-right {
  display: flex;
  align-items: center;
}

.login-btn {
  background-color: #9b59b6;
  border-radius: 8px;
  color: white;
  display: flex;
  align-items: center;
  font-size: 14px;
  font-weight: 600;
  padding: 10px 16px;
  text-decoration: none;
  transition: all 0.2s;
}

.login-btn:hover {
  background-color: #8e44ad;
  transform: translateY(-2px);
}

.login-icon {
  margin-right: 8px;
}

.user-menu {
  position: relative;
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.user-menu:hover {
  background-color: #f8f0fd;
}

.user-avatar {
  background-color: #9b59b6;
  border-radius: 50%;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  margin-right: 10px;
}

.user-initial {
  font-size: 16px;
  font-weight: 600;
}

.user-name {
  color: #333;
  font-size: 14px;
  font-weight: 500;
  margin-right: 6px;
}

.dropdown-icon {
  color: #9f7ead;
}

.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 5px 25px rgba(0, 0, 0, 0.1);
  width: 220px;
  padding: 8px 0;
  z-index: 100;
}

.dropdown-item {
  color: #6b5876;
  display: flex;
  align-items: center;
  font-size: 14px;
  padding: 10px 16px;
  text-decoration: none;
  transition: background-color 0.2s;
}

.dropdown-item svg {
  margin-right: 10px;
  color: #9f7ead;
}

.dropdown-item:hover {
  background-color: #f8f0fd;
  color: #8e44ad;
}

.dropdown-item:hover svg {
  color: #9b59b6;
}

.dropdown-item.logout {
  color: #e74c3c;
}

.dropdown-item.logout svg {
  color: #e74c3c;
}

.dropdown-item.logout:hover {
  background-color: #fdecef;
}

.dropdown-divider {
  height: 1px;
  background-color: #e6d5f2;
  margin: 8px 0;
}

.mobile-menu-toggle {
  background: none;
  border: none;
  color: #6b5876;
  cursor: pointer;
  display: none;
  padding: 8px;
}

.mobile-menu {
  background-color: white;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.05);
  display: none;
  height: 0;
  overflow: hidden;
  transition: height 0.3s ease-in-out;
}

.mobile-menu.active {
  height: auto;
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  padding: 16px;
}

.mobile-nav-link {
  color: #6b5876;
  font-size: 16px;
  padding: 12px 16px;
  text-decoration: none;
  transition: color 0.2s;
}

.mobile-nav-link:hover, .mobile-nav-link.active {
  color: #9b59b6;
}

.mobile-nav-link.logout {
  color: #e74c3c;
}

.mobile-divider {
  height: 1px;
  background-color: #e6d5f2;
  margin: 8px 0;
}

@media (max-width: 992px) {
  .main-nav {
    display: none;
  }
  
  .mobile-menu-toggle {
    display: block;
  }
  
  .mobile-menu {
    display: block;
  }
}

@media (max-width: 576px) {
  .header-container {
    height: 60px;
    padding: 0 16px;
  }
  
  .logo-text {
    font-size: 18px;
  }
  
  .user-name {
    display: none;
  }
  
  .user-menu {
    padding: 8px;
  }
  
  .user-avatar {
    margin-right: 4px;
  }
}
</style>
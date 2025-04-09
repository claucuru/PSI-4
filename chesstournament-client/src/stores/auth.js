// src/stores/auth.js
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '../router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
    loading: false,
    error: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    getToken: (state) => state.token,
    getUser: (state) => state.user
  },
  
  actions: {
    async login(username, password) {
      this.loading = true
      this.error = null
      
      try {
        // Usando la API de Django con djoser para autenticación
        const response = await axios.post('http://localhost:8000/api/v1/token/login/', {
          username,
          password
        })
        
        // Guardar el token en el estado y localStorage
        this.token = response.data.auth_token
        localStorage.setItem('token', this.token)
        
        // Obtener información del usuario
        await this.fetchUserProfile()
        
        // Redireccionar a la página inicial
        router.push('/')
        return true
      } catch (err) {
        this.error = err.response?.data?.non_field_errors?.[0] || 'Error de autenticación'
        return false
      } finally {
        this.loading = false
      }
    },
    
    async fetchUserProfile() {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/users/me/', {
          headers: {
            'Authorization': `Token ${this.token}`
          }
        })
        
        this.user = response.data
        localStorage.setItem('user', JSON.stringify(response.data))
      } catch (err) {
        console.error('Error al obtener perfil de usuario:', err)
      }
    },
    
    async logout() {
      this.loading = true
      
      try {
        // Envía la solicitud de logout al servidor
        await axios.post('http://localhost:8000/api/v1/token/logout/', {}, {
          headers: {
            'Authorization': `Token ${this.token}`
          }
        })
      } catch (err) {
        console.error('Error al hacer logout:', err)
      } finally {
        // Independientemente de la respuesta del servidor, limpiamos localmente
        this.clearAuth()
        this.loading = false
        
        // Redireccionar a la página de logout
        router.push('/logout-success')
      }
    },
    
    clearAuth() {
      // Limpiar el estado
      this.token = null
      this.user = null
      
      // Limpiar el localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
})
<template>
  <div class="home-page">
    <HeaderComponent />
    
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Bienvenid@ a TournamentMaster</h1>
        <p class="hero-subtitle">La plataforma líder para gestión y seguimiento de torneos de ajedrez.</p>
        <div v-if="isAdmin">
        <div data-cy="admin-log" class="admin-welcome-message">Hello, you are logged in as an administrator</div>
        <router-link to="/createtournament" class="create-tournament-btn" data-cy="create-Tournament-button">
          Crea un torneo
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </router-link>
      </div>
      </div>
    </div>
    
    <div class="main-content">
      <div class="container">
        <div class="tournaments-header">
          <h2 class="section-title">Torneos disponibles</h2>
          
          <div class="search-bar">
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Buscar torneos por nombre..."
              @keyup.enter="handleSearch"
              class="search-input"
              data-cy="input-search"
            >
            <button class="search-button" @click="handleSearch" data-cy="submit-search">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </button>
          </div>
        </div>
      
        <!-- Estado de error -->
        <div v-if="apiErrors" class="error-state">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <h3>Ha ocurrido un error</h3>
          <p>{{ apiErrors }}</p>
        </div>
        
        <!-- Estado de carga -->
        <div v-else-if="isLoading" class="loading-state">
          <div class="spinner"></div>
          <p>Cargando torneos...</p>
        </div>
        
        <!-- Estado vacío -->
        <div v-else-if="tournaments.length === 0" class="empty-state">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <h3>No se encontraron torneos</h3>
          <p>Intenta con otros filtros de búsqueda o vuelve más tarde.</p>
        </div>
        
        <!-- Lista de torneos -->
         <!-- :data-cy=" isSearching ? 'search-' + tournament.name : tournament.name"-->
         <div v-else class="tournaments-grid">
          <router-link
            v-for="tournament in tournaments" 
            :key="tournament.id" 
            :to="`/tournamentdetail/${tournament.id}`"
            class="tournament-card"
            :data-cy=" isSearching ? 'search-' + tournament.name : tournament.name"
          >
            <div class="tournament-image">
              <div class="tournament-status" :class="getTournamentStatusClass(tournament)">
                {{ getTournamentStatusText(tournament) }}
              </div>
            </div>
            
            <div class="tournament-content">
              <div class="tournament-sport">
                {{ getTournamentTypeText(tournament.tournament_type) }}
              </div>
              <h3 class="tournament-title">{{ tournament.name }}</h3>
              <div class="tournament-info">
                <div class="info-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                  <span>{{ formatDate(tournament.start_date) }} - {{ tournament.end_date ? formatDate(tournament.end_date) : 'En curso' }}</span>
                </div>
                <div class="info-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                  </svg>
                  <span>{{ tournament.players ? tournament.players.length : 0 }} participantes</span>
                </div>
                <div class="info-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                    <circle cx="12" cy="10" r="3"></circle>
                  </svg>
                  <span>{{ tournament.board_type === 'OTB' ? 'Presencial' : 'Online' }}</span>
                </div>
                <div class="info-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                  </svg>
                  <span>{{ tournament.timeControl || 'Tiempo no especificado' }}</span>
                </div>
              </div>
              
              <div class="tournament-footer">
                <span class="view-details-btn"> Ver detalles</span>
              </div>
            </div>
          </router-link>
        </div>
        
        <!-- Paginación -->
        <div class="pagination" v-if="totalPages > 1 && !isSearching">
          <button 
            class="pagination-btn" 
            :disabled="currentPage === 1"
            @click="goToPage(currentPage - 1)"
            data-cy="previous-button"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
          </button>
          
          <div class="pagination-pages">
            <template v-for="page in displayedPages" :key="page">
              <button 
                v-if="page !== '...'" 
                class="page-number" 
                :class="{ active: page === currentPage }"
                @click="goToPage(page)"
                :data-cy="`page-${page}`"
              >
                {{ page }}
              </button>
              <span v-else class="page-ellipsis">...</span>
            </template>
          </div>
          
          <button 
            class="pagination-btn" 
            :disabled="currentPage === totalPages"
            @click="goToPage(currentPage + 1)"
            data-cy="next-button"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-logo">
          <h3>TournamentMaster</h3>
          <p>La plataforma líder para gestión de torneos de ajedrez.</p>
        </div>
        
        <div class="footer-authors">
          <h4>Desarrollado por:</h4>
          <div class="authors-list">
            <div class="author">
              <div class="author-avatar">
                <!-- Iniciales o ícono -->
                <span>AP</span>
              </div>
              <div class="author-info">
                <span class="author-name">Alejandra Palma</span>
              </div>
            </div>
            
            <div class="author">
              <div class="author-avatar">
                <span>CC</span>
              </div>
              <div class="author-info">
                <span class="author-name">Claudia Cuevas</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="footer-copyright">
          <p>&copy; 2025 TournamentMaster. Todos los derechos reservados.</p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
import axios from 'axios'
import { computed, onMounted, ref } from 'vue'
import HeaderComponent from './Header.vue'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'HomeView',
  components: {
    HeaderComponent
  },
  setup() {
    const tournaments = ref([])
    const isLoading = ref(true)
    const searchQuery = ref('')
    const currentPage = ref(1)
    const totalItems = ref(0)
    const itemsPerPage = 5
    const apiErrors = ref(null)
    const isSearching = ref(false)

    const isAdmin = ref(false)
    
    // Función para verificar si el usuario actual es administrador
    const checkAdminStatus = async () => {
        try {
          isAdmin.value = false
          
          // Verificar si el usuario está autenticado
          if (!authStore.isAuthenticated) {
            console.log('Usuario no autenticado')
            return false
          }
          
          // Obtener información del usuario actual
          const currentUser = authStore.getUser
          if (!currentUser || !currentUser.id) {
            console.log('No se pudo obtener información del usuario')
            return false
          }
          
          isAdmin.value = true
          
        } catch (error) {
          console.error('Error al verificar estado de administrador:', error)
          isAdmin.value = false
          return false
        }
    }
    

    const authStore = useAuthStore()
    
    const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage))
    
    // Cálculo de los números de página a mostrar
    const displayedPages = computed(() => {
      const pages = []
      const maxVisiblePages = 5
      
      if (totalPages.value <= maxVisiblePages) {
        for (let i = 1; i <= totalPages.value; i++) {
          pages.push(i)
        }
      } else {
        pages.push(1)
        
        let startPage = Math.max(2, currentPage.value - 1)
        let endPage = Math.min(totalPages.value - 1, startPage + 2)
        
        if (startPage > 2) {
          pages.push('...')
        }
        
        for (let i = startPage; i <= endPage; i++) {
          pages.push(i)
        }
        
        if (endPage < totalPages.value - 1) {
          pages.push('...')
        }
        
        pages.push(totalPages.value)
      }
      
      return pages
    })
    
    // Determinar el estado del torneo
    const getTournamentStatusClass = (tournament) => {
      if (!tournament.start_date) return 'proximo'
      
      const now = new Date()
      const startDate = new Date(tournament.start_date)
      
      if (startDate > now) return 'proximo'
      if (!tournament.end_date) return 'en_curso'
      
      const endDate = new Date(tournament.end_date)
      if (endDate < now) return 'finalizado'
      
      return 'en_curso'
    }
    
    // Obtener texto de estado para mostrar
    const getTournamentStatusText = (tournament) => {
      const status = getTournamentStatusClass(tournament)
      
      const statusMap = {
        'proximo': 'Próximo',
        'en_curso': 'En curso',
        'finalizado': 'Finalizado',
        'abierto': 'Inscripción abierta'
      }
      
      return statusMap[status] || 'Estado desconocido'
    }
    
    // Obtener el texto del tipo de torneo
    const getTournamentTypeText = (type) => {
      const typeMap = {
        'SW': 'Suizo',
        'RR': 'Round Robin',
        'KO': 'Eliminación',
        'TE': 'Por equipos',
        'SR': 'Single Round Robin' // Añadido este tipo que aparece en las pruebas
      }
      
      return typeMap[type] || 'Ajedrez'
    }
      // Cargar torneos desde la API
      const loadTournaments = async () => {
        isLoading.value = true
        apiErrors.value = null
        isSearching.value = searchQuery.value.trim() !== ''
        
        try {
          // Si hay una búsqueda activa, usar el endpoint de búsqueda
          if (isSearching.value) {
            const response = await axios.post(
              `/searchTournaments/`,
              { search_string: searchQuery.value.trim() },
              { headers: { 'Content-Type': 'application/json' } }
            )
            
            console.log('Búsqueda respuesta:', response.data)
            
            // Procesar los resultados de búsqueda
            tournaments.value = Array.isArray(response.data) ? response.data : []
            totalItems.value = tournaments.value.length
          } else {
            // Si no hay búsqueda, cargar la lista de torneos
            const params = {
              page: currentPage.value,
              page_size: itemsPerPage
            }
            
            const response = await axios.get(`/tournaments/`, { params })
            
            console.log('Torneos respuesta:', response.data)
            
            // Procesar la respuesta paginada de la API
            if (response.data && Array.isArray(response.data.results)) {
              tournaments.value = response.data.results
              totalItems.value = response.data.count || response.data.results.length
            } else if (Array.isArray(response.data)) {
              tournaments.value = response.data
              totalItems.value = response.data.length
            } else {
              console.error('Formato de respuesta inesperado:', response.data)
              tournaments.value = []
              totalItems.value = 0
            }
          }
          
          console.log('Torneos procesados:', tournaments.value)
          
        } catch (error) {
          console.error('Error al cargar torneos:', error)
          
          if (error.message && error.message.includes('CORS')) {
            apiErrors.value = 'Error de acceso al servidor: CORS no configurado correctamente. Contacta al administrador.'
          } else {
            apiErrors.value = 'Error al cargar los torneos. Por favor, inténtalo de nuevo más tarde.'
          }
          
          tournaments.value = []
          totalItems.value = 0
        } finally {
          isLoading.value = false
        }
      }
      
      // Formateador de fechas
      const formatDate = (dateString) => {
        if (!dateString) return 'Fecha no disponible'
        
        try {
          const options = { day: '2-digit', month: '2-digit', year: 'numeric' }
          return new Date(dateString).toLocaleDateString('es-ES', options)
        } catch (error) {
          console.error('Error al formatear fecha:', dateString, error)
          return 'Fecha inválida'
        }
      }
      
      // Manejar búsqueda
      const handleSearch = () => {
        currentPage.value = 1
        loadTournaments()
      }
      
      // Cambiar de página
      const goToPage = (page) => {
        currentPage.value = page
        loadTournaments()
      }
      
      onMounted(() => {
        checkAdminStatus()
        loadTournaments()
      })
      
      return {
        tournaments,
        isAdmin,
        checkAdminStatus,
        isLoading,
        searchQuery,
        currentPage,
        totalPages,
        displayedPages,
        isSearching,
        apiErrors,
        formatDate,
        getTournamentStatusClass,
        getTournamentStatusText,
        getTournamentTypeText,
        handleSearch,
        goToPage
      }
    }
  }
  </script>
  
  <style scoped>
  @import '@/assets/style_home.css';
  </style>
<template>
  <div class="home-page">
    <HeaderComponent />
    
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Bienvenid@ a TournamentMaster</h1>
        <p class="hero-subtitle">La plataforma líder para gestión y seguimiento de torneos de ajedrez.</p>
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
            >
            <button class="search-button" @click="handleSearch">
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
        <div v-else class="tournaments-grid">
          <div 
            v-for="tournament in tournaments" 
            :key="tournament.id" 
            class="tournament-card"
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
                <router-link :to="`/torneos/${tournament.id}`" class="view-details-btn">
                  Ver detalles
                </router-link>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Paginación -->
        <div class="pagination" v-if="totalPages > 1 && !isSearching">
          <button 
            class="pagination-btn" 
            :disabled="currentPage === 1"
            @click="goToPage(currentPage - 1)"
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
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
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
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import HeaderComponent from './Header.vue'
import axios from 'axios'

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
    const itemsPerPage = 10
    const apiErrors = ref(null)
    const isSearching = ref(false)
    
    // Configurar la URL base para las solicitudes a la API
    const apiBaseUrl = '/api/v1'
    
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
        'TE': 'Por equipos'
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
            `${apiBaseUrl}/searchTournaments/`,
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
          
          const response = await axios.get(`${apiBaseUrl}/tournaments/`, { params })
          
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
      loadTournaments()
    })
    
    return {
      tournaments,
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
.home-page {
  min-height: 100vh;
  min-width: 100vw;
  background-color: #f8f9fa;
  display: flex;
  flex-direction: column;
}

.hero-section {
  background: linear-gradient(135deg, #a96fc0 0%, #ba8cce 100%);
  padding: 80px 20px;
  color: white;
  text-align: center;
  flex-shrink: 0;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 42px;
  font-weight: 700;
  margin-bottom: 16px;
}

.hero-subtitle {
  font-size: 20px;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.5;
}

.main-content {
  padding: 40px 0;
  flex-grow: 1;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  width: 100%;
}

.tournaments-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 20px;
}

.section-title {
  color: #333;
  font-size: 28px;
  font-weight: 700;
  margin: 0;
}

.search-bar {
  display: flex;
  max-width: 500px;
  width: 100%;
}

.search-input {
  border: 2px solid #e6d5f2;
  border-radius: 8px 0 0 8px;
  color: #333;
  flex: 1;
  font-size: 16px;
  padding: 12px 16px;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #bb8fce;
  outline: none;
}

.search-button {
  background-color: #9b59b6;
  border: none;
  border-radius: 0 8px 8px 0;
  color: white;
  cursor: pointer;
  padding: 0 20px;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #8e44ad;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  color: #6b5876;
}

.spinner {
  border: 4px solid rgba(155, 89, 182, 0.1);
  border-radius: 50%;
  border-top: 4px solid #9b59b6;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 80px 0;
  color: #6b5876;
}

.empty-state svg {
  color: #9f7ead;
  margin-bottom: 20px;
}

.empty-state h3 {
  font-size: 24px;
  margin-bottom: 12px;
}

.empty-state p {
  color: #9f7ead;
  max-width: 400px;
  margin: 0 auto;
  font-size: 16px;
}

.error-state {
  text-align: center;
  padding: 80px 0;
  color: #e74c3c;
}

.error-state svg {
  color: #e74c3c;
  margin-bottom: 20px;
}

.error-state h3 {
  font-size: 24px;
  margin-bottom: 12px;
}

.error-state p {
  max-width: 400px;
  margin: 0 auto;
  font-size: 16px;
}

.tournaments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.tournament-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.tournament-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(155, 89, 182, 0.2);
}

.tournament-image {
  height: 180px;
  background-color: #edc0ff;
  background-image: linear-gradient(135deg, #e3b3f7 0%, #c288db 100%);
  position: relative;
}

.tournament-status {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 6px 12px;
  border-radius: 50px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.tournament-status.proximo {
  background-color: #f39c12;
  color: white;
}

.tournament-status.en_curso {
  background-color: #3498db;
  color: white;
}

.tournament-status.finalizado {
  background-color: #95a5a6;
  color: white;
}

.tournament-status.abierto {
  background-color: #27ae60;
  color: white;
}

.tournament-content {
  padding: 24px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.tournament-sport {
  color: #9b59b6;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 10px;
}

.tournament-title {
  color: #333;
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 16px 0;
  line-height: 1.3;
}

.tournament-info {
  margin-bottom: 24px;
  flex-grow: 1;
}

.info-item {
  display: flex;
  align-items: center;
  color: #6b5876;
  font-size: 15px;
  margin-bottom: 10px;
}

.info-item svg {
  color: #c4abcf;
  margin-right: 10px;
  flex-shrink: 0;
}

.tournament-footer {
  border-top: 1px solid #e6d5f2;
  padding-top: 16px;
}

.view-details-btn {
  background-color: transparent;
  border: 2px solid #9b59b6;
  border-radius: 8px;
  color: #9b59b6;
  display: block;
  font-size: 15px;
  font-weight: 600;
  padding: 10px;
  text-align: center;
  text-decoration: none;
  transition: all 0.3s;
}

.view-details-btn:hover {
  background-color: #9b59b6;
  color: white;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 40px;
}

.pagination-btn {
  background-color: white;
  border: 1px solid #e6d5f2;
  border-radius: 8px;
  color: #6b5876;
  cursor: pointer;
  padding: 10px 14px;
  transition: all 0.3s;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #f8f0fd;
  color: #9b59b6;
}

.pagination-btn:disabled {
  color: #d5b8e0;
  cursor: not-allowed;
}

.pagination-pages {
  display: flex;
  align-items: center;
  margin: 0 16px;
}

.page-number {
  background-color: transparent;
  border: none;
  border-radius: 4px;
  color: #6b5876;
  cursor: pointer;
  font-size: 15px;
  margin: 0 6px;
  padding: 8px 12px;
  transition: all 0.3s;
}

.page-number.active {
  background-color: #9b59b6;
  color: white;
  font-weight: 600;
}

.page-number:hover:not(.active) {
  background-color: #f8f0fd;
  color: #9b59b6;
}

.page-ellipsis {
  color: #9f7ead;
  margin: 0 6px;
}

/* Responsive */
@media (max-width: 1200px) {
  .container {
    max-width: 1000px;
  }
  
  .tournaments-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
}

@media (max-width: 992px) {
  .hero-title {
    font-size: 36px;
  }
  
  .hero-subtitle {
    font-size: 18px;
  }
  
  .tournaments-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .search-bar {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 60px 20px;
  }
  
  .tournaments-grid {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 20px;
  }
  
  .section-title {
    font-size: 24px;
  }
}

@media (max-width: 576px) {
  .hero-title {
    font-size: 28px;
  }
  
  .hero-subtitle {
    font-size: 16px;
  }
  
  .tournaments-grid {
    grid-template-columns: 1fr;
  }
  
  .pagination-pages {
    margin: 0 8px;
  }
  
  .page-number {
    margin: 0 2px;
    padding: 6px 8px;
  }
}
.site-footer {
  background-color: #8e44ad;
  color: white;
  padding: 40px 0;
  margin-top: auto;
}

.footer-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 30px;
}

.footer-logo h3 {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 10px 0;
}

.footer-logo p {
  opacity: 0.8;
  margin: 0;
}

.footer-authors h4 {
  font-size: 18px;
  margin: 0 0 15px 0;
}

.authors-list {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.author {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-avatar {
  width: 40px;
  height: 40px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.author-info {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-weight: 600;
}

.author-role {
  font-size: 14px;
  opacity: 0.8;
}

.footer-copyright {
  width: 100%;
  margin-top: 20px;
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    text-align: center;
  }
  
  .authors-list {
    justify-content: center;
  }
}
</style>
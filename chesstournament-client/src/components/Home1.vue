<template>
    <div class="home-page">
      <HeaderComponent />
      
      <div class="hero-section">
        <div class="hero-content">
          <h1 class="hero-title">Bienvenido a TournamentMaster</h1>
          <p class="hero-subtitle">La plataforma líder para gestión y seguimiento de torneos deportivos</p>
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
                placeholder="Buscar torneos..."
                @input="handleSearch"
                class="search-input"
              >
              <button class="search-button">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </button>
            </div>
          </div>
          
          <div class="tournaments-filters">
            <div class="filter-group">
              <label for="sport-filter">Deporte:</label>
              <select id="sport-filter" v-model="sportFilter" @change="handleFilters" class="filter-select">
                <option value="">Todos los deportes</option>
                <option value="futbol">Fútbol</option>
                <option value="baloncesto">Baloncesto</option>
                <option value="tenis">Tenis</option>
                <option value="padel">Pádel</option>
                <option value="voleibol">Voleibol</option>
              </select>
            </div>
            
            <div class="filter-group">
              <label for="status-filter">Estado:</label>
              <select id="status-filter" v-model="statusFilter" @change="handleFilters" class="filter-select">
                <option value="">Todos</option>
                <option value="abierto">Abierto a inscripciones</option>
                <option value="en_curso">En curso</option>
                <option value="finalizado">Finalizado</option>
                <option value="proximo">Próximo</option>
              </select>
            </div>
          </div>
          
          <div v-if="isLoading" class="loading-state">
            <div class="spinner"></div>
            <p>Cargando torneos...</p>
          </div>
          
          <div v-else-if="tournaments.length === 0" class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <h3>No se encontraron torneos</h3>
            <p>Intenta con otros filtros de búsqueda o vuelve más tarde.</p>
          </div>
          
          <div v-else class="tournaments-grid">
            <div v-for="tournament in tournaments" :key="tournament.id" class="tournament-card">
              <div class="tournament-image" :style="{ backgroundImage: `url(${tournament.image_url || '/default-tournament.jpg'})` }">
                <div class="tournament-status" :class="tournament.status">
                  {{ getStatusText(tournament.status) }}
                </div>
              </div>
              
              <div class="tournament-content">
                <div class="tournament-sport">{{ tournament.sport }}</div>
                <h3 class="tournament-title">{{ tournament.name }}</h3>
                <div class="tournament-info">
                  <div class="info-item">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                      <line x1="16" y1="2" x2="16" y2="6"></line>
                      <line x1="8" y1="2" x2="8" y2="6"></line>
                      <line x1="3" y1="10" x2="21" y2="10"></line>
                    </svg>
                    <span>{{ formatDate(tournament.start_date) }} - {{ formatDate(tournament.end_date) }}</span>
                  </div>
                  <div class="info-item">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                      <circle cx="9" cy="7" r="4"></circle>
                      <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                      <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                    </svg>
                    <span>{{ tournament.participants }} participantes</span>
                  </div>
                  <div class="info-item">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                      <circle cx="12" cy="10" r="3"></circle>
                    </svg>
                    <span>{{ tournament.location }}</span>
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
          <div class="pagination" v-if="totalPages > 1">
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
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue'
  import HeaderComponent from './Header.vue'
  
  export default {
    name: 'HomeView',
    components: {
      HeaderComponent
    },
    setup() {
      const tournaments = ref([])
      const isLoading = ref(true)
      const searchQuery = ref('')
      const sportFilter = ref('')
      const statusFilter = ref('')
      const currentPage = ref(1)
      const totalItems = ref(0)
      const itemsPerPage = 10
      
      // Datos de ejemplo - En una aplicación real, estos vendrían de una API
      const mockTournaments = [
        {
          id: 1,
          name: 'Campeonato Regional de Fútbol',
          sport: 'Fútbol',
          status: 'en_curso',
          start_date: '2025-05-15',
          end_date: '2025-06-30',
          location: 'Madrid',
          participants: 24,
          image_url: 'https://via.placeholder.com/800x500/9b59b6/ffffff?text=Fútbol'
        },
        {
          id: 2,
          name: 'Torneo Open de Tenis',
          sport: 'Tenis',
          status: 'abierto',
          start_date: '2025-07-10',
          end_date: '2025-07-25',
          location: 'Barcelona',
          participants: 32,
          image_url: 'https://via.placeholder.com/800x500/3498db/ffffff?text=Tenis'
        },
        {
          id: 3,
          name: 'Liga Amateur de Baloncesto',
          sport: 'Baloncesto',
          status: 'proximo',
          start_date: '2025-09-05',
          end_date: '2025-12-15',
          location: 'Valencia',
          participants: 16,
          image_url: 'https://via.placeholder.com/800x500/e74c3c/ffffff?text=Baloncesto'
        },
        {
          id: 4,
          name: 'Campeonato Nacional de Pádel',
          sport: 'Pádel',
          status: 'abierto',
          start_date: '2025-06-20',
          end_date: '2025-07-05',
          location: 'Sevilla',
          participants: 48,
          image_url: 'https://via.placeholder.com/800x500/27ae60/ffffff?text=Pádel'
        },
        {
          id: 5,
          name: 'Torneo Universitario de Voleibol',
          sport: 'Voleibol',
          status: 'finalizado',
          start_date: '2025-03-10',
          end_date: '2025-04-15',
          location: 'Málaga',
          participants: 12,
          image_url: 'https://via.placeholder.com/800x500/f39c12/ffffff?text=Voleibol'
        },
        {
          id: 6,
          name: 'Copa Internacional de Fútbol',
          sport: 'Fútbol',
          status: 'proximo',
          start_date: '2025-08-01',
          end_date: '2025-08-15',
          location: 'Bilbao',
          participants: 16,
          image_url: 'https://via.placeholder.com/800x500/9b59b6/ffffff?text=Fútbol'
        },
        {
          id: 7,
          name: 'Grand Slam de Tenis',
          sport: 'Tenis',
          status: 'en_curso',
          start_date: '2025-05-01',
          end_date: '2025-05-14',
          location: 'Madrid',
          participants: 128,
          image_url: 'https://via.placeholder.com/800x500/3498db/ffffff?text=Tenis'
        },
        {
          id: 8,
          name: 'Liga Provincial de Baloncesto',
          sport: 'Baloncesto',
          status: 'abierto',
          start_date: '2025-06-15',
          end_date: '2025-09-15',
          location: 'Zaragoza',
          participants: 10,
          image_url: 'https://via.placeholder.com/800x500/e74c3c/ffffff?text=Baloncesto'
        },
        {
          id: 9,
          name: 'Torneo de Verano de Pádel',
          sport: 'Pádel',
          status: 'proximo',
          start_date: '2025-07-01',
          end_date: '2025-07-15',
          location: 'Alicante',
          participants: 24,
          image_url: 'https://via.placeholder.com/800x500/27ae60/ffffff?text=Pádel'
        },
        {
          id: 10,
          name: 'Campeonato Escolar de Voleibol',
          sport: 'Voleibol',
          status: 'finalizado',
          start_date: '2025-02-10',
          end_date: '2025-03-05',
          location: 'Murcia',
          participants: 8,
          image_url: 'https://via.placeholder.com/800x500/f39c12/ffffff?text=Voleibol'
        },
        {
          id: 11,
          name: 'Mundial de Clubes',
          sport: 'Fútbol',
          status: 'en_curso',
          start_date: '2025-04-10',
          end_date: '2025-04-25',
          location: 'Madrid',
          participants: 8,
          image_url: 'https://via.placeholder.com/800x500/9b59b6/ffffff?text=Fútbol'
        },
        {
          id: 12,
          name: 'Master Nacional de Tenis',
          sport: 'Tenis',
          status: 'proximo',
          start_date: '2025-09-01',
          end_date: '2025-09-10',
          location: 'Barcelona',
          participants: 16,
          image_url: 'https://via.placeholder.com/800x500/3498db/ffffff?text=Tenis'
        }
      ]
      
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
      
      // Cargar torneos con simulación de API
      const loadTournaments = () => {
        isLoading.value = true
        
        // Simulación de retraso de API
        setTimeout(() => {
          // Filtrar torneos según los criterios de búsqueda
          let filteredTournaments = [...mockTournaments]
          
          if (searchQuery.value) {
            const query = searchQuery.value.toLowerCase()
            filteredTournaments = filteredTournaments.filter(t => 
              t.name.toLowerCase().includes(query) || 
              t.location.toLowerCase().includes(query) ||
              t.sport.toLowerCase().includes(query)
            )
          }
          
          if (sportFilter.value) {
            filteredTournaments = filteredTournaments.filter(t => 
              t.sport.toLowerCase() === sportFilter.value.toLowerCase()
            )
          }
          
          if (statusFilter.value) {
            filteredTournaments = filteredTournaments.filter(t => 
              t.status === statusFilter.value
            )
          }
          
          // Actualizar total de items
          totalItems.value = filteredTournaments.length
          
          // Aplicar paginación
          const start = (currentPage.value - 1) * itemsPerPage
          const end = start + itemsPerPage
          tournaments.value = filteredTournaments.slice(start, end)
          
          isLoading.value = false
        }, 500)
      }
      
      // Formateador de fechas
      const formatDate = (dateString) => {
        const options = { day: '2-digit', month: '2-digit', year: 'numeric' }
        return new Date(dateString).toLocaleDateString('es-ES', options)
      }
      
      // Obtener texto de estado para mostrar
      const getStatusText = (status) => {
        const statusMap = {
          abierto: 'Inscripción abierta',
          en_curso: 'En curso',
          finalizado: 'Finalizado',
          proximo: 'Próximo'
        }
        return statusMap[status] || status
      }
      
      // Manejar búsqueda
      const handleSearch = () => {
        currentPage.value = 1
        loadTournaments()
      }
      
      // Manejar cambios en filtros
      const handleFilters = () => {
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
        sportFilter,
        statusFilter,
        currentPage,
        totalPages,
        displayedPages,
        formatDate,
        getStatusText,
        handleSearch,
        handleFilters,
        goToPage
      }
    }
  }
  </script>
  
  <style scoped>
  .home-page {
    min-height: 100vh;
    background-color: #f8f9fa;
  }
  
  .hero-section {
    background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%);
    padding: 60px 20px;
    color: white;
    text-align: center;
  }
  
  .hero-content {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .hero-title {
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 16px;
  }
  
  .hero-subtitle {
    font-size: 18px;
    opacity: 0.9;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.5;
  }
  
  .main-content {
    padding: 40px 0;
  }
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
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
    font-size: 24px;
    font-weight: 700;
    margin: 0;
  }
  
  .search-bar {
    display: flex;
    max-width: 400px;
    width: 100%;
  }
  
  .search-input {
    border: 2px solid #e6d5f2;
    border-radius: 8px 0 0 8px;
    color: #333;
    flex: 1;
    font-size: 15px;
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
    padding: 0 16px;
    transition: background-color 0.3s;
  }
  
  .search-button:hover {
    background-color: #8e44ad;
  }
  
  .tournaments-filters {
    display: flex;
    gap: 20px;
    margin-bottom: 24px;
    flex-wrap: wrap;
  }
  
  .filter-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .filter-group label {
    color: #6b5876;
    font-size: 14px;
    font-weight: 600;
  }
  
  .filter-select {
    background-color: white;
    border: 2px solid #e6d5f2;
    border-radius: 8px;
    color: #333;
    font-size: 14px;
    padding: 10px 16px;
    transition: border-color 0.3s;
    min-width: 180px;
  }
  
  .filter-select:focus {
    border-color: #bb8fce;
    outline: none;
  }
  
  .loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 0;
    color: #6b5876;
  }
  
  .spinner {
    border: 4px solid rgba(155, 89, 182, 0.1);
    border-radius: 50%;
    border-top: 4px solid #9b59b6;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin-bottom: 16px;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  .empty-state {
    text-align: center;
    padding: 60px 0;
    color: #6b5876;
  }
  
  .empty-state svg {
    color: #9f7ead;
    margin-bottom: 16px;
  }
  
  .empty-state h3 {
    font-size: 20px;
    margin-bottom: 8px;
  }
  
  .empty-state p {
    color: #9f7ead;
    max-width: 400px;
    margin: 0 auto;
  }
  
  .tournaments-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 24px;
    margin-bottom: 40px;
  }
  
  .tournament-card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    overflow: hidden;
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .tournament-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(155, 89, 182, 0.15);
  }
  
  .tournament-image {
    height: 160px;
    background-size: cover;
    background-position: center;
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
  
  .tournament-status.abierto {
    background-color: #27ae60;
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
  
  .tournament-status.proximo {
    background-color: #f39c12;
    color: white;
  }
  
  .tournament-content {
    padding: 20px;
  }
  
  .tournament-sport {
    color: #9b59b6;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 8px;
  }
  
  .tournament-title {
    color: #333;
    font-size: 18px;
    font-weight: 700;
    margin: 0 0 16px 0;
    line-height: 1.3;
  }
  
  .tournament-info {
    margin-bottom: 20px;
  }
  
  .info-item {
    display: flex;
    align-items: center;
    color: #6b5876;
    font-size: 14px;
    margin-bottom: 8px;
  }
  
  .info-item svg {
    color: #9f7ead;
    margin-right: 8px;
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
    font-size: 14px;
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
    padding: 8px 12px;
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
    margin: 0 12px;
  }
  
  .page-number {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    color: #6b5876;
    cursor: pointer;
    font-size: 14px;
    margin: 0 4px;
    padding: 6px 10px;
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
    margin: 0 4px;
  }
  
  /* Responsive */
  @media (max-width: 992px) {
    .hero-title {
      font-size: 32px;
    }
    
    .hero-subtitle {
      font-size: 16px;
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
      padding: 40px 20px;
    }
    
    .tournaments-grid {
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 16px;
    }
    
    .section-title {
      font-size: 22px;
    }
  }
  
  @media (max-width: 576px) {
    .tournaments-grid {
      grid-template-columns: 1fr;
    }
    
    .filter-group {
      width: 100%;
    }
    
    .filter-select {
      flex: 1;
    }
    
    .pagination-pages {
      margin: 0 8px;
    }
    
    .page-number {
      margin: 0 2px;
      padding: 6px 8px;
    }
  }
  </style>
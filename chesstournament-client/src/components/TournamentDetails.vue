<template>
  <div class="tournament-details-page">
    <HeaderComponent />
    
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title" data-cy="tournament-title">{{ tournament ? tournament.name : 'Cargando torneo...' }}</h1>
        <p class="hero-subtitle" v-if="tournament">
          {{ getTournamentTypeText(tournament.tournament_type) }} | 
          {{ tournament.board_type === 'OTB' ? 'Presencial' : 'Online' }} |
          {{ tournament.timeControl || 'Tiempo no especificado' }}
        </p>
      </div>
    </div>

    <div class="main-content">
      <div class="container">
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
          <p>Cargando información del torneo...</p>
        </div>
        
        <div v-else-if="tournament" class="tournament-details">
          <!-- Información del torneo -->
          <div class="tournament-info-card">
            <div class="tournament-status-banner" :class="getTournamentStatusClass(tournament)">
              {{ getTournamentStatusText(tournament) }}
            </div>
            
            <div class="tournament-info-content">
              <div class="tournament-meta">
                <div class="meta-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                  <div>
                    <strong>Fechas:</strong>
                    <div>{{ formatDate(tournament.start_date) }} - {{ tournament.end_date ? formatDate(tournament.end_date) : 'En curso' }}</div>
                  </div>
                </div>
                
                <div class="meta-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                  </svg>
                  <div>
                    <strong>Participantes:</strong>
                    <div>{{ tournament.players ? tournament.players.length : 0 }} jugadores</div>
                  </div>
                </div>
                
                <div class="meta-item">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                  </svg>
                  <div>
                    <strong>Control de tiempo:</strong>
                    <div>{{ tournament.timeControl || 'No especificado' }}</div>
                  </div>
                </div>
              </div>
              
              <div class="tournament-description" v-if="tournament.description">
                <h3>Descripción</h3>
                <p>{{ tournament.description }}</p>
              </div>
            </div>
          </div>
          
          <!-- Mostramos todas las secciones en la misma página -->
          <div class="tournament-sections">
            <!-- Sección de Participantes -->
            <div class="section-container">
              <h2 class="tabs-header">Participantes</h2>
              
              <div v-if="playersLoading" class="loading-state mini">
                <div class="spinner"></div>
                <p>Cargando participantes...</p>
              </div>
              
              <div v-else-if="players.length === 0" class="empty-state mini">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <h3>No hay participantes registrados</h3>
              </div>
              
              <div v-else class="players-list">
                <table class="players-table">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Nombre</th>
                      <th>Username Lichess</th>
                      <th>Rating</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(player, index) in players" :key="player.id">
                      <td>{{ index + 1 }}</td>
                      <td>{{ player.name || 'N/A' }}</td>
                      <td>{{ player.lichess_username || 'N/A' }}</td>
                      <td>{{ getPlayerRating(player) || 'N/A' }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            
            <!-- Sección de Rondas y Partidas -->
            <div class="section-container">
              <h2 class="tabs-header">Rondas y Partidas</h2>
              
              <div v-if="roundsLoading" class="loading-state mini">
                <div class="spinner"></div>
                <p>Cargando rondas y partidas...</p>
              </div>
              
              <div v-else-if="!roundsData || roundsData.rounds.length === 0" class="empty-state mini">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <h3>No hay rondas configuradas</h3>
                <p>El torneo aún no ha sido emparejado o está en preparación.</p>
              </div>

              <div v-else class="rounds-list">
                <div v-for="(round, roundIndex) in roundsData.rounds.rounds" :key="round.round_id" class="round-card" :data-cy="`round_${roundIndex + 1}`">
                  <div class="round-header">
                    <h3>{{ "round_00" + (roundIndex + 1) }}</h3>
                    <div class="round-date" v-if="round.start_date">
                      {{ formatDate(round.start_date) }}
                    </div>
                  </div>
                  
                  <div class="games-list">
                    <div v-for="(game, gameIndex) in round.games" :key="game.game_id" 
                        class="game-item" 
                        :data-cy="`game_${roundIndex + 1}_${gameIndex + 1}`">
                      <div class="game-players">
                        <div class="player white">
                          <strong>{{ game.white.name || 'Sin jugador' }}</strong>
                          <span v-if="game.white.rating" class="rating">({{ game.white.rating }})</span>
                        </div>
                        <div class="game-result">
                          <!-- Select para usuarios normales - visible para no administradores -->
                          <select 
                            v-if="!isAdmin"
                            v-model="game.result" 
                            class="custom-select"
                            :data-cy="`select-${round.round_id}-${gameIndex + 1}`"
                          >
                            <option value="">-- Seleccionar --</option>
                            <option value="White wins (1-0)">White wins (1-0)</option>
                            <option value="B">Black wins (0-1)</option>
                            <option value="D">Draw (1/2-1/2)</option>
                            <option value="F">Forfeit (F-F)</option>
                          </select>

                          <!-- Select para administradores - visible solo para administradores -->
                          <select 
                            v-if="isAdmin"
                            v-model="game.result" 
                            class="custom-select"
                            :data-cy="`select-admin-${round.round_id}-${gameIndex + 1}`"
                          >
                            <option value="">-- Seleccionar --</option>
                            <option value="White wins (1-0)">White wins (1-0)</option>
                            <option value="B">Black wins (0-1)</option>
                            <option value="D">Draw (1/2-1/2)</option>
                            <option value="F">Forfeit (F-F)</option>
                          </select>
                          
                          <span 
                            class="result-display"
                            :data-cy="`input-${round.round_id}-${gameIndex + 1}`"
                          >
                            {{ formatGameResult(game.result) }}
                          </span>
                        </div>
                        
                        <div class="player black">
                          <strong>{{ game.black.name || 'Sin jugador' }}</strong>
                          <span v-if="game.black.rating" class="rating">({{ game.black.rating }})</span>
                        </div>
                      </div>
                      
                      <div class="game-actions">
                        <div class="game-status" :class="game.finished ? 'finished' : 'pending'">
                          {{ game.finished ? 'Finalizada' : 'Pendiente' }}
                        </div>
                        
                        <button 
                          class="edit-game-btn"
                          :data-cy="`button-${isAdmin ? 'admin-' : ''}${round.round_id}-${gameIndex + 1}`" 
                          @click="submitGameResult(round.round_id, game)"
                        >
                          Enviar resultado
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Agrega un elemento para mensajes de error globales -->
              <div v-if="globalError" class="error-state" data-cy="error-message">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <h3>Ha ocurrido un error</h3>
                <p>{{ globalError }}</p>
              </div>
            </div>
            
            <!-- Sección de Clasificación -->
            <div class="section-container" data-cy="ranking-section">
              <h2 class="tabs-header" data-cy="standing-accordion-button">Clasificación</h2>
              
              <div v-if="rankingsLoading" class="loading-state mini">
                <div class="spinner"></div>
                <p>Cargando clasificación...</p>
              </div>
              
              <div v-else-if="!rankings || Object.keys(rankings).length === 0" class="empty-state mini">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <h3>No hay clasificación disponible</h3>
                <p>La clasificación estará disponible cuando se hayan jugado partidas.</p>
              </div>
              
              <div v-else class="rankings-list">
                <table class="rankings-table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Points</th>
                      <th>Black</th>
                      <th>Wins</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(player, index) in rankingsSorted" :key="player.id" :data-cy="`ranking-${index + 1}`">
                      <td data-cy="name">{{ player.name }}&nbsp;</td>
                        <td data-cy="points">{{ player.score.toFixed(2) }}&nbsp;</td>
                        <td data-cy="black">{{ player.BT.toFixed(2) }}&nbsp;</td>
                        <td data-cy="wins">{{ player.WI.toFixed(2) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
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
import axios from 'axios'
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import HeaderComponent from './Header.vue'

export default {
  name: 'TournamentDetails',
  components: {
    HeaderComponent
  },
  setup() {
    const route = useRoute()
    const tournamentId = computed(() => route.params.id)
    
    // Estado
    const isLoading = ref(true)
    const apiErrors = ref(null)
    const tournament = ref(null)
    const players = ref([])
    const rankings = ref({})
    const roundsData = ref(null)
    const playersLoading = ref(false)
    const rankingsLoading = ref(false)
    const roundsLoading = ref(false)
    
    // Estado para la edición de partidas
    const showEditGameModal = ref(false)
    const editingGame = ref(null)
    const editingRoundId = ref(null)
    const editingGameError = ref(null)
    const updateGameLoading = ref(false)
    
    // URL base para solicitudes a la API
    const apiBaseUrl = '/api/v1'
    
    // Añade una nueva variable de estado para errores globales
    const globalError = ref(null)

    const isAdmin = ref(false)
    
    // Función para verificar si el usuario actual es administrador
    const checkAdminStatus = async (tournamentId) => {
        try {
            isAdmin.value = false
            const response = await axios.get(`${apiBaseUrl}/tournaments/${tournamentId.value}/`)
            tournament.value = response.data
            alert(`Tournament ID: ${tournamentId.value}`)
            
            if (tournament.value && tournament.value.administrativeUser) {
                const currentUserId = getCurrentUserId()
                isAdmin.value = (currentUserId === tournament.value.administrativeUser)
                alert(`Estado de administrador: ${isAdmin.value} (Usuario: ${currentUserId}, Admin: ${tournament.value.administrativeUser})`)
                console.log(`Estado de administrador: ${isAdmin.value} (Usuario: ${currentUserId}, Admin: ${tournament.value.administrativeUser})`)
            } else {
                isAdmin.value = false
            }
        } catch (error) {
            console.error('Error al verificar estado de administrador:', error)
            isAdmin.value = false
        }
    }

    const getCurrentUserId = () => {
        const userStr = localStorage.getItem('user')
        if (userStr) {
            try {
                const user = JSON.parse(userStr)
                return user.id
            } catch (e) {
                console.error('Error al obtener ID de usuario:', e)
            }
        }
        return null
    }
    
    const loadTournament = async () => {
        isLoading.value = true
        apiErrors.value = null
        globalError.value = null
        
        try {
            const response = await axios.get(`${apiBaseUrl}/tournaments/${tournamentId.value}/`)
            tournament.value = response.data
            
            console.log('Torneo cargado:', tournament.value)
            
            // Cargar todos los datos necesarios
            await loadPlayers()
            await loadRankings()
            await loadRounds()
            
        } catch (error) {
            console.error('Error al cargar torneo:', error)
            apiErrors.value = 'Error al cargar los datos del torneo. Por favor, inténtalo de nuevo más tarde.'
            
            // Comprobar si es un error de "Tournament name already exists"
            if (error.response && error.response.data) {
                if (error.response.data.detail && error.response.data.detail.includes('already exists')) {
                    globalError.value = 'Error: Tournament name already exists'
                }
            }
        } finally {
            isLoading.value = false
        }
    }

    // Modifica la función loadPlayers para manejar errores específicos
    const loadPlayers = async () => {
        playersLoading.value = true
        
        try {
            const response = await axios.get(`${apiBaseUrl}/get_players/${tournamentId.value}/`)
            players.value = response.data
            console.log('Jugadores cargados:', players.value)
        } catch (error) {
            console.error('Error al cargar jugadores:', error)
            apiErrors.value = 'Error al cargar los participantes.'
            
            // Comprobar si es un error de "can not add players"
            if (error.response && error.response.data) {
                if (error.response.data.detail && error.response.data.detail.includes('can not add players')) {
                    globalError.value = 'Error: can not add players to tournament'
                }
            }
        } finally {
            playersLoading.value = false
        }
    }
    
    // Cargar datos de clasificación
    const loadRankings = async () => {
        rankingsLoading.value = true
        
        try {
            const response = await axios.get(`${apiBaseUrl}/get_ranking/${tournamentId.value}/`)
            rankings.value = response.data

            console.log('Clasificación cargada:', rankings.value)
        } catch (error) {
            console.error('Error al cargar clasificación:', error)
            apiErrors.value = 'Error al cargar la clasificación.'
        } finally {
            rankingsLoading.value = false
        }
    }
    
    // Cargar datos de rondas
    const loadRounds = async () => {
        roundsLoading.value = true
        
        try {
            const response = await axios.get(`${apiBaseUrl}/get_round_results/${tournamentId.value}/`)
            roundsData.value = response.data
            console.log('Rondas cargadas:', roundsData.value)
        } catch (error) {
            console.error('Error al cargar rondas:', error)
            apiErrors.value = 'Error al cargar las rondas y partidas.'
        } finally {
            roundsLoading.value = false
        }
    }

    // Función para enviar el resultado de una partida
    const submitGameResult = async (roundId, game) => {
        try {
            // Si no hay resultado seleccionado, no enviar
            if (!game.result) {
                alert('Por favor, selecciona un resultado antes de enviar.')
                return
            }
            
            // Convertir el resultado al formato correcto para la API
            let resultCode = game.result
            if (game.result === 'White wins (1-0)') {
                resultCode = "W"
            }
            
            // Preparar datos para enviar
            const gameData = {
                game_id: game.game_id,
                result: resultCode
            }
            
            if (!isAdmin.value) {
                // Si no es admin, solicitar correo para verificación
                const userEmail = window.prompt('Por favor, ingresa tu correo electrónico para confirmar:')
                
                if (!userEmail) {
                    return // Si el usuario cancela, no continuar
                }
                
                // Validar el formato del correo electrónico
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
                if (!emailRegex.test(userEmail)) {
                    alert('Por favor, ingresa un correo electrónico válido.')
                    return
                }
                
                // Añadir email a los datos
                gameData.email = userEmail
                
                // Enviar resultado a la API para usuarios normales
                const response = await axios.post(`${apiBaseUrl}/update_game/`, gameData)
                console.log('Resultado enviado correctamente:', response.data)
            } else {
                // Enviar resultado a la API para administradores
                const response = await axios.post(`${apiBaseUrl}/admin_update_game/`, gameData)
                console.log('Resultado enviado correctamente (admin):', response.data)
            }
            
            // Marcar la partida como finalizada
            game.finished = true
            
            // Recargar la clasificación para reflejar los cambios
            loadRankings()
            
            // Mensaje de éxito
            alert(isAdmin.value ? 'Resultado actualizado correctamente (como administrador).' : 'Resultado enviado correctamente.')
            
        } catch (error) {
            console.error('Error al enviar el resultado:', error)
            alert('Error al enviar el resultado. Por favor, inténtalo de nuevo.')
            
            // Si hay un error específico de la API, mostrarlo
            if (error.response && error.response.data && error.response.data.detail) {
                alert(`Error: ${error.response.data.detail}`)
            }
        }
    }

    // Guardar los cambios de la partida
    const saveGameChanges = async () => {
        updateGameLoading.value = true
        editingGameError.value = null
        
        try {
            // Si el resultado está establecido pero finished es false, actualizar finished a true
            if (editingGame.value.result && !editingGame.value.finished) {
                editingGame.value.finished = true
            }

            // Convertir el resultado al formato correcto para la API
            let resultCode = editingGame.value.result
            if (editingGame.value.result === 'White wins (1-0)') {
                resultCode = "W"
            }
            
            // Enviar los datos actualizados a la API
            const response = await axios.post(
                `${apiBaseUrl}/admin_update_game/`,
                {
                    // Asegúrate de incluir todos los campos necesarios en el cuerpo de la solicitud
                    game_id: editingGame.value.game_id,
                    result: resultCode,
                    finished: editingGame.value.finished,
                }
            )
            console.log('Partida actualizada correctamente:', response.data)
            
            // Actualizar la partida en la lista local
            if (roundsData.value && roundsData.value.rounds) {
                const roundIndex = roundsData.value.rounds.rounds.findIndex(r => r.round_id === editingRoundId.value)
                
                if (roundIndex !== -1) {
                    const gameIndex = roundsData.value.rounds.rounds[roundIndex].games.findIndex(g => g.game_id === editingGame.value.game_id)
                    
                    if (gameIndex !== -1) {
                        roundsData.value.rounds.rounds[roundIndex].games[gameIndex] = { ...editingGame.value }
                    }
                }
            }
            
            // Actualizar la clasificación si hay cambios en los resultados
            loadRankings()
            
            // Cerrar el modal
            showEditGameModal.value = false
        } catch (error) {
            console.error('Error al actualizar la partida:', error)
            
            if (error.response && error.response.data) {
                editingGameError.value = error.response.data.detail || 'Error al guardar los cambios. Inténtalo de nuevo.'
            } else {
                editingGameError.value = 'Error de conexión. Por favor, verifica tu conexión a internet e inténtalo de nuevo.'
            }
        } finally {
            updateGameLoading.value = false
        }
    }
    
    // Abrir el modal para editar una partida
    const openEditGameModal = (roundId, game) => {
        // Crear una copia profunda del objeto para no modificar directamente el original
        editingGame.value = JSON.parse(JSON.stringify(game))
        editingGame.value.id = game.game_id // Asegurarse de que el ID de la partida esté presente
        editingRoundId.value = roundId
        editingGameError.value = null
        showEditGameModal.value = true
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
    
    // Determinar el estado del torneo
    const getTournamentStatusClass = (tournament) => {
        if (!tournament.start_date) return 'proximo'
        
        const now = new Date()
        const startDate = new Date(tournament.start_date)
        const endDate = tournament.end_date ? new Date(tournament.end_date) : null
        
        if (now < startDate) return 'proximo'
        if (endDate && now > endDate) return 'finalizado'
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
            'SR': 'Round Robin' // Añadido para ser compatible con el test
        }
        
        return typeMap[type] || 'Ajedrez'
    }
    
    // Obtener el rating del jugador según el tipo de torneo
    const getPlayerRating = (player) => {
      if (!tournament.value || !player) return null
      
      switch(tournament.value.tournament_speed) {
        case 'BL':
          return player.fide_rating_blitz || player.lichess_rating_blitz
        case 'RA':
          return player.fide_rating_rapid || player.lichess_rating_rapid
        default: // 'CL' - Classical
          return player.fide_rating_classical || player.lichess_rating_classical
      }
    }
      
    // Formatear el resultado de la partida para mostrar
    const formatGameResult = (result) => {
      const resultMap = {
        'White wins (1-0)': '1-0',
        'B': '0-1',
        'D': '½-½',
        'F': 'F-F' // Forfeit
      }
      
      return resultMap[result] || '-'
    }
      
    // Obtener la clase CSS según el resultado
    const getGameResultClass = (result) => {
      return {
        'White wins (1-0)': 'white-win',
        'B': 'black-win',
        'D': 'draw',
        'F': 'forfeit'
      }[result] || ''
    }
      
    // Ordenar rankings por posición
    const rankingsSorted = computed(() => {
      return Object.values(rankings.value)
        .sort((a, b) => a.rank - b.rank).map(player => ({
          ...player,
          rank: player.rank,
          score: parseFloat(player.score.toFixed(2)),
          BT: parseFloat(player.BT.toFixed(2) || 0),
          WI: parseFloat(player.WI.toFixed(2) || 0),
        }))
    })
      
    onMounted(() => {
      loadTournament()
      checkAdminStatus(tournamentId)
    })
      
    return {
      tournament,
      isLoading,
      apiErrors,
      isAdmin,
      players,
      tournamentId,
      globalError,
      rankings,
      rankingsSorted,
      roundsData,
      playersLoading,
      rankingsLoading,
      roundsLoading,
      showEditGameModal,
      editingGame,
      editingRoundId,
      editingGameError,
      updateGameLoading,
      getTournamentStatusClass,
      getTournamentStatusText,
      getTournamentTypeText,
      getPlayerRating,
      formatGameResult,
      formatDate,
      submitGameResult,
      openEditGameModal,
      saveGameChanges,
      getGameResultClass
    }
  }
}
</script>
<style scoped>

.tournament-details-page {
  color: #000;
}

.tournament-description h3,
.tournament-description p,
.tabs-header,
.players-table th,
.players-table td,
.rankings-table th,
.rankings-table td,
.round-header h3,
.player strong,
.game-result,
.modal-header h3,
.form-group label {
  color: #000 !important;
}

.tournament-status-banner,
.game-status,
.rating,
.round-date,
.empty-state h3,
.empty-state p,
.error-state {
  
}
.tournament-details-page {
  min-height: 100vh;
  min-width: 100vw;
  background-color: #f8f9fa;
  display: flex;
  flex-direction: column;
}

.hero-section {
  background: linear-gradient(135deg, #a96fc0 0%, #ba8cce 100%);
  padding: 60px 20px;
  color: white;
  text-align: center;
  flex-shrink: 0;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 12px;
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
  flex-grow: 1;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  width: 100%;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  color: #6b5876;
}

.loading-state.mini {
  padding: 40px 0;
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

.empty-state.mini {
  padding: 40px 0;
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

/* Estilos para la tarjeta de información del torneo */
.tournament-info-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 30px;
  overflow: hidden;
  position: relative;
}

.tournament-status-banner {
  background-color: #3498db;
  color: white;
  font-weight: 600;
  padding: 10px 20px;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.tournament-status-banner.proximo {
  background-color: #f39c12;
}

.tournament-status-banner.en_curso {
  background-color: #3498db;
}

.tournament-status-banner.finalizado {
  background-color: #95a5a6;
}

.tournament-status-banner.abierto {
  background-color: #27ae60;
}

.tournament-info-content {
  padding: 30px;
}

.tournament-meta {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.meta-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
}

.meta-item svg {
  color: #9b59b6;
}

.tournament-description h3 {
  color: #333;
  font-size: 20px;
  margin-bottom: 10px;
}

.tournament-description p {
  color: #666;
  line-height: 1.6;
}

/* Estilos para las pestañas */
.tabs-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.tabs-header {
  display: flex;
  border-bottom: 1px solid #e6d5f2;
  padding: 15px 20px;
  background-color: #f8f5fb;
}

.tab-button {
  background-color: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  color: #6b5876;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  padding: 15px 25px;
  transition: all 0.3s;
}

.tab-button:hover {
  background-color: #f0e6f7;
  color: #9b59b6;
}

.tab-button.active {
  border-bottom-color: #9b59b6;
  color: #9b59b6;
}

.tabs-content {
  padding: 30px;
}

/* Estilos para la tabla de participantes */
.players-table {
  width: 100%;
  border-collapse: collapse;
}

.players-table th,
.players-table td {
  border-bottom: 1px solid #e6d5f2;
  padding: 12px 15px;
  text-align: left;
}

.players-table th {
  background-color: #f8f5fb;
  color: #6b5876;
  font-weight: 600;
}

.players-table tr:hover {
  background-color: #faf7fc;
}

/* Estilos para las rondas y partidas */
.round-card {
  background-color: #f8f5fb;
  border-radius: 8px;
  margin-bottom: 25px;
  overflow: hidden;
}

.round-header {
  background-color: #e6d5f2;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.round-header h3 {
  color: #6b5876;
  font-size: 18px;
  margin: 0;
}

.round-date {
  color: #9f7ead;
  font-size: 14px;
}

.games-list {
  padding: 15px;
}

.game-item {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 15px;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.game-players {
  display: flex;
  align-items: center;
  flex: 1;
}

.player {
  flex: 1;
}

.player.white {
  text-align: right;
  padding-right: 10px;
}

.player.black {
  text-align: left;
  padding-left: 10px;
}

.game-result {
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  padding: 0 15px;
  min-width: 60px;
  text-align: center;
}

.white-win {
  color: #2980b9;
}

.black-win {
  color: #c0392b;
}

.draw {
  color: #7f8c8d;
}

.forfeit {
  color: #95a5a6;
}

.game-status {
  font-size: 14px;
  padding: 4px 10px;
  border-radius: 4px;
  font-weight: 500;
}

.game-status.finished {
  background-color: #e8f4f8;
  color: #3498db;
}

.game-status.pending {
  background-color: #f7f6ed;
  color: #f39c12;
}

.rating {
  font-size: 14px;
  color: #95a5a6;
  margin-left: 5px;
}

/* Estilos para la clasificación */
.rankings-table {
  width: 100%;
  border-collapse: collapse;
}

.rankings-table th,
.rankings-table td {
  border-bottom: 1px solid #e6d5f2;
  padding: 12px 15px;
  text-align: center;
}

.rankings-table th {
  background-color: #f8f5fb;
  color: #6b5876;
  font-weight: 600;
}

.rankings-table td:first-child {
  font-weight: bold;
}

.rankings-table td:nth-child(2) {
  text-align: left;
}

.rankings-table tr:hover {
  background-color: #faf7fc;
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

.footer-copyright {
  width: 100%;
  margin-top: 20px;
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

/* Estilos responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 28px;
  }
  
  .hero-subtitle {
    font-size: 16px;
  }
  
  .tournament-meta {
    grid-template-columns: 1fr;
  }
  
  .game-players {
    flex-direction: column;
    gap: 10px;
    align-items: center;
  }
  
  .player.white,
  .player.black {
    text-align: center;
    padding: 0;
  }
  
  .game-item {
    flex-direction: column;
    gap: 15px;
  }
  
  .game-status {
    width: 100%;
    text-align: center;
  }
  
  .tab-button {
    padding: 12px 15px;
    font-size: 14px;
  }
  
  .tabs-content {
    padding: 20px 15px;
  }
  
  .players-table th,
  .players-table td,
  .rankings-table th,
  .rankings-table td {
    padding: 10px 8px;
    font-size: 14px;
  }
}

/* Estilos para dispositivos muy pequeños */
@media (max-width: 480px) {
  .tabs-header {
    flex-direction: column;
  }
  
  .tab-button {
    width: 100%;
    border-bottom: 1px solid #e6d5f2;
    border-left: 3px solid transparent;
  }
  
  .tab-button.active {
    border-left-color: #9b59b6;
    border-bottom-color: #e6d5f2;
  }
  
  .rankings-table,
  .players-table {
    font-size: 12px;
  }
}

/* Estilos para el modal de edición de partidas */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}

.modal-container {
  background-color: white;
  border-radius: 12px;
  width: 100%;
  max-width: 550px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #e6d5f2;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 10;
}

.modal-header h3 {
  margin: 0;
  color: #6b5876;
  font-size: 20px;
}

.close-modal {
  background: none;
  border: none;
  color: #9f7ead;
  cursor: pointer;
  padding: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.close-modal:hover {
  background-color: #f8f5fb;
  color: #8e44ad;
}

.modal-body {
  padding: 20px;
  flex-grow: 1;
  overflow-y: auto;
}

.edit-game-error {
  background-color: #fdeaea;
  border-left: 4px solid #e74c3c;
  color: #c0392b;
  padding: 12px 15px;
  margin-bottom: 20px;
  border-radius: 4px;
  font-size: 14px;
}

.edit-game-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: #6b5876;
  font-size: 14px;
}

.player-info {
  background-color: #f8f5fb;
  padding: 12px 15px;
  border-radius: 6px;
  border: 1px solid #e6d5f2;
}

.form-control {
  background-color: #f8f5fb;
  border: 1px solid #e6d5f2;
  border-radius: 6px;
  color: #6b5876;
  font-size: 16px;
  padding: 12px 15px;
  transition: border-color 0.2s;
  width: 100%;
}

.form-control:focus {
  border-color: #9b59b6;
  outline: none;
}

.textarea {
  min-height: 100px;
  resize: vertical;
}

.toggle-switch {
  position: relative;
  display: inline-block;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-switch label {
  position: relative;
  display: inline-block;
  padding-left: 50px;
  cursor: pointer;
  font-weight: 400;
  line-height: 24px;
}

.toggle-switch label::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 40px;
  height: 24px;
  background-color: #e6d5f2;
  border-radius: 12px;
  transition: background-color 0.3s;
}

.toggle-switch label::after {
  content: '';
  position: absolute;
  left: 4px;
  top: 4px;
  width: 16px;
  height: 16px;
  background-color: white;
  border-radius: 50%;
  transition: transform 0.3s;
}

.toggle-switch input:checked + label::before {
  background-color: #9b59b6;
}

.toggle-switch input:checked + label::after {
  transform: translateX(16px);
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #e6d5f2;
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  position: sticky;
  bottom: 0;
  background-color: white;
  z-index: 10;
}

.btn {
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  padding: 12px 24px;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn:active {
  transform: translateY(1px);
}

.btn-cancel {
  background-color: #f8f5fb;
  color: #9f7ead;
}

.btn-cancel:hover {
  background-color: #e6d5f2;
}

.btn-save {
  background-color: #9b59b6;
  color: white;
}

.btn-save:hover {
  background-color: #8e44ad;
}

.btn-save:disabled {
  background-color: #d2b4e5;
  cursor: not-allowed;
}

.mini-spinner {
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top: 2px solid white;
  width: 16px;
  height: 16px;
  animation: spin 1s linear infinite;
}

/* Estilos responsive para el modal */
@media (max-width: 600px) {
  .modal-container {
    max-width: 100%;
    height: 100%;
    max-height: 100%;
    border-radius: 0;
  }
  
  .modal-overlay {
    padding: 0;
  }
  
  .form-group {
    gap: 6px;
  }
  
  .form-control {
    padding: 10px 12px;
    font-size: 14px;
  }
  
  .btn {
    padding: 10px 20px;
    font-size: 14px;
  }
}

/* Estilos para la edición adicional de acciones en la lista de juegos */
.game-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.edit-game-btn {
  background-color: #f7f6ed;
  border: none;
  color: #9b59b6;
  font-size: 14px;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: background-color 0.2s;
}

.edit-game-btn:hover {
  background-color: #e6d5f2;
}

.edit-game-btn svg {
  color: #9b59b6;
}

.custom-select {
  appearance: none;
  background-color: #f8f5fb;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%239b59b6' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
  border: 1px solid #e6d5f2;
  border-radius: 6px;
  color: #6b5876;
  font-size: 15px;
  padding: 10px 36px 10px 15px;
  width: 100%;
  transition: border-color 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.custom-select:hover {
  border-color: #d2b4e5;
}

.custom-select:focus {
  border-color: #9b59b6;
  outline: none;
  box-shadow: 0 0 0 3px rgba(155, 89, 182, 0.15);
}

.custom-select:disabled {
  background-color: #f0e6f7;
  border-color: #e6d5f2;
  color: #9f7ead;
  opacity: 0.7;
  cursor: not-allowed;
}

/* Para pantallas más pequeñas */
@media (max-width: 768px) {
  .custom-select {
    font-size: 14px;
    padding: 8px 32px 8px 12px;
    background-position: right 10px center;
  }
}
 

</style>
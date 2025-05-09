<template>
  <div class="tournament-details-page">
    <HeaderComponent />

    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title" data-cy="tournament-title">
          {{ tournament ? tournament.name : "Cargando torneo..." }}
        </h1>
        <p class="hero-subtitle" v-if="tournament">
          {{ getTournamentTypeText(tournament.tournament_type) }} |
          {{ tournament.board_type === "OTB" ? "Presencial" : "Online" }} |
          {{ tournament.timeControl || "Tiempo no especificado" }}
        </p>
      </div>
    </div>

    <div class="main-content">
      <div class="container">
        <!-- Estado de error -->
        <div v-if="apiErrors" class="error-state">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
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
            <div
              class="tournament-status-banner"
              :class="getTournamentStatusClass(tournament)"
            >
              {{ getTournamentStatusText(tournament) }}
            </div>

            <div class="tournament-info-content">
              <div class="tournament-meta">
                <div class="meta-item">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <rect
                      x="3"
                      y="4"
                      width="18"
                      height="18"
                      rx="2"
                      ry="2"
                    ></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                  <div>
                    <strong>Fechas:</strong>
                    <div>
                      {{ formatDate(tournament.start_date) }} -
                      {{
                        tournament.end_date
                          ? formatDate(tournament.end_date)
                          : "En curso"
                      }}
                    </div>
                  </div>
                </div>

                <div class="meta-item">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                  </svg>
                  <div>
                    <strong>Participantes:</strong>
                    <div>
                      {{ tournament.players ? tournament.players.length : 0 }}
                      jugadores
                    </div>
                  </div>
                </div>

                <div class="meta-item">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                  </svg>
                  <div>
                    <strong>Control de tiempo:</strong>
                    <div>{{ tournament.timeControl || "No especificado" }}</div>
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
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="32"
                  height="32"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
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
                      <td>{{ player.name || "N/A" }}</td>
                      <td>{{ player.lichess_username || "N/A" }}</td>
                      <td>{{ getPlayerRating(player) || "N/A" }}</td>
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

              <div
                v-else-if="!roundsData || roundsData.rounds.length === 0"
                class="empty-state mini"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="32"
                  height="32"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <h3>No hay rondas configuradas</h3>
                <p>
                  El torneo aún no ha sido emparejado o está en preparación.
                </p>
              </div>

              <div v-else class="rounds-list">
                <div
                  v-for="(round, roundIndex) in roundsData.rounds.rounds"
                  :key="round.round_id"
                  class="round-card"
                  :data-cy="`round_${roundIndex + 1}`"
                >
                  <div class="round-header">
                    <h3>{{ "round_00" + (roundIndex + 1) }}</h3>
                    <div class="round-date" v-if="round.start_date">
                      {{ formatDate(round.start_date) }}
                    </div>
                  </div>

                  <div class="games-list">
                    <div
                      v-for="(game, gameIndex) in round.games"
                      :key="game.game_id"
                      class="game-item"
                      :data-cy="`game_${roundIndex + 1}_${
                        round.games.length - gameIndex
                      }`"
                    >
                      <div class="game-players">
                        <div class="player white">
                          <strong>{{
                            game.white.name || "Sin jugador"
                          }}</strong>
                          <span v-if="game.white.rating" class="rating"
                            >({{ game.white.rating }})</span
                          >
                        </div>
                        <div class="game-result">
                          <!-- Para administradores - visible solo para administradores -->
                          <div v-if="isAdmin">
                            <select
                              v-model="game.result"
                              class="custom-select"
                              :data-cy="`select-admin-${round.round_id}-${
                                round.games.length - gameIndex
                              }`"
                            >
                              <option value="">-- Seleccionar --</option>
                              <option value="White wins (1-0)">
                                White wins (1-0)
                              </option>
                              <option value="B">Black wins (0-1)</option>
                              <option value="D">Draw (1/2-1/2)</option>
                              <option value="F">Forfeit (F-F)</option>
                            </select>

                            <span
                              class="result-display"
                              :data-cy="`input-${round.round_id}-${
                                round.games.length - gameIndex
                              }`"
                              readonly
                            >
                              {{ formatGameResult(game.result) }}
                            </span>
                          </div>

                          <!-- Para usuarios normales -->
                          <div v-else>
                            <!-- Si es OTB, mostrar el selector -->
                            <div v-if="tournament.board_type === 'OTB'">
                              <select
                                v-if="tournament.board_type === 'OTB'"
                                v-model="game.result"
                                class="custom-select"
                                :data-cy="`select-${round.round_id}-${
                                  round.games.length - gameIndex
                                }`"
                              >
                                <option value="">-- Seleccionar --</option>
                                <option value="White wins (1-0)">
                                  White wins (1-0)
                                </option>
                                <option value="B">Black wins (0-1)</option>
                                <option value="D">Draw (1/2-1/2)</option>
                                <option value="F">Forfeit (F-F)</option>
                              </select>

                              <span
                                v-if="tournament.board_type === 'OTB'"
                                class="result-display"
                                :data-cy="`input-${round.round_id}-${
                                  round.games.length - gameIndex
                                }`"
                                readonly
                              >
                                {{ formatGameResult(game.result) }}
                              </span>
                            </div>

                            <!-- Si es Online (Lichess), mostrar input para ID de juego -->
                            <div v-else class="lichess-game-input">
                              <input
                                v-if="
                                  tournament.board_type === 'LIC' &&
                                  !game.finished
                                "
                                v-model="game.result"
                                class="custom-select"
                                :data-cy="`input-${round.round_id}-${
                                  round.games.length - gameIndex
                                }`"
                                placeholder="ID de juego"
                                :value="'{{ formatGameResult(game.result) }}'"
                              />
                              <span
                                v-if="
                                  tournament.board_type === 'LIC' &&
                                  game.finished
                                "
                                class="custom-select"
                                :data-cy="`input-${round.round_id}-${
                                  round.games.length - gameIndex
                                }`"
                              >
                                {{ formatGameResult(game.result) }}
                              </span>

                              <span
                                v-if="tournament.board_type === 'LIC'"
                                class="result-display"
                                readonly
                              >
                                {{ formatGameResult(game.result) }}
                              </span>
                            </div>
                          </div>
                        </div>

                        <div class="player black">
                          <strong>{{
                            game.black.name || "Sin jugador"
                          }}</strong>
                          <span v-if="game.black.rating" class="rating"
                            >({{ game.black.rating }})</span
                          >
                        </div>
                      </div>

                      <div class="game-actions">
                        <div
                          class="game-status"
                          :class="game.finished ? 'finished' : 'pending'"
                        >
                          {{ game.finished ? "Finalizada" : "Pendiente" }}
                        </div>

                        <!-- Botón para usuarios normales con OTB o lichess verificado -->
                        <button
                          v-if="!isAdmin && tournament.board_type === 'LIC'"
                          class="edit-game-btn"
                          :data-cy="`button-${round.round_id}-${
                            round.games.length - gameIndex
                          }`"
                          @click="submitGameResultLic(round.round_id, game)"
                        >
                          Enviar resultado
                        </button>

                        <button
                          v-if="!isAdmin && tournament.board_type === 'OTB'"
                          class="edit-game-btn"
                          :data-cy="`button-${round.round_id}-${
                            round.games.length - gameIndex
                          }`"
                          @click="submitGameResultOtb(round.round_id, game)"
                        >
                          Enviar resultado
                        </button>

                        <!-- Botón para administradores -->
                        <button
                          v-if="isAdmin"
                          class="edit-game-btn"
                          :data-cy="`button-admin-${round.round_id}-${
                            round.games.length - gameIndex
                          }`"
                          @click="submitGameResultOtb(round.round_id, game)"
                        >
                          Enviar resultado
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Agrega un elemento para mensajes de error globales -->
              <div
                v-if="globalError"
                class="error-state"
                data-cy="error-message"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="48"
                  height="48"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
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
              <h2 class="tabs-header" data-cy="standing-accordion-button">
                Clasificación
              </h2>

              <div v-if="rankingsLoading" class="loading-state mini">
                <div class="spinner"></div>
                <p>Cargando clasificación...</p>
              </div>

              <div
                v-else-if="!rankings || Object.keys(rankings).length === 0"
                class="empty-state mini"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="32"
                  height="32"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <h3>No hay clasificación disponible</h3>
                <p>
                  La clasificación estará disponible cuando se hayan jugado
                  partidas.
                </p>
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
                    <tr
                      v-for="(player, index) in rankingsSorted"
                      :key="player.id"
                      :data-cy="`ranking-${index + 1}`"
                    >
                      <td data-cy="name">{{ player.name }}&nbsp;</td>
                      <td data-cy="points">
                        {{ player.score.toFixed(2) }}&nbsp;
                      </td>
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
import { useAuthStore } from "@/stores/auth";
import axios from "axios";
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import HeaderComponent from "./Header.vue";

export default {
  name: "TournamentDetails",
  components: {
    HeaderComponent,
  },
  setup() {
    const route = useRoute();
    const tournamentId = computed(() => route.params.id);
    const authStore = useAuthStore(); // store de autenticación

    // Estado
    const isLoading = ref(true);
    const apiErrors = ref(null);
    const tournament = ref(null);
    const players = ref([]);
    const rankings = ref({});
    const roundsData = ref(null);
    const playersLoading = ref(false);
    const rankingsLoading = ref(false);
    const roundsLoading = ref(false);

    // Estado para la edición de partidas
    const showEditGameModal = ref(false);
    const editingGame = ref(null);
    const editingRoundId = ref(null);
    const editingGameError = ref(null);
    const updateGameLoading = ref(false);

    // Añade una nueva variable de estado para errores globales
    const globalError = ref(null);

    const isAdmin = ref(false);

    // Función para verificar si el usuario actual es administrador
    const checkAdminStatus = async (tournamentId) => {
      try {
        isAdmin.value = false;
        const response = await axios.get(`/tournaments/${tournamentId.value}/`);
        tournament.value = response.data;
        alert(`Tournament ID: ${tournamentId.value}`);

        if (tournament.value && tournament.value.administrativeUser) {
          const currentUserId = getCurrentUserId();
          isAdmin.value = currentUserId === tournament.value.administrativeUser;
          alert(
            `Estado de administrador: ${isAdmin.value} (Usuario: ${currentUserId}, Admin: ${tournament.value.administrativeUser})`
          );
          console.log(
            `Estado de administrador: ${isAdmin.value} (Usuario: ${currentUserId}, Admin: ${tournament.value.administrativeUser})`
          );
        } else {
          isAdmin.value = false;
        }
      } catch (error) {
        console.error("Error al verificar estado de administrador:", error);
        isAdmin.value = false;
      }
    };

    const getCurrentUserId = () => {
      const user = authStore.getUser;
      return user ? user.id : null;
    };

    const loadTournament = async () => {
      isLoading.value = true;
      apiErrors.value = null;
      globalError.value = null;

      try {
        const response = await axios.get(`/tournaments/${tournamentId.value}/`);
        tournament.value = response.data;

        console.log("Torneo cargado:", tournament.value);

        // Cargar todos los datos necesarios
        await loadPlayers();
        await loadRankings();
        await loadRounds();
      } catch (error) {
        console.error("Error al cargar torneo:", error);
        apiErrors.value =
          "Error al cargar los datos del torneo. Por favor, inténtalo de nuevo más tarde.";

        // Comprobar si es un error de "Tournament name already exists"
        if (error.response && error.response.data) {
          if (
            error.response.data.detail &&
            error.response.data.detail.includes("already exists")
          ) {
            globalError.value = "Error: Tournament name already exists";
          }
        }
      } finally {
        isLoading.value = false;
      }
    };

    // Modifica la función loadPlayers para manejar errores específicos
    const loadPlayers = async () => {
      playersLoading.value = true;

      try {
        const response = await axios.get(`/get_players/${tournamentId.value}/`);
        players.value = response.data;
        console.log("Jugadores cargados:", players.value);
      } catch (error) {
        console.error("Error al cargar jugadores:", error);
        apiErrors.value = "Error al cargar los participantes.";

        // Comprobar si es un error de "can not add players"
        if (error.response && error.response.data) {
          if (
            error.response.data.detail &&
            error.response.data.detail.includes("can not add players")
          ) {
            globalError.value = "Error: can not add players to tournament";
          }
        }
      } finally {
        playersLoading.value = false;
      }
    };

    // Cargar datos de clasificación
    const loadRankings = async () => {
      rankingsLoading.value = true;

      try {
        const response = await axios.get(`/get_ranking/${tournamentId.value}/`);
        rankings.value = response.data;

        console.log("Clasificación cargada:", rankings.value);
      } catch (error) {
        console.error("Error al cargar clasificación:", error);
        apiErrors.value = "Error al cargar la clasificación.";
      } finally {
        rankingsLoading.value = false;
      }
    };

    // Cargar datos de rondas
    const loadRounds = async () => {
      roundsLoading.value = true;

      try {
        const response = await axios.get(
          `/get_round_results/${tournamentId.value}/`
        );
        roundsData.value = response.data;
        alert("Rondas cargadas:", roundsData.value);
      } catch (error) {
        console.error("Error al cargar rondas:", error);
        apiErrors.value = "Error al cargar las rondas y partidas.";
      } finally {
        roundsLoading.value = false;
      }
    };

    const submitGameResultLic = async (roundId, game) => {
      alert("entra aqui");

      alert(game.result);

      try {
        alert("entra");

        alert(`ID DEL JUEGO: ${game.game_id}`);

        const response = await axios.get(`/lichess_game_result/`, {
          params: {
            game_id: game.game_id,
            lichess_id: game.result,
          },
        });

        const gameData = {
          game_id: game.game_id,
          result: response.data.result,
          finished: true,
        };

        alert("Enviando datos de juego:", gameData);

        const authStore = useAuthStore();
        const token = authStore.getToken;

        const headers = {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        };

        if (!isAdmin.value) {
          const response = await axios.post(`/update_game/`, gameData);
          alert("Resultado enviado correctamente:", response.data);
        } else {
          const response = await axios.post(`/admin_update_game/`, gameData, {
            headers,
          });
          console.log(
            "Resultado enviado correctamente (admin):",
            response.data
          );
        }

        await loadRankings();
        game.result = formatGameResult(response.data.result);

        alert(game.result);

        alert(
          isAdmin.value
            ? "Resultado actualizado correctamente (como administrador)."
            : "Resultado enviado correctamente."
        );

        game.finished = true;
      } catch (error) {
        alert("Error al enviar el resultado:", error);

        let errorMessage =
          "Error al enviar el resultado. Por favor, inténtalo de nuevo.";
        if (error.response) {
          console.log("Error response:", error.response);
          if (error.response.data) {
            if (error.response.data.message) {
              errorMessage = `Error: ${error.response.data.message}`;
            } else if (error.response.data.detail) {
              errorMessage = `Error: ${error.response.data.detail}`;
            }
          }
        }
        alert(errorMessage);
        globalError.value = errorMessage;
      }
    };

    const formatGameResult = (result) => {
      if (!result) return "";

      switch (result) {
        case "W":
          return "1-0";
        case "White wins (1-0)":
          return "1-0";
        case "B":
          return "0-1";
        case "D":
          return "½-½";
        case "F":
          return "F-F";
        default:
          return result;
      }
    };

    // Función para enviar el resultado de una partida
    const submitGameResultOtb = async (roundId, game) => {
      try {
        // Si no hay resultado seleccionado, no enviar
        if (!game.result) {
          alert("Por favor, selecciona un resultado antes de enviar.");
          return;
        }

        let resultCode = game.result;
        if (game.result === "White wins (1-0)") {
          resultCode = "W";
        }

        // Preparar datos para enviar - asegurarse de que el formato es correcto
        const gameData = {
          game_id: game.game_id,
          result: resultCode, // Ya no convertir, usar directamente lo seleccionado
          finished: true, // Siempre marcar como finalizado al enviar un resultado
        };

        console.log("Enviando datos de juego:", gameData);

        // SOLUCIÓN: Obtener el token de autenticación desde el store
        const authStore = useAuthStore();
        const token = authStore.getToken;

        // Preparar headers con el token
        const headers = {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        };

        if (!isAdmin.value) {
          // Si no es admin, solicitar correo para verificación
          const userEmail = window.prompt(
            "Por favor, ingresa tu correo electrónico para confirmar:"
          );
          if (!userEmail) {
            return; // Si el usuario cancela, no continuar
          }
          // Añadir el email a los datos enviados
          gameData.email = userEmail;
          // Enviar resultado a la API para usuarios normales
          const response = await axios.post(`/update_game/`, gameData);
          console.log("Resultado enviado correctamente:", response.data);
        } else {
          // Enviar resultado a la API para administradores
          // SOLUCIÓN: Añadir headers con el token en la solicitud
          const response = await axios.post(`/admin_update_game/`, gameData, {
            headers,
          });
          console.log(
            "Resultado enviado correctamente (admin):",
            response.data
          );
        }

        await loadRankings();
        // Mensaje de éxito
        alert(
          isAdmin.value
            ? "Resultado actualizado correctamente (como administrador)."
            : "Resultado enviado correctamente."
        );
        game.finished = true;
      } catch (error) {
        console.error("Error al enviar el resultado:", error);
        // Mostrar mensaje de error con detalles específicos si están disponibles
        let errorMessage =
          "Error al enviar el resultado. Por favor, inténtalo de nuevo.";
        if (error.response) {
          console.log("Error response:", error.response);
          if (error.response.data) {
            if (error.response.data.message) {
              errorMessage = `Error: ${error.response.data.message}`;
            } else if (error.response.data.detail) {
              errorMessage = `Error: ${error.response.data.detail}`;
            }
          }
        }
        alert(errorMessage);
        globalError.value = errorMessage;
      }
    };

    // Guardar los cambios de la partida
    const saveGameChanges = async () => {
      updateGameLoading.value = true;
      editingGameError.value = null;

      try {
        // Si el resultado está establecido pero finished es false, actualizar finished a true
        if (editingGame.value.result && !editingGame.value.finished) {
          editingGame.value.finished = true;
        }

        // Convertir el resultado al formato correcto para la API
        let resultCode = editingGame.value.result;
        if (editingGame.value.result === "White wins (1-0)") {
          resultCode = "W";
        }

        // Enviar los datos actualizados a la API
        const response = await axios.post(`/admin_update_game/`, {
          game_id: editingGame.value.game_id,
          result: resultCode,
          finished: editingGame.value.finished,
        });
        console.log("Partida actualizada correctamente:", response.data);

        // Actualizar la partida en la lista local
        if (roundsData.value && roundsData.value.rounds) {
          const roundIndex = roundsData.value.rounds.rounds.findIndex(
            (r) => r.round_id === editingRoundId.value
          );

          if (roundIndex !== -1) {
            const gameIndex = roundsData.value.rounds.rounds[
              roundIndex
            ].games.findIndex((g) => g.game_id === editingGame.value.game_id);

            if (gameIndex !== -1) {
              roundsData.value.rounds.rounds[roundIndex].games[gameIndex] = {
                ...editingGame.value,
              };
            }
          }
        }

        // Actualizar la clasificación si hay cambios en los resultados
        loadRankings();

        // Cerrar el modal
        showEditGameModal.value = false;
      } catch (error) {
        console.error("Error al actualizar la partida:", error);

        if (error.response && error.response.data) {
          editingGameError.value =
            error.response.data.detail ||
            "Error al guardar los cambios. Inténtalo de nuevo.";
        } else {
          editingGameError.value =
            "Error de conexión. Por favor, verifica tu conexión a internet e inténtalo de nuevo.";
        }
      } finally {
        updateGameLoading.value = false;
      }
    };

    // Abrir el modal para editar una partida
    const openEditGameModal = (roundId, game) => {
      // Crear una copia profunda del objeto para no modificar directamente el original
      editingGame.value = JSON.parse(JSON.stringify(game));
      editingGame.value.id = game.game_id; // Asegurarse de que el ID de la partida esté presente
      editingRoundId.value = roundId;
      editingGameError.value = null;
      showEditGameModal.value = true;
    };

    // Formateador de fechas
    const formatDate = (dateString) => {
      if (!dateString) return "Fecha no disponible";

      try {
        const options = { day: "2-digit", month: "2-digit", year: "numeric" };
        return new Date(dateString).toLocaleDateString("es-ES", options);
      } catch (error) {
        console.error("Error al formatear fecha:", dateString, error);
        return "Fecha inválida";
      }
    };

    // Determinar el estado del torneo
    const getTournamentStatusClass = (tournament) => {
      if (!tournament.start_date) return "proximo";

      const now = new Date();
      const startDate = new Date(tournament.start_date);
      const endDate = tournament.end_date
        ? new Date(tournament.end_date)
        : null;

      if (now < startDate) return "proximo";
      if (endDate && now > endDate) return "finalizado";
      return "en_curso";
    };

    // Obtener texto de estado para mostrar
    const getTournamentStatusText = (tournament) => {
      const status = getTournamentStatusClass(tournament);

      const statusMap = {
        proximo: "Próximo",
        en_curso: "En curso",
        finalizado: "Finalizado",
        abierto: "Inscripción abierta",
      };

      return statusMap[status] || "Estado desconocido";
    };

    // Obtener el texto del tipo de torneo
    const getTournamentTypeText = (type) => {
      const typeMap = {
        SW: "Suizo",
        RR: "Round Robin",
        KO: "Eliminación",
        TE: "Por equipos",
        SR: "Round Robin", // Añadido para ser compatible con el test
      };

      return typeMap[type] || "Ajedrez";
    };

    // Obtener el rating del jugador según el tipo de torneo
    const getPlayerRating = (player) => {
      if (!tournament.value || !player) return null;

      switch (tournament.value.tournament_speed) {
        case "BL":
          return player.fide_rating_blitz || player.lichess_rating_blitz;
        case "RA":
          return player.fide_rating_rapid || player.lichess_rating_rapid;
        default: // 'CL' - Classical
          return (
            player.fide_rating_classical || player.lichess_rating_classical
          );
      }
    };

    // Obtener la clase CSS según el resultado
    const getGameResultClass = (result) => {
      return (
        {
          "White wins (1-0)": "white-win",
          B: "black-win",
          D: "draw",
          F: "forfeit",
        }[result] || ""
      );
    };

    // Ordenar rankings por posición
    const rankingsSorted = computed(() => {
      return Object.values(rankings.value)
        .sort((a, b) => a.rank - b.rank)
        .map((player) => ({
          ...player,
          rank: player.rank,
          score: parseFloat(player.score.toFixed(2)),
          BT: parseFloat(player.BT.toFixed(2) || 0),
          WI: parseFloat(player.WI.toFixed(2) || 0),
        }));
    });

    onMounted(() => {
      checkAdminStatus(tournamentId);
      loadTournament();
    });

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
      submitGameResultLic,
      submitGameResultOtb,
      openEditGameModal,
      saveGameChanges,
      getGameResultClass,
    };
  },
};
</script>
<style scoped>
@import '@/assets/tournament_details.css';
</style>

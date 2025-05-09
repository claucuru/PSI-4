<template>
  <div class="confirmation-container">
    <div class="confirmation-background">
      <!-- Parte izquierda con imagen de fondo -->
      <div class="chess-tournament-bg">
        <div class="chess-tournament-content">
          <h1 class="confirmation-brand">¡Torneo Creado!</h1>
          <p class="confirmation-tagline">
            Tu competencia de ajedrez está lista
          </p>
        </div>
      </div>

      <!-- Parte derecha con los detalles del torneo -->
      <div class="tournament-details">
        <div v-if="loading" class="loading-indicator">
          <p>Cargando detalles del torneo...</p>
        </div>
        <div v-else-if="error" class="error-message">
          <p>{{ error }}</p>
          <button class="secondary-btn" @click="goHome">
            Volver al inicio
          </button>
        </div>
        <div v-else>
          <div class="success-header">
            <div class="success-icon">✓</div>
            <h2 class="details-title">Torneo creado exitosamente</h2>
          </div>

          <div class="details-card">
            <div class="card-header">
              <h3 class="tournament-name">{{ tournament.name }}</h3>
              <p class="tournament-date">
                Fecha de inicio: {{ formatDate(tournament.start_date) }}
              </p>
            </div>

            <div class="details-section">
              <h4 class="section-title">Configuración General</h4>
              <div class="details-grid">
                <div class="detail-item">
                  <span class="detail-label">Sistema de emparejamiento</span>
                  <span class="detail-value">{{
                    getPairingSystemName(tournament.tournament_type)
                  }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">Tipo de tablero</span>
                  <span class="detail-value">{{
                    getBoardTypeName(tournament.board_type)
                  }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">Velocidad del torneo</span>
                  <span class="detail-value">{{
                    getSpeedName(tournament.tournament_speed)
                  }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">Administración</span>
                  <span class="detail-value">{{
                    tournament.onlyAdminCanUpdate
                      ? "Solo administrador"
                      : "Todos pueden actualizar"
                  }}</span>
                </div>
              </div>
            </div>

            <div class="details-section">
              <h4 class="section-title">Puntuación</h4>
              <div class="points-grid">
                <div class="point-item">
                  <div class="point-circle win">
                    {{ tournament.win_points }}
                  </div>
                  <span class="point-label">Victoria</span>
                </div>
                <div class="point-item">
                  <div class="point-circle draw">
                    {{ tournament.draw_points }}
                  </div>
                  <span class="point-label">Empate</span>
                </div>
                <div class="point-item">
                  <div class="point-circle lose">
                    {{ tournament.lose_points }}
                  </div>
                  <span class="point-label">Derrota</span>
                </div>
              </div>
            </div>

            <div class="details-section">
              <h4 class="section-title">Métodos de ranking</h4>
              <div class="ranking-methods">
                <div
                  class="method-chip"
                  v-for="(method, index) in displayRankingMethods"
                  :key="index"
                >
                  {{ getRankingMethodName(method) }}
                </div>
              </div>
            </div>

            <div class="details-section">
              <h4 class="section-title">
                Jugadores ({{ tournamentPlayers.length }})
              </h4>
              <div class="players-list">
                <div
                  class="player-item"
                  v-for="(player, index) in tournamentPlayers"
                  :key="index"
                >
                  <div class="player-avatar">
                    {{ getPlayerInitials(player) }}
                  </div>
                  <span class="player-name">{{
                    player.name || player.lichess_username
                  }}</span>
                </div>
              </div>
            </div>

            <div class="action-buttons">
              <button class="secondary-btn" @click="goHome">
                Volver al inicio
              </button>
              <button class="primary-btn" @click="goToTournament">
                Ir al torneo
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"; // Asegúrate de importar axios o tu cliente HTTP preferido
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

export default {
  name: "TournamentConfirmation",
  setup() {
    const tournament = ref({
      id: null,
      name: "",
      tournament_type: "",
      board_type: "",
      tournament_speed: "",
      onlyAdminCanUpdate: true,
      win_points: 0,
      draw_points: 0,
      lose_points: 0,
      start_date: "",
      ranking_methods: [],
    });
    const tournamentPlayers = ref([]);
    const rankingMethods = computed(() => {
      if (
        tournament.value.rankingList &&
        Array.isArray(tournament.value.rankingList)
      ) {
        return tournament.value.rankingList;
      } else if (
        tournament.value.ranking_methods &&
        Array.isArray(tournament.value.ranking_methods)
      ) {
        return tournament.value.ranking_methods.map((m) => m.value || m);
      } else if (
        tournament.value.ranking_methods &&
        typeof tournament.value.ranking_methods === "string"
      ) {
        // Si ranking_methods es un string, separamos por comas o lo convertimos en array
        return tournament.value.ranking_methods.split(",").map((m) => m.trim());
      }
      return [];
    });

    // Métodos de ranking para mostrar en pantalla (asegura que siempre haya algo)
    const displayRankingMethods = computed(() => {
      if (rankingMethods.value && rankingMethods.value.length > 0) {
        return rankingMethods.value;
      }
      // Valores por defecto si no hay métodos definidos
      return ["BU", "BC", "SB"];
    });

    const loading = ref(true);
    const error = ref(null);
    const route = useRoute();
    const router = useRouter();

    onMounted(async () => {
      // Obtenemos el ID del torneo de los parámetros de la ruta
      const tournamentId = route.params.id;

      // Si tenemos datos de torneo en los params de la ruta, los usamos
      if (route.params.tournament) {
        tournament.value = route.params.tournament;
        await fetchTournamentPlayers(tournamentId);
        loading.value = false;
        return;
      }

      // Si no hay datos en los params, cargamos los datos del torneo desde la API
      try {
        await fetchTournamentDetails(tournamentId);
        await fetchTournamentPlayers(tournamentId);
        loading.value = false;
      } catch (err) {
        console.error("Error al cargar los datos del torneo:", err);
        error.value =
          "No se pudieron cargar los detalles del torneo. Por favor, inténtalo de nuevo.";
        loading.value = false;
      }
    });

    const fetchTournamentDetails = async (tournamentId) => {
      try {
        const response = await axios.get(`/tournaments/${tournamentId}/`);
        tournament.value = response.data;
        console.log("Torneo cargado:", tournament.value); // Depuración
      } catch (error) {
        console.error("Error fetching tournament details:", error);
        throw new Error("No se pudo obtener la información del torneo");
      }
    };

    const fetchTournamentPlayers = async (tournamentId) => {
      try {
        const response = await axios.get(`/get_players/${tournamentId}/`);
        tournamentPlayers.value = response.data;
      } catch (error) {
        console.error("Error fetching tournament players:", error);
        throw new Error("No se pudo obtener la lista de jugadores");
      }
    };

    const formatDate = (dateString) => {
      if (!dateString) return "";

      const date = new Date(dateString);
      return date.toLocaleDateString("es-ES", {
        day: "2-digit",
        month: "long",
        year: "numeric",
      });
    };

    const getPairingSystemName = (code) => {
      if (!code) return "No especificado";

      const systems = {
        SW: "Sistema Suizo",
        SR: "Round Robin Simple",
        DR: "Round Robin Doble",
        DD: "Round Robin Doble (mismo día)",
      };
      return systems[code] || code;
    };

    const getBoardTypeName = (code) => {
      if (!code) return "No especificado";

      const types = {
        LIC: "Lichess (Online)",
        OTB: "Presencial (OTB)",
      };
      return types[code] || code;
    };

    const getSpeedName = (code) => {
      if (!code) return "No especificado";

      const speeds = {
        CL: "Clásico",
        RA: "Rápido",
        BL: "Blitz",
        BU: "Bullet",
      };
      return speeds[code] || code;
    };

    const getRankingMethodName = (code) => {
      if (!code) return "No especificado";

      const methods = {
        BU: "Buchholz",
        BC: "Buchholz cut 1",
        BA: "Buchholz average",
        SB: "Sonneborn-Berger",
        PS: "Plain Score",
        WI: "Victorias",
        BT: "Juegos con negras",
      };
      return methods[code] || code;
    };

    const getPlayerInitials = (player) => {
      if (player.name && player.name.length > 0) {
        return player.name.charAt(0).toUpperCase();
      }
      if (player.lichess_username && player.lichess_username.length > 0) {
        return player.lichess_username.charAt(0).toUpperCase();
      }
      return "?";
    };

    const goHome = () => {
      router.push("/");
    };

    const goToTournament = () => {
      router.push(`/tournamentdetail/${tournament.value.id}`);
    };

    return {
      tournament,
      tournamentPlayers,
      rankingMethods,
      displayRankingMethods,
      loading,
      error,
      formatDate,
      getPairingSystemName,
      getBoardTypeName,
      getSpeedName,
      getRankingMethodName,
      getPlayerInitials,
      goHome,
      goToTournament,
    };
  },
};
</script>

<style scoped>
@import '@/assets/tournament_config.css';
</style>

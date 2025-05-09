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
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios"; // Asegúrate de importar axios o tu cliente HTTP preferido

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
/* Los estilos permanecen iguales */
.confirmation-container {
  min-height: 100vh;
  min-width: 100vw;
  background-color: #f8f9fa;
}

.confirmation-background {
  display: flex;
  min-height: 100vh;
}

/* Sección izquierda con imagen de fondo */
.chess-tournament-bg {
  width: 40%;
  background-image: url("../components/icons/chess.jpg");
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

/* Capa oscura para mejorar legibilidad del texto */
.chess-tournament-bg::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
}

.chess-tournament-content {
  text-align: center;
  max-width: 600px;
  padding: 20px;
  position: relative;
  z-index: 1;
  color: white;
}

.confirmation-brand {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 16px;
  color: white;
}

.confirmation-tagline {
  font-size: 18px;
  opacity: 0.9;
  line-height: 1.5;
  color: white;
}

/* Loading y error */
.loading-indicator,
.error-message {
  text-align: center;
  padding: 40px;
  color: #d88ca0;
}

.error-message button {
  margin-top: 20px;
}

/* Sección de detalles del torneo */
.tournament-details {
  width: 60%;
  padding: 40px;
  background-color: white;
  overflow-y: auto;
}

.success-header {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 30px;
}

.success-icon {
  background-color: #e091a9;
  color: white;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 15px;
}

.details-title {
  color: #333;
  font-size: 28px;
  font-weight: 700;
}

.details-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 30px;
  margin-bottom: 30px;
}

.card-header {
  border-bottom: 2px solid #f0d4dc;
  padding-bottom: 20px;
  margin-bottom: 25px;
}

.tournament-name {
  color: #d88ca0;
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
}

.tournament-date {
  color: #999;
  font-size: 14px;
}

.details-section {
  margin-bottom: 30px;
}

.section-title {
  color: #e091a9;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
  border-left: 4px solid #e091a9;
  padding-left: 10px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.detail-item {
  background-color: #fcf7f8;
  padding: 15px;
  border-radius: 8px;
}

.detail-label {
  display: block;
  color: #d88ca0;
  font-size: 14px;
  margin-bottom: 5px;
}

.detail-value {
  display: block;
  color: #333;
  font-size: 16px;
  font-weight: 500;
}

/* Puntuación */
.points-grid {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}

.point-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.point-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 10px;
}

.win {
  background-color: #e091a9;
}

.draw {
  background-color: #d9a6b3;
}

.lose {
  background-color: #e9c5ce;
}

.point-label {
  color: #d88ca0;
  font-size: 14px;
}

/* Métodos de ranking */
.ranking-methods {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.method-chip {
  background-color: #fcf7f8;
  color: #d88ca0;
  padding: 8px 15px;
  border-radius: 20px;
  font-size: 14px;
  display: inline-block;
  border: 1px solid #f0d4dc;
}

/* Lista de jugadores */
.players-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 15px;
  max-height: 200px;
  overflow-y: auto;
  padding: 5px;
}

.player-item {
  display: flex;
  align-items: center;
  background-color: #fcf7f8;
  padding: 10px;
  border-radius: 8px;
}

.player-avatar {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  background-color: #e091a9;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-right: 10px;
}

.player-name {
  font-size: 14px;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Botones de acción */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #f0d4dc;
}

.secondary-btn {
  background-color: white;
  border: 2px solid #d88ca0;
  border-radius: 8px;
  color: #d88ca0;
  font-weight: 600;
  padding: 12px 24px;
  cursor: pointer;
  transition: all 0.3s;
}

.secondary-btn:hover {
  background-color: #fcf7f8;
}

.primary-btn {
  background-color: #d88ca0;
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  padding: 12px 24px;
  cursor: pointer;
  transition: all 0.3s;
}

.primary-btn:hover {
  background-color: #c27f92;
}

/* Mejora de la responsividad */
@media (max-width: 1200px) {
  .chess-tournament-bg {
    width: 35%;
  }

  .tournament-details {
    width: 65%;
    padding: 30px;
  }

  .details-title {
    font-size: 24px;
  }
}

@media (max-width: 992px) {
  .confirmation-background {
    flex-direction: column;
  }

  .chess-tournament-bg {
    width: 100%;
    height: 180px;
  }

  .tournament-details {
    width: 100%;
    padding: 30px 20px;
  }

  .confirmation-brand {
    font-size: 30px;
  }
}

@media (max-width: 768px) {
  .details-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .secondary-btn,
  .primary-btn {
    width: 100%;
    text-align: center;
  }

  .players-list {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  }
}

@media (max-width: 576px) {
  .tournament-details {
    padding: 20px 15px;
  }

  .details-card {
    padding: 20px;
  }

  .chess-tournament-bg {
    height: 150px;
  }

  .confirmation-brand {
    font-size: 24px;
  }

  .confirmation-tagline {
    font-size: 14px;
  }

  .success-icon {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }

  .points-grid {
    flex-direction: column;
    align-items: center;
    gap: 15px;
  }

  .point-item {
    flex-direction: row;
    width: 100%;
    justify-content: flex-start;
    gap: 15px;
  }

  .point-circle {
    width: 45px;
    height: 45px;
    font-size: 16px;
    margin-bottom: 0;
  }
}

@media (max-width: 350px) {
  .details-title {
    font-size: 20px;
  }

  .section-title {
    font-size: 16px;
  }

  .confirmation-brand {
    font-size: 20px;
  }
}
</style>

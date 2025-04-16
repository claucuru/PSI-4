<template>
    <div class="createtournament-container">
        <div class="createtournament-background">
            <!-- Parte izquierda con imagen de fondo -->
            <div class="chess-tournament-bg">
                <div class="chess-tournament-content">
                    <h1 class="login-brand">Crea un torneo</h1>
                    <p class="chesstournament-tagline">Organiza tu competencia de ajedrez</p>
                </div>
            </div>

            <!-- Parte derecha con el formulario -->
            <div class="create-tournament-form">
                <h2 class="form-title">Crear Torneo</h2>
                
                <div v-if="errorMessage" class="error-message">
                    {{ errorMessage }}
                </div>
                <div v-if="successMessage" class="success-message">
                    {{ successMessage }}
                </div>
                
                <div class="form-section">
                    <h3 class="section-title">Nombre del Torneo</h3>
                    <div class="input-group">
                        <label for="tournament-name">Nombre completo del torneo</label>
                        <input 
                            id="tournament-name" 
                            type="text" 
                            v-model="tournament.name" 
                            placeholder="Ej: Campeonato Nacional de Ajedrez 2024"
                        />
                    </div>
                    <div class="checkbox-group">
                        <input 
                            type="checkbox" 
                            id="admin-update" 
                            v-model="tournament.onlyAdminCanUpdate"
                        />
                        <label for="admin-update">Solo el administrador puede actualizar los juegos</label>
                    </div>
                </div>

                <div class="form-section">
                    <h3 class="section-title">Sistema de Emparejamiento</h3>
                    <div class="select-group">
                        <select v-model="tournament.pairing_system">
                            <option value="" disabled selected>Seleccione un sistema</option>
                            <option value="SW">Suizo</option>
                            <option value="RR">Round Robin</option>
                            <option value="KO">Eliminatoria</option>
                            <option value="TM">Por equipos</option>
                        </select>
                    </div>
                </div>

                <div class="form-section">
                    <h3 class="section-title">Tipo de Tablero</h3>
                    <div class="select-group">
                        <select v-model="tournament.board_type">
                            <option value="" disabled selected>Seleccione un tipo</option>
                            <option value="LIC">Lichess (Online)</option>
                            <option value="OTB">Presencial (OTB)</option>
                        </select>
                    </div>
                </div>

                <div class="form-section">
                    <h3 class="section-title">Velocidad del Torneo</h3>
                    <div class="select-group">
                        <select v-model="tournament.tournament_speed">
                            <option value="" disabled selected>Seleccione velocidad</option>
                            <option value="CL">Clásico</option>
                            <option value="RA">Rápido</option>
                            <option value="BL">Blitz</option>
                        </select>
                    </div>
                </div>

                <div class="form-section points-section">
                    <h3 class="section-title">Puntos otorgados</h3>
                    <div class="points-grid">
                        <div class="points-item">
                            <label>Victoria</label>
                            <input type="number" v-model="tournament.win_points" step="0.5" min="0" />
                        </div>
                        <div class="points-item">
                            <label>Empate</label>
                            <input type="number" v-model="tournament.draw_points" step="0.5" min="0" />
                        </div>
                        <div class="points-item">
                            <label>Derrota</label>
                            <input type="number" v-model="tournament.lose_points" step="0.5" min="0" />
                        </div>
                    </div>
                </div>

                <div class="form-section">
                    <h3 class="section-title">Métodos de Ranking</h3>
                    <p class="section-description">Seleccione los métodos de ranking en el orden que deben aplicarse</p>
                    <div class="checkbox-list">
                        <div class="checkbox-item" v-for="method in rankingMethods" :key="method.value">
                            <input 
                                type="checkbox" 
                                :id="method.value" 
                                v-model="tournament.ranking_methods" 
                                :value="method.value"
                            />
                            <label :for="method.value">{{ method.label }}</label>
                        </div>
                    </div>
                </div>

                <div class="form-section">
                    <h3 class="section-title">Jugadores</h3>
                    <p class="section-description">Lista de nombres de usuario de Lichess (uno por línea)</p>
                    <div class="textarea-group">
                        <textarea 
                            v-model="playersText" 
                            placeholder="Ingrese los nombres de usuario de Lichess, uno por línea"
                            rows="5"
                        ></textarea>
                    </div>
                </div>

                <!-- Sección para información de emails en modo OTB -->
                <div class="form-section" v-if="tournament.board_type === 'OTB'">
                    <h3 class="section-title">Información de jugadores (OTB)</h3>
                    <p class="section-description">Para torneos presenciales, necesitamos información adicional de los jugadores</p>
                    
                    <div v-for="(player, index) in playersList" :key="index" class="player-info-container">
                        <div class="player-header">
                            <span class="player-name">Jugador: {{ player }}</span>
                        </div>
                        <div class="input-group">
                            <label :for="'player-email-'+index">Email del jugador</label>
                            <input 
                                :id="'player-email-'+index" 
                                type="email" 
                                v-model="playerEmails[index]" 
                                placeholder="Ej: jugador@ejemplo.com"
                            />
                        </div>
                    </div>
                </div>

                <div class="form-actions">
                    <button class="cancel-btn" @click="cancelCreation">Cancelar</button>
                    <button class="create-btn" @click="createTournament" :disabled="isLoading">
                        {{ isLoading ? 'Creando...' : 'Crear Torneo' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import router from '../router';


export default {
    name: 'CreateTournament',
    data() {
        return {
            tournament: {
                name: '',
                onlyAdminCanUpdate: true,
                pairing_system: '',
                board_type: '',
                tournament_speed: '',
                win_points: 1.0,
                draw_points: 0.5,
                lose_points: 0.0,
                ranking_methods: [],
                start_date: new Date().toISOString().split('T')[0], // Fecha actual para el inicio
            },
            playersText: '',
            playersList: [],
            playerEmails: [],
            rankingMethods: [
                { value: 'BU', label: 'Buchholz (BU)' },
                { value: 'BC', label: 'Buchholz cut 1 (BC)' },
                { value: 'BA', label: 'Buchholz average (BA)' },
                { value: 'SB', label: 'Sonneborn-Berger (SB)' },
                { value: 'WI', label: 'Victorias (WI)' },
                { value: 'BL', label: 'Juegos con negras (BL)' }
            ],
            isLoading: false,
            errorMessage: '',
            successMessage: ''
        }
    },
    computed: {
        authStore() {
            return useAuthStore();
        },
        router() {
            return useRouter();
        }
    },
    watch: {
        playersText() {
            this.updatePlayersList();
        },
        'tournament.board_type'() {
            // Actualizar jugadores cuando cambie el tipo de tablero
            this.updatePlayersList();
        }
    },
    mounted() {
        // Verificar autenticación al cargar el componente
        if (!this.authStore.isAuthenticated) {
            this.errorMessage = 'Debe iniciar sesión para crear un torneo.';
            setTimeout(() => {
                router.push('/login');
            }, 2000);
        }
    },
    methods: {
        updatePlayersList() {
            this.playersList = this.playersText.split('\n')
                .map(name => name.trim())
                .filter(name => name.length > 0);
                
            // Ajustar el array de emails para que coincida con la cantidad de jugadores
            if (this.playersList.length > this.playerEmails.length) {
                // Añadir emails vacíos si hay más jugadores
                const diff = this.playersList.length - this.playerEmails.length;
                for (let i = 0; i < diff; i++) {
                    this.playerEmails.push('');
                }
            } else if (this.playersList.length < this.playerEmails.length) {
                // Recortar el array si hay menos jugadores
                this.playerEmails = this.playerEmails.slice(0, this.playersList.length);
            }
        },
        
        async validateLichessUsers() {
            // Solo validar si el tipo de tablero es Lichess
            if (this.tournament.board_type !== 'LI') {
                return true;
            }
            
            // Obtener la lista de usuarios
            const usernamesList = this.playersText.split('\n')
                .map(name => name.trim())
                .filter(name => name.length > 0);
            
            if (usernamesList.length === 0) {
                this.errorMessage = 'Debe ingresar al menos un jugador.';
                return false;
            }
            
            try {
                // Verificar la existencia de cada usuario en Lichess
                const invalidUsers = [];
                
                for (const username of usernamesList) {
                    try {
                        // Usar la API pública de Lichess para verificar usuarios
                        const response = await axios.get(`https://lichess.org/api/user/${username}`);
                        // Si no hay error, el usuario existe
                    } catch (error) {
                        // Si hay error, el usuario no existe
                        invalidUsers.push(username);
                    }
                }
                
                if (invalidUsers.length > 0) {
                    this.errorMessage = `Los siguientes usuarios no existen en Lichess: ${invalidUsers.join(', ')}`;
                    return false;
                }
                
                return true;
            } catch (error) {
                console.error('Error al validar usuarios de Lichess:', error);
                this.errorMessage = 'Error al validar usuarios. Por favor, inténtelo de nuevo.';
                return false;
            }
        },
        
        validatePlayerEmails() {
            if (this.tournament.board_type !== 'OT') {
                return true;
            }
            
            // Actualizar la lista de jugadores antes de validar
            this.updatePlayersList();
            
            // Verificar que hay emails para todos los jugadores
            if (this.playersList.length === 0) {
                this.errorMessage = 'Debe ingresar al menos un jugador.';
                return false;
            }
            
            // Verificar que todos los emails están completos
            const emptyEmails = this.playerEmails.some((email, index) => 
                !email.trim() && index < this.playersList.length
            );
            
            if (emptyEmails) {
                this.errorMessage = 'Debe proporcionar un email para cada jugador en modo presencial (OTB).';
                return false;
            }
            
            // Validar formato de emails
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const invalidEmails = this.playerEmails.some((email, index) => 
                index < this.playersList.length && !emailRegex.test(email)
            );
            
            if (invalidEmails) {
                this.errorMessage = 'Uno o más emails tienen formato inválido.';
                return false;
            }
            
            return true;
        },
        
        async createTournament() {
            this.isLoading = true;
            this.errorMessage = '';
            this.successMessage = '';
            
            // Verificar autenticación primero
            if (!this.authStore.isAuthenticated) {
                this.errorMessage = 'Debe iniciar sesión para crear un torneo.';
                this.isLoading = false;
                setTimeout(() => {
                    router.push('/login');
                }, 2000);
                return;
            }
            
            try {
                // Validar usuarios según el tipo de tablero
                if (this.tournament.board_type === 'LI') {
                    const usersValid = await this.validateLichessUsers();
                    if (!usersValid) {
                        this.isLoading = false;
                        return;
                    }
                } else if (this.tournament.board_type === 'OT') {
                    // Validar emails para torneo presencial
                    const emailsValid = this.validatePlayerEmails();
                    if (!emailsValid) {
                        this.isLoading = false;
                        return;
                    }
                }
                
                // Preparar datos para enviar a la API
                const tournamentData = {
                    name: this.tournament.name,
                    onlyAdminCanUpdate: this.tournament.onlyAdminCanUpdate,
                    pairing_system: this.tournament.pairing_system,
                    board_type: this.tournament.board_type,
                    tournament_speed: this.tournament.tournament_speed,
                    win_points: parseFloat(this.tournament.win_points),
                    draw_points: parseFloat(this.tournament.draw_points),
                    lose_points: parseFloat(this.tournament.lose_points),
                    start_date: this.tournament.start_date
                };

                // Obtener la lista de jugadores
                tournamentData.players = this.playersText.split('\n')
                    .map(name => name.trim())
                    .filter(name => name.length > 0);

                // Agregar los métodos de ranking al objeto
                tournamentData.ranking_methods = this.tournament.ranking_methods.map((method, index) => {
                    return {
                        value: method,
                        order: index + 1 // La posición en la lista determina el orden
                    };
                });
                
                // Agregar información de emails para torneos presenciales
                if (this.tournament.board_type === 'OT') {
                    tournamentData.playerEmails = {};
                    this.playersList.forEach((player, index) => {
                        if (index < this.playerEmails.length) {
                            tournamentData.playerEmails[player] = this.playerEmails[index];
                        }
                    });
                }

                // Obtener el token de autenticación del usuario desde el store
                const token = this.authStore.getToken;

                // Realizar la solicitud API con el token del store
                const response = await axios.post(
                    'http://localhost:8000/api/v1/tournaments/',
                    tournamentData,
                    {
                        headers: {
                            'Authorization': `Token ${token}`,
                            'Content-Type': 'application/json'
                        }
                    }
                );

                if (response && response.data) {
                this.successMessage = '¡Torneo creado exitosamente!';
                
                // Guardar los datos del torneo en localStorage como respaldo
                localStorage.setItem('lastCreatedTournament', JSON.stringify(response.data));

                    router.push({
                    name: 'TournamentConfirmation',  
                    params: {
                        tournament: response.data
                    }
                    });
                }

                
                // Manejar específicamente errores de autenticación
                if (error.response && error.response.status === 401) {
                    this.errorMessage = 'Su sesión ha expirado. Por favor, inicie sesión nuevamente.';
                    setTimeout(() => {
                        router.push('/login');
                    }, 2000);
                } else {
                    this.errorMessage = error.response?.data?.message || 
                                      'Ocurrió un error al crear el torneo. Por favor, inténtelo de nuevo.';
                }
            } finally {
                this.isLoading = false;
            }
        },
        
        cancelCreation() {
            if(confirm('¿Está seguro que desea cancelar la creación del torneo?')) {
                router.push('/');
            }
        }
    }
}
</script>

<style scoped>
.createtournament-container {
    min-height: 100vh;
    min-width: 100vw;
    background-color: #f8f9fa;
}

.createtournament-background {
    display: flex;
    min-height: 100vh;
}

/* Sección izquierda con imagen de fondo */
.chess-tournament-bg {
    width: 40%;
    background-image: url('../components/icons/chess.jpg');
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

/* Capa oscura para mejorar legibilidad del texto */
.chess-tournament-bg::before {
    content: '';
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

.login-brand {
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 16px;
    color: white;
}

.chesstournament-tagline {
    font-size: 18px;
    opacity: 0.9;
    line-height: 1.5;
    color: white;
}

/* Formulario de creación */
.create-tournament-form {
    width: 60%;
    padding: 40px;
    background-color: white;
    overflow-y: auto;
}

.form-title {
    color: #333;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 30px;
    text-align: center;
}

.form-section {
    margin-bottom: 30px;
}

/* Color rosa pastel suave para títulos (reemplazado #ff6b98) */
.section-title {
    color: #e091a9; /* Rosa pastel más suave */
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 16px;
}

/* Rosa pastel medio para descripciones (reemplazado #f296b6) */
.section-description {
    color: #d9a6b3; /* Rosa pastel medio más suave */
    font-size: 14px;
    margin-bottom: 16px;
}

.input-group, .textarea-group {
    margin-bottom: 20px;
}

/* Textos en elementos de formulario (reemplazado #ff6b98) */
.input-group label, .textarea-group label, .points-item label, .checkbox-item label, .select-group select {
    display: block;
    margin-bottom: 8px;
    color: #d88ca0; /* Rosa pastel más suave */
    font-weight: 500;
}

/* Rosa pastel claro para bordes (reemplazado #ffd2e0) */
.input-group input, .textarea-group textarea, .select-group select {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #f0d4dc; /* Rosa pastel claro más suave */
    border-radius: 8px;
    font-size: 16px;
    transition: border-color 0.3s;
}

/* Rosa pastel medio para foco (reemplazado #ff8daa) */
.input-group input:focus, .textarea-group textarea:focus, .select-group select:focus {
    border-color: #e0b0bd; /* Rosa pastel medio más suave */
    outline: none;
}

.select-group select {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #f0d4dc;
    border-radius: 8px;
    font-size: 16px;
    color: #d88ca0;
    background-color: white;
    transition: border-color 0.3s;
}

.checkbox-group {
    display: flex;
    align-items: center;
    margin-top: 15px;
}

.checkbox-group input {
    margin-right: 10px;
}

.checkbox-group label {
    color: #d88ca0;
    font-size: 15px;
}

/* Fondo rosa muy claro para sección de puntos (reemplazado #fff5f8) */
.points-section {
    background-color: #fcf7f8; /* Rosa muy suave, casi blanco */
    padding: 20px;
    border-radius: 12px;
}

.points-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.points-item {
    background-color: white;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.points-item input {
    width: 100%;
    padding: 10px 12px;
    border: 2px solid #f0d4dc;
    border-radius: 8px;
    font-size: 16px;
    text-align: center;
}

.checkbox-list {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
}

.checkbox-item {
    display: flex;
    align-items: center;
    background-color: white;
    padding: 12px 15px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.checkbox-item input {
    margin-right: 10px;
}

.textarea-group textarea {
    width: 100%;
    min-height: 100px;
    padding: 12px 16px;
    border: 2px solid #f0d4dc;
    border-radius: 8px;
    font-size: 16px;
    resize: vertical;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 20px;
    margin-top: 30px;
    padding-top: 30px;
    border-top: 1px solid #f0d4dc;
}

/* Botón de cancelar (reemplazado #ff6b98) */
.cancel-btn {
    background-color: white;
    border: 2px solid #d88ca0;
    border-radius: 8px;
    color: #d88ca0;
    font-weight: 600;
    padding: 12px 24px;
    cursor: pointer;
    transition: all 0.3s;
}

.cancel-btn:hover {
    background-color: #fcf7f8;
}

/* Botón de crear (reemplazado #ff6b98 y #ff4c82) */
.create-btn {
    background-color: #d88ca0;
    border: none;
    border-radius: 8px;
    color: white;
    font-weight: 600;
    padding: 12px 24px;
    cursor: pointer;
    transition: all 0.3s;
}

.create-btn:hover {
    background-color: #c27f92;
}

.create-btn:disabled {
    background-color: #e9c5ce;
    cursor: not-allowed;
}

.error-message {
    background-color: #ffebee;
    color: #c62828;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 20px;
    text-align: center;
}

.success-message {
    background-color: #e8f5e9;
    color: #2e7d32;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 20px;
    text-align: center;
}

/* Estilos adicionales para la información de jugadores OTB */
.player-info-container {
    background-color: #fcf7f8;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 15px;
}

.player-header {
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid #f0d4dc;
}

.player-name {
    font-weight: 600;
    color: #d88ca0;
}

/* Mejora de la responsividad */
@media (max-width: 1200px) {
    .chess-tournament-bg {
        width: 35%;
    }
    
    .create-tournament-form {
        width: 65%;
        padding: 30px;
    }
    
    .form-title {
        font-size: 28px;
    }
}

@media (max-width: 992px) {
    .createtournament-background {
        flex-direction: column;
    }
    
    .chess-tournament-bg {
        width: 100%;
        height: 180px;
    }
    
    .create-tournament-form {
        width: 100%;
        padding: 30px 20px;
    }
    
    .login-brand {
        font-size: 30px;
    }
}

@media (max-width: 768px) {
    .points-grid {
        grid-template-columns: 1fr;
        gap: 15px;
    }
    
    .checkbox-list {
        grid-template-columns: 1fr;
    }
    
    .form-actions {
        flex-direction: column-reverse;
    }
    
    .cancel-btn, .create-btn {
        width: 100%;
        text-align: center;
    }
    
    .form-title {
        font-size: 24px;
    }
    
    .section-title {
        font-size: 18px;
    }
}

@media (max-width: 576px) {
    .create-tournament-form {
        padding: 20px 15px;
    }
    
    .chess-tournament-bg {
        height: 150px;
    }
    
    .login-brand {
        font-size: 24px;
    }
    
    .chesstournament-tagline {
        font-size: 14px;
    }
    
    .input-group input, 
    .select-group select, 
    .textarea-group textarea {
        padding: 10px 12px;
        font-size: 14px;
    }
    
    .form-section {
        margin-bottom: 20px;
    }
}

/* Para pantallas muy pequeñas */
@media (max-width: 350px) {
    .form-title {
        font-size: 20px;
    }
    
    .section-title {
        font-size: 16px;
    }
    
    .login-brand {
        font-size: 20px;
    }
}
</style>
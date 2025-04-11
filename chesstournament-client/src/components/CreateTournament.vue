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
                        <select v-model="tournament.pairingSystem">
                            <option value="" disabled selected>Seleccione un sistema</option>
                            <option value="swiss">Suizo</option>
                            <option value="round-robin">Round Robin</option>
                            <option value="knockout">Eliminatoria</option>
                            <option value="team">Por equipos</option>
                        </select>
                    </div>
                </div>

                <div class="form-section">
                    <h3 class="section-title">Tipo de Tablero</h3>
                    <div class="select-group">
                        <select v-model="tournament.boardType">
                            <option value="" disabled selected>Seleccione un tipo</option>
                            <option value="lichess">Lichess (Online)</option>
                            <option value="chesscom">Chess.com (Online)</option>
                            <option value="otb">Presencial (OTB)</option>
                            <option value="other">Otro</option>
                        </select>
                    </div>
                </div>

                <div class="form-section points-section">
                    <h3 class="section-title">Puntos otorgados</h3>
                    <div class="points-grid">
                        <div class="points-item">
                            <label>Victoria</label>
                            <input type="number" v-model="tournament.points.win" step="0.5" min="0" />
                        </div>
                        <div class="points-item">
                            <label>Empate</label>
                            <input type="number" v-model="tournament.points.draw" step="0.5" min="0" />
                        </div>
                        <div class="points-item">
                            <label>Derrota</label>
                            <input type="number" v-model="tournament.points.lose" step="0.5" min="0" />
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
                                v-model="tournament.rankingMethods" 
                                :value="method.value"
                            />
                            <label :for="method.value">{{ method.label }}</label>
                        </div>
                    </div>
                </div>

                <div class="form-actions">
                    <button class="cancel-btn" @click="cancelCreation">Cancelar</button>
                    <button class="create-btn" @click="createTournament">Crear Torneo</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CreateTournament',
    data() {
        return {
            tournament: {
                name: '',
                onlyAdminCanUpdate: true,
                pairingSystem: '',
                boardType: '',
                points: {
                    win: 1.0,
                    draw: 0.5,
                    lose: 0.0
                },
                rankingMethods: []
            },
            rankingMethods: [
                { value: 'BU', label: 'Buchholz (BU)' },
                { value: 'BC', label: 'Buchholz cut 1 (BC)' },
                { value: 'BA', label: 'Buchholz average (BA)' },
                { value: 'SB', label: 'Sonneborn-Berger (SB)' }
            ]
        }
    },
    methods: {
        createTournament() {
            console.log('Torneo creado:', this.tournament);
            // Aquí iría la lógica para enviar los datos al servidor
            alert('Torneo creado exitosamente!');
            this.$router.push('/');
        },
        cancelCreation() {
            if(confirm('¿Está seguro que desea cancelar la creación del torneo?')) {
                this.$router.push('/');
            }
        }
    }
}
</script>

<style scoped>
.createtournament-container {
    min-height: 100vh;
    min-width: 90vw;
    background-color: #f8f9fa;
}

.createtournament-background {
    display: flex;
    min-height: 100vh;
}

/* Sección izquierda con imagen de fondo */
.chess-tournament-bg {
    width: 60%;
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
    width: 120%;
    padding: 60px;
    background-color: white;
    overflow-y: auto;
}

.form-title {
    color: #333;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 40px;
    text-align: center;
}

.form-section {
    margin-bottom: 40px;
}

.section-title {
    color: #6b5876;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 16px;
}

.section-description {
    color: #9f7ead;
    font-size: 14px;
    margin-bottom: 16px;
}

.input-group {
    margin-bottom: 20px;
}

.input-group label {
    display: block;
    margin-bottom: 8px;
    color: #6b5876;
    font-weight: 500;
}

.input-group input {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #e6d5f2;
    border-radius: 8px;
    font-size: 16px;
    transition: border-color 0.3s;
}

.input-group input:focus {
    border-color: #bb8fce;
    outline: none;
}

.select-group select {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #e6d5f2;
    border-radius: 8px;
    font-size: 16px;
    color: #6b5876;
    background-color: white;
    transition: border-color 0.3s;
}

.select-group select:focus {
    border-color: #bb8fce;
    outline: none;
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
    color: #6b5876;
    font-size: 15px;
}

.points-section {
    background-color: #faf5ff;
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

.points-item label {
    display: block;
    margin-bottom: 8px;
    color: #9b59b6;
    font-weight: 600;
}

.points-item input {
    width: 100%;
    padding: 10px 12px;
    border: 2px solid #e6d5f2;
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

.checkbox-item label {
    color: #6b5876;
    font-size: 15px;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 20px;
    margin-top: 40px;
    padding-top: 30px;
    border-top: 1px solid #e6d5f2;
}

.cancel-btn {
    background-color: white;
    border: 2px solid #e74c3c;
    border-radius: 8px;
    color: #e74c3c;
    font-weight: 600;
    padding: 12px 24px;
    cursor: pointer;
    transition: all 0.3s;
}

.cancel-btn:hover {
    background-color: #fdecea;
}

.create-btn {
    background-color: #9b59b6;
    border: none;
    border-radius: 8px;
    color: white;
    font-weight: 600;
    padding: 12px 24px;
    cursor: pointer;
    transition: all 0.3s;
}

.create-btn:hover {
    background-color: #8e44ad;
}

/* Responsive */
@media (max-width: 1200px) {
    .chess-tournament-bg {
        width: 35%;
    }
    
    .create-tournament-form {
        width: 65%;
        padding: 40px;
    }
}

@media (max-width: 992px) {
    .createtournament-background {
        flex-direction: column;
    }
    
    .chess-tournament-bg {
        width: 100%;
        height: 200px;
    }
    
    .create-tournament-form {
        width: 100%;
        padding: 40px 20px;
    }
}

@media (max-width: 768px) {
    .points-grid {
        grid-template-columns: 1fr;
    }
    
    .checkbox-list {
        grid-template-columns: 1fr;
    }
    
    .form-actions {
        flex-direction: column-reverse;
    }
    
    .cancel-btn, .create-btn {
        width: 100%;
    }
}

@media (max-width: 576px) {
    .create-tournament-form {
        padding: 30px 20px;
    }
    
    .login-brand {
        font-size: 28px;
    }
    
    .chesstournament-tagline {
        font-size: 16px;
    }
}
</style>
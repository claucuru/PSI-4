<template>
    <div class="faq-page">
      <HeaderComponent />
      
      <div class="hero-section">
        <div class="hero-content">
          <h1 class="hero-title">Preguntas Frecuentes</h1>
          <p class="hero-subtitle">Encuentra respuestas a las dudas más comunes sobre nuestra plataforma de torneos de ajedrez.</p>
        </div>
      </div>
      
      <div class="main-content">
        <div class="container">
          <!-- Buscador de preguntas -->
          <div class="faq-search">
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Buscar preguntas..."
              @input="filterQuestions"
              class="faq-search-input"
              data-cy="faq-search"
            >
            <button class="search-button" @click="filterQuestions">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </button>
          </div>
          
          <!-- Categorías de preguntas -->
          <div class="faq-categories">
            <button 
              class="category-btn" 
              :class="{ active: activeCategory === 'all' }"
              @click="setCategory('all')"
              data-cy="category-all"
            >
              Todas
            </button>
            <button 
              v-for="category in categories" 
              :key="category.id" 
              class="category-btn" 
              :class="{ active: activeCategory === category.id }"
              @click="setCategory(category.id)"
              :data-cy="`category-${category.id}`"
            >
              {{ category.name }}
            </button>
          </div>
          
          <!-- Lista de preguntas -->
          <div class="faq-list">
            <div 
              v-for="(question, index) in filteredQuestions" 
              :key="index" 
              class="faq-item"
              :data-cy="`faq-item-${index}`"
            >
              <div 
                class="faq-question" 
                @click="toggleQuestion(index)"
                :class="{ 'is-open': openQuestions[index] }"
              >
                <h3>{{ question.question }}</h3>
                <span class="toggle-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="6 9 12 15 18 9"></polyline>
                  </svg>
                </span>
              </div>
              <div class="faq-answer" v-show="openQuestions[index]">
                <p v-html="question.answer"></p>
              </div>
            </div>
          </div>
          
          <!-- Estado sin resultados -->
          <div v-if="filteredQuestions.length === 0" class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <h3>No se encontraron preguntas</h3>
            <p>Intenta con otros términos de búsqueda o selecciona otra categoría.</p>
          </div>
          
          <!-- Contacto para más ayuda -->
          <div class="contact-support">
            <h3>¿No encontraste lo que buscabas?</h3>
            <p>Si tienes alguna pregunta que no esté respondida aquí, no dudes en contactarnos.</p>
            <!--Nos lleva al footer-->
            <a href="#footer" class="contact-btn" data-cy="contact-support">
              Contactar Soporte
            </a>

          </div>
        </div>
      </div>
      
      <!-- Footer -->
      <footer class="site-footer" id="footer">
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
  import { ref, computed, onMounted } from 'vue'
  import HeaderComponent from './Header.vue'
  
  export default {
    name: 'FaqView',
    components: {
      HeaderComponent
    },
    setup() {
      const searchQuery = ref('')
      const activeCategory = ref('all')
      const openQuestions = ref({})
      
      // Definir categorías
      const categories = [
        { id: 'general', name: 'General' },
        { id: 'torneos', name: 'Torneos' },
        { id: 'jugadores', name: 'Jugadores' },
        { id: 'sistema', name: 'Sistema' }
      ]
      
      // Lista completa de preguntas
      const allQuestions = [
        {
          question: '¿Qué es TournamentMaster?',
          answer: 'TournamentMaster es una plataforma web diseñada para la gestión y seguimiento de torneos de ajedrez. Permite crear torneos, gestionar participantes, registrar resultados y visualizar clasificaciones de forma intuitiva y en tiempo real.',
          category: 'general'
        },
        {
          question: '¿Necesito crear una cuenta para participar en un torneo?',
          answer: 'No es necesario crear una cuenta para participar en torneos como jugador. Podrás acceder a la información de los torneos y enviar resultados identificándote con tu correo electrónico. Sin embargo, para crear y administrar torneos sí necesitarás una cuenta con permisos de administrador.',
          category: 'general'
        },
        {
          question: '¿Cómo puedo crear un torneo?',
          answer: 'Para crear un torneo necesitas tener una cuenta de administrador. Una vez iniciada sesión, verás un botón "Crear torneo" en la página principal. Al hacer clic, se abrirá un formulario donde podrás configurar todos los detalles del torneo: nombre, fechas, tipo de torneo, número de rondas, controles de tiempo y tipo de tablero (presencial u online).',
          category: 'torneos'
        },
        {
          question: '¿Qué tipos de torneos puedo crear?',
          answer: 'Actualmente TournamentMaster soporta cuatro formatos de torneos:<br><br>• <strong>Suizo (SW)</strong>: Emparejamiento suizo tradicional.<br>• <strong>Round Robin (RR)</strong>: Todos contra todos.<br>• <strong>Eliminación (KO)</strong>: Sistema de eliminación directa.<br>• <strong>Por equipos (TE)</strong>: Competición entre equipos.',
          category: 'torneos'
        },
        {
          question: '¿Cuál es la diferencia entre un torneo OTB y LIC?',
          answer: '"OTB" (Over The Board) se refiere a torneos presenciales donde los jugadores se enfrentan físicamente en un tablero. "LIC" se refiere a torneos online jugados a través de la plataforma Lichess, donde los resultados se pueden verificar automáticamente. En torneos OTB, los jugadores deben reportar manualmente los resultados, mientras que en LIC la plataforma puede recuperar y verificar los resultados automáticamente.',
          category: 'torneos'
        },
        {
          question: '¿Cómo reporto el resultado de una partida?',
          answer: 'Para reportar el resultado de una partida, debes acceder a la página de detalles del torneo y localizar tu partida. Hay una opción para "Registrar resultado" donde puedes seleccionar el ganador o indicar tablas. En torneos presenciales (OTB), se te pedirá verificar tu identidad con tu correo electrónico.',
          category: 'jugadores'
        },
        {
          question: '¿Puedo modificar un resultado ya reportado?',
          answer: 'Como jugador, no puedes modificar un resultado una vez reportado. Si hay algún error, debes contactar con el administrador del torneo quien tiene la capacidad de modificar cualquier resultado.',
          category: 'jugadores'
        },
        {
          question: '¿Cómo se calculan los puntos en la clasificación?',
          answer: 'Por defecto, se asigna 1 punto por victoria, 0.5 puntos por tablas y 0 puntos por derrota. En torneos por equipos o con sistemas de puntuación especiales, el administrador puede configurar un sistema de puntuación diferente al crear el torneo.',
          category: 'torneos'
        },
        {
          question: '¿Cómo puedo ver las clasificaciones y resultados de un torneo?',
          answer: 'En la página principal puedes ver todos los torneos disponibles. Al hacer clic en "Ver detalles" de cualquier torneo, accederás a una página con pestañas que muestran la clasificación actual y los emparejamientos por rondas.',
          category: 'jugadores'
        },
        {
          question: '¿Puedo buscar torneos específicos?',
          answer: 'Sí, en la página principal hay un buscador donde puedes introducir palabras clave para encontrar torneos por su nombre. Próximamente implementaremos filtros adicionales por fecha, tipo de torneo y ubicación.',
          category: 'general'
        },
        {
          question: '¿Qué debo hacer si mi usuario de Lichess no es reconocido?',
          answer: 'Si al crear un torneo de tipo LIC tu usuario de Lichess no es reconocido, verifica que has escrito correctamente el nombre de usuario. Considera que Lichess distingue entre mayúsculas y minúsculas. Si el problema persiste, asegúrate de que la cuenta existe y es pública en Lichess.',
          category: 'sistema'
        },
        {
          question: '¿La plataforma tiene algún costo?',
          answer: 'Actualmente TournamentMaster es completamente gratuito tanto para organizadores como para jugadores. En un futuro, podríamos introducir planes premium con características adicionales, pero mantendremos siempre una versión funcional gratuita.',
          category: 'general'
        },
        {
          question: '¿Cómo puedo obtener una cuenta de administrador?',
          answer: 'Las cuentas de administrador son creadas por el equipo de TournamentMaster. Si eres un organizador de torneos y deseas obtener una cuenta de administrador, puedes contactarnos a través del formulario de contacto y revisaremos tu solicitud.',
          category: 'sistema'
        },
        {
          question: '¿Es posible exportar los datos de un torneo?',
          answer: 'Sí, los administradores pueden exportar los datos de un torneo en formato CSV o PDF desde la página de detalles del torneo. Esto incluye la lista de participantes, emparejamientos, resultados y clasificación final.',
          category: 'torneos'
        },
        {
          question: '¿La plataforma funciona en dispositivos móviles?',
          answer: 'Sí, TournamentMaster está diseñado con un enfoque responsive que se adapta automáticamente a cualquier tamaño de pantalla, permitiendo una experiencia óptima tanto en ordenadores como en tablets y smartphones.',
          category: 'sistema'
        }
      ]
      
      // Filtrar preguntas según categoría y búsqueda
      const filteredQuestions = computed(() => {
        let result = allQuestions
  
        // Filtrar por categoría
        if (activeCategory.value !== 'all') {
          result = result.filter(q => q.category === activeCategory.value)
        }
        
        // Filtrar por búsqueda
        if (searchQuery.value.trim()) {
          const searchTerms = searchQuery.value.toLowerCase().trim()
          result = result.filter(q => 
            q.question.toLowerCase().includes(searchTerms)
          )
        }
        
        return result
      })
      
      // Cambiar categoría activa
      const setCategory = (categoryId) => {
        activeCategory.value = categoryId
        // Resetear estados de apertura al cambiar de categoría
        openQuestions.value = {}
      }
      
      // Filtrar preguntas (usado por el buscador)
      const filterQuestions = () => {
        // Resetear estados de apertura al buscar
        openQuestions.value = {}
      }
      
      // Abrir/cerrar una pregunta
      const toggleQuestion = (index) => {
        openQuestions.value = {
          ...openQuestions.value,
          [index]: !openQuestions.value[index]
        }
      }
      
      // Al montar, abrir la primera pregunta
      onMounted(() => {
        if (filteredQuestions.value.length > 0) {
          openQuestions.value = { 0: true }
        }
      })
      
      return {
        searchQuery,
        categories,
        activeCategory,
        filteredQuestions,
        openQuestions,
        setCategory,
        filterQuestions,
        toggleQuestion
      }
    }
  }
  </script>
  
  <style scoped>
  .faq-page {
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
    padding: 60px 0;
    flex-grow: 1;
  }
  
  .container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 20px;
  }
  
  .faq-search {
    display: flex;
    max-width: 700px;
    margin: 0 auto 40px;
  }
  
  .faq-search-input {
    border: 2px solid #e6d5f2;
    border-radius: 8px 0 0 8px;
    color: #333;
    flex: 1;
    font-size: 16px;
    padding: 14px 20px;
    transition: border-color 0.3s;
  }
  
  .faq-search-input:focus {
    border-color: #bb8fce;
    outline: none;
    box-shadow: 0 0 0 3px rgba(187, 143, 206, 0.2);
  }
  
  .search-button {
    background-color: #9b59b6;
    border: none;
    border-radius: 0 8px 8px 0;
    color: white;
    cursor: pointer;
    padding: 0 25px;
    transition: background-color 0.3s;
  }
  
  .search-button:hover {
    background-color: #8e44ad;
  }
  
  .faq-categories {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 40px;
  }
  
  .category-btn {
    background-color: transparent;
    border: 2px solid #e6d5f2;
    border-radius: 50px;
    color: #6b5876;
    cursor: pointer;
    font-size: 15px;
    font-weight: 600;
    padding: 10px 20px;
    transition: all 0.3s;
  }
  
  .category-btn:hover {
    background-color: #f8f0fd;
    border-color: #bb8fce;
    color: #9b59b6;
  }
  
  .category-btn.active {
    background-color: #9b59b6;
    border-color: #9b59b6;
    color: white;
  }
  
  .faq-list {
    margin-bottom: 60px;
  }
  
  .faq-item {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    margin-bottom: 16px;
    overflow: hidden;
    transition: box-shadow 0.3s;
  }
  
  .faq-item:hover {
    box-shadow: 0 6px 20px rgba(155, 89, 182, 0.15);
  }
  
  .faq-question {
    align-items: center;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    padding: 20px 24px;
    transition: background-color 0.3s;
  }
  
  .faq-question:hover {
    background-color: #f8f0fd;
  }
  
  .faq-question.is-open {
    background-color: #f8f0fd;
    border-bottom: 1px solid #e6d5f2;
  }
  
  .faq-question h3 {
    color: #333;
    font-size: 18px;
    font-weight: 600;
    margin: 0;
    transition: color 0.3s;
  }
  
  .faq-question:hover h3 {
    color: #9b59b6;
  }
  
  .toggle-icon {
    color: #9b59b6;
    transition: transform 0.3s;
  }
  
  .faq-question.is-open .toggle-icon {
    transform: rotate(180deg);
  }
  
  .faq-answer {
    background-color: white;
    padding: 6px 24px 24px;
  }
  
  .faq-answer p {
    color: #6b5876;
    font-size: 16px;
    line-height: 1.6;
    margin: 0;
  }
  
  .empty-state {
    text-align: center;
    padding: 60px 0;
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
  
  .contact-support {
    background-color: #f8f0fd;
    border-radius: 12px;
    padding: 40px;
    text-align: center;
    margin-bottom: 60px;
  }
  
  .contact-support h3 {
    color: #333;
    font-size: 24px;
    font-weight: 700;
    margin: 0 0 12px 0;
  }
  
  .contact-support p {
    color: #6b5876;
    font-size: 16px;
    margin: 0 auto 24px;
    max-width: 500px;
  }
  
  .contact-btn {
    background-color: #9b59b6;
    border: none;
    border-radius: 8px;
    color: white;
    display: inline-block;
    font-size: 16px;
    font-weight: 600;
    padding: 14px 30px;
    text-decoration: none;
    transition: all 0.3s;
  }
  
  .contact-btn:hover {
    background-color: #8e44ad;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(155, 89, 182, 0.3);
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
  
  @media (max-width: 768px) {
    .hero-title {
      font-size: 32px;
    }
    
    .hero-subtitle {
      font-size: 18px;
    }
    
    .faq-question h3 {
      font-size: 16px;
    }
    
    .contact-support {
      padding: 30px 20px;
    }
    
    .footer-content {
      flex-direction: column;
      text-align: center;
    }
    
    .authors-list {
      justify-content: center;
    }
  }
  </style>
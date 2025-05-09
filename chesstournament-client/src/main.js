import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
import "./assets/main.css";

// Configuración de URLs según entorno
const DJANGO_URL = import.meta.env.VITE_DJANGO_URL;
const RENDER_URL = import.meta.env.VITE_RENDER_URL;

// Seleccionar URL base según variable de entorno de testing
axios.defaults.baseURL = import.meta.env.VITE_TESTING === 'true' ? DJANGO_URL : RENDER_URL ;

alert(`Usando API: ${axios.defaults.baseURL}`);

const app = createApp(App);
const pinia = createPinia();
app.use(pinia);
app.use(router);
app.mount("#app");

// Interceptor para añadir el token a todas las solicitudes
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});
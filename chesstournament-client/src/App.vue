<script setup>
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <header>
    <nav class="navbar">
      <div class="logo">
        <img alt="Logo" src="./assets/logo.svg" width="30" height="30" />
        <span>Chess Tournament</span>
      </div>
      
      <div class="nav-links">
        <router-link to="/">Inicio</router-link>
        
        <template v-if="authStore.isAuthenticated">
          <span>Bienvenido, {{ authStore.user?.username }}</span>
          <button @click="authStore.logout" class="logout-btn">Cerrar sesión</button>
        </template>
        <template v-else>
          <router-link to="/log-in">Iniciar sesión</router-link>
        </template>
      </div>
    </nav>
  </header>

  <main>
    <router-view />
  </main>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #2c3e50;
  color: white;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-links a {
  color: white;
  text-decoration: none;
}

.nav-links a:hover {
  text-decoration: underline;
}

.logout-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
}

main {
  padding: 2rem;
}
</style>
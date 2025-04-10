<script setup>
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <main>
    <router-view />
  </main>
</template>

<style>
</style>
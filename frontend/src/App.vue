<script setup>
import { onMounted, ref } from 'vue'
import { RouterView } from 'vue-router'

import { useAuthStore } from './stores/auth'

import NavBar from '@/components/navbar/NavBar.vue'

import './assets/style.css'

const isLoading = ref(true)

// Check if user is logged in before rendering page
onMounted(async () => {
  const authStore = useAuthStore()
  try {
    await authStore.getUser()
  } catch (error) {
    isLoading.value = false
  }
  isLoading.value = false
})
</script>

<template>
  <div id="app" v-if="!isLoading">
    <NavBar />
    <RouterView />
  </div>
</template>

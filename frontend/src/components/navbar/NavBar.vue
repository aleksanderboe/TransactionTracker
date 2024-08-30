<script setup>
import NavBarGuest from './NavBarGuest.vue'
import NavBarUser from './NavBarUser.vue'

import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <NavBarUser v-if="authStore.isAuthenticated" />
  <NavBarGuest v-else />
</template>

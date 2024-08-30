<script setup>
import NavBarLink from './NavBarLink.vue'

import ThemeToggle from '@/components/ui/ThemeToggle.vue'
</script>

<template>
  <nav class="navbar navbar-expand-sm navbar-dark bg-dark mb-4 fs-5">
    <div class="container-fluid">
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ThemeToggle></ThemeToggle>
        <div class="navbar-nav">
          <NavBarLink name="Login" route="/login" />
          <NavBarLink name="Register" route="/register" />
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped></style>

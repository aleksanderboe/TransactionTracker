<script setup>
import NavBarLink from './NavBarLink.vue'

import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()

import ThemeToggle from '@/components/ui/ThemeToggle.vue'
</script>

<template>
  <nav class="navbar navbar-expand-sm navbar-dark bg-dark mb-4 fs-5">
    <div class="container-fluid">
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarUser"
        aria-controls="navbarUser"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>|
      </button>
      <div class="collapse navbar-collapse" id="navbarUser">
        <NavBarLink route="/" class="me-3">Dashboard</NavBarLink>
        <NavBarLink route="/transactions">Transactions</NavBarLink>

        <div class="navbar-nav ms-auto">
          <ThemeToggle></ThemeToggle>
          <div class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              id="navbarDropdownMenuLink"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <img :src="authStore.profilePicture" alt="Profile" class="profile-image" />
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li>
                <NavBarLink route="/profile">
                  <a class="dropdown-item">
                    <i class="bi bi-person"></i>
                    Profile
                  </a>
                </NavBarLink>
              </li>
              <li><hr class="dropdown-divider" /></li>
              <li>
                <NavBarLink route="/logout">
                  <a class="dropdown-item text-danger" href="/logout">
                    <i class="bi bi-door-open"></i>
                    Logout
                  </a>
                </NavBarLink>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.profile-image {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 5px;
}
</style>

<script setup>
import { ref, onMounted } from 'vue'

const lightIcon = 'bi bi-sun-fill'
const darkIcon = 'bi bi-moon-fill'
const activeIcon = ref(lightIcon)

const applyTheme = (theme) => {
  const htmlElement = document.documentElement
  htmlElement.setAttribute('data-bs-theme', theme)
  localStorage.setItem('theme', theme)

  if (theme === 'dark') {
    activeIcon.value = darkIcon
    document.body.classList.remove('bg-light')
  } else {
    activeIcon.value = lightIcon
    document.body.classList.add('bg-light')
  }
}

// Check local storage for a saved theme and apply it
onMounted(() => {
  const theme = localStorage.getItem('theme')
  if (theme) {
    applyTheme(theme)
  }
})

const changeTheme = () => {
  const currentTheme = document.documentElement.getAttribute('data-bs-theme')
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark'
  applyTheme(newTheme)
}
</script>

<template>
  <button @click="changeTheme" class="btn btn-link">
    <i :class="[activeIcon, 'text-light', 'fs-4']" alt="Change Theme"></i>
  </button>
</template>

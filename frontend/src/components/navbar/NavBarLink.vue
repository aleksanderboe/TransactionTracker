<script setup>
const props = defineProps({
  name: {
    type: String
  },
  route: {
    type: String,
    default: '/'
  }
})
</script>

<template>
  <router-link :to="props.route" class="nav-link"
    ><slot>{{ props.name }}</slot>
  </router-link>
</template>

<style scoped>
nav a.router-link-exact-active {
  text-decoration: underline;
  text-underline-offset: 0.5rem;
  color: #ffdd57;
}

nav a {
  color: #ffffff;
}

nav a:hover {
  color: #ffd700;
}
</style>

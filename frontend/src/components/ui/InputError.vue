<script setup>
defineProps({
  error: {
    type: String,
    required: true
  }
})
</script>

<template>
  <p class="text-danger" v-show="error">{{ error }}</p>
</template>

<style scoped></style>

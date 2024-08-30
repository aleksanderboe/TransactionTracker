<script setup>
defineProps({ title: String })
defineEmits(['submit'])
</script>

<template>
  <div class="container py-4 d-flex justify-content-center">
    <div class="card shadow-sm w-auto" style="min-width: 380px">
      <div class="card-body text-center">
        <h1 class="card-title">{{ title }}</h1>
        <form @submit.prevent="$emit('submit')">
          <slot></slot>
        </form>
      </div>
    </div>
  </div>
</template>

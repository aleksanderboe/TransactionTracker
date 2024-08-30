<script setup>
defineProps({
  message: String
})
</script>

<template>
  <div
    v-if="message"
    class="p-3 text-danger bg-danger-subtle border border-danger-subtle rounded-3 d-flex align-items-center justify-content center gap-2"
    :class="$attrs.class"
  >
    <i class="bi bi-exclamation-circle fs-4"></i>

    {{ message }}
  </div>
</template>

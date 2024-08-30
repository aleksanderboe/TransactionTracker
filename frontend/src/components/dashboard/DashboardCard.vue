<script setup>
defineProps({
  value: {
    required: true
  },
  title: {
    type: String,
    required: true
  },
  icon: {
    type: String,
    required: true
  },
  iconColor: {
    type: String,
    required: true
  },
  iconBgColor: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div class="card rounded border-0 shadow-sm">
    <div class="card-body d-flex align-items-start">
      <span :class="iconBgColor" class="badge badge-l p-2 me-3">
        <i :class="[icon, iconColor]" style="font-size: 4em"></i>
      </span>
      <div>
        <p class="card-text fs-4 fw-bold mb-0">
          {{ value }}
        </p>
        <h5 class="card-title text-muted">{{ title }}</h5>
      </div>
    </div>
  </div>
</template>

<style scoped></style>

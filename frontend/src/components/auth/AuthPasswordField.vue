<script setup>
import { ref } from 'vue'

const model = defineModel()

const emit = defineEmits(['onInputChange'])

const passwordVisible = ref(false)

defineProps({
  id: {
    type: String,
    required: true
  },
  label: {
    type: String,
    required: false
  },
  placeholder: {
    type: String,
    required: false
  }
})
</script>

<template>
  <input
    :type="passwordVisible ? 'text' : 'password'"
    class="form-control"
    :id="id"
    :placeholder="placeholder"
    v-model="model"
    @input="emit('onInputChange')"
    required
  />
  <label for="{{id}}">{{ label }}</label>
  <button
    type="button"
    @click="passwordVisible = !passwordVisible"
    class="btn border-0 position-absolute end-0 top-0"
    style="height: 100%"
  >
    <i class="h4" :class="passwordVisible ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill'"></i>
  </button>
</template>

<style scoped></style>

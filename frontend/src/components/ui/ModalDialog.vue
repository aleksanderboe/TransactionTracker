<script setup>
import { onMounted, onBeforeUnmount } from 'vue'

const emit = defineEmits(['close'])

const closeModal = () => {
  emit('close')
}

const handleKeyPress = (event) => {
  if (event.key === 'Escape') {
    closeModal()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeyPress)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeyPress)
})
</script>

<template>
  <div class="modal show d-block" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header text-center">
          <h1 class="modal-title fs-5 w-100">
            <slot name="title"></slot>
          </h1>
          <button class="btn-close" type="button" @click="closeModal"></button>
        </div>
        <div class="modal-body">
          <slot name="body"></slot>
        </div>
        <div class="modal-footer">
          <slot name="footer"></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal.show.d-block {
  display: block;
  background-color: rgba(0, 0, 0, 0.5);
}
</style>

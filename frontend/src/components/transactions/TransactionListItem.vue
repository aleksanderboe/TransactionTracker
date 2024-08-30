<script setup>
defineProps({
  transaction: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['edit'])

import { useCurrencyFormatter } from '@/composables/currencyFormatter.js'
const formatUSD = useCurrencyFormatter()
</script>

<template>
  <li
    v-if="transaction"
    @click="emit('edit', transaction)"
    class="list-group-item card p-4 mb-4 shadow-sm border-0 rounded-3 clickable"
  >
    <div class="d-flex justify-content-between align-items-center">
      <div>
        <div class="h4 mb-2 fw-bold">{{ transaction?.description }}</div>
        <div class="text-muted fs-5 mb-2">
          {{ transaction.date_created }}
        </div>
      </div>
      <div class="d-flex align-items-center">
        <div class="text-end me-3">
          <p class="h4 mb-2">{{ transaction?.amount ? formatUSD.format(transaction.amount) : '' }}</p>
          <span class="badge fs-5" :style="{ backgroundColor: transaction?.category?.color || '#000' }">
            {{ transaction?.category?.name || 'Uncategorized' }}
          </span>
        </div>
      </div>
    </div>
  </li>
</template>

<style scoped>
.clickable {
  cursor: pointer;
  transition: filter 0.3s ease;
}

.clickable:hover {
  filter: brightness(0.95);
}
</style>

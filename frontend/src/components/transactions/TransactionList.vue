<script setup>
import { ref, computed, watch } from 'vue'
import TransactionListItem from './TransactionListItem.vue'

const props = defineProps({
  transactions: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['edit'])

const handleEdit = (transaction) => {
  emit('edit', transaction)
}

const currentPage = ref(1)
const itemsPerPage = 3

const totalPages = computed(() => {
  const fullPages = Math.floor(props.transactions.length / itemsPerPage)
  const remainder = props.transactions.length % itemsPerPage
  return remainder > 0 ? fullPages + 1 : fullPages
})

const paginatedTransactions = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return props.transactions.slice(start, end)
})

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

watch(
  () => props.transactions,
  () => {
    if (currentPage.value > totalPages.value) {
      currentPage.value = totalPages.value
    }
    if (currentPage.value === 0 && totalPages.value > 0) {
      currentPage.value = 1
    }
  },
  { immediate: true }
)
</script>

<template>
  <div>
    <div v-if="props.transactions.length">
      <ul class="list-group list-group-flush">
        <TransactionListItem
          v-for="transaction in paginatedTransactions"
          :key="transaction.id"
          :transaction="transaction"
          @edit="handleEdit"
        />
      </ul>
      <nav v-if="totalPages > 1" aria-label="Page navigation" class="mt-3">
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="prevPage" :disabled="currentPage === 1">Previous</button>
          </li>
          <li
            v-for="page in totalPages"
            :key="page"
            class="page-item"
            :class="{ active: currentPage === page }"
          >
            <button class="page-link" @click="currentPage = page">{{ page }}</button>
          </li>
          <li class="page-item" :class="{ disabled: currentPage === totalPages.value }">
            <button class="page-link" @click="nextPage" :disabled="currentPage === totalPages.value">Next</button>
          </li>
        </ul>
      </nav>
    </div>
    <div v-else class="alert alert-info" role="alert">There are no transactions to display.</div>
  </div>
</template>

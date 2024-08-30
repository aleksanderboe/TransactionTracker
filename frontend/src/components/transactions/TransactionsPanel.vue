<script setup>
import { ref, onMounted, computed, watch } from 'vue'

import TransactionList from './TransactionList.vue'
import TransactionModal from './TransactionModal.vue'
import TransactionCategoryModal from './TransactionCategoryModal.vue'

import { useTransactionStore } from '@/stores/transactions'
import { useCategoryStore } from '@/stores/categories'

const transactionStore = useTransactionStore()
const categoryStore = useCategoryStore()

onMounted(() => {
  transactionStore.fetchTransactions()
  categoryStore.fetchCategories()
})

const showTransactionModal = ref(false)
const showCategoryModal = ref(false)

const selectedTransaction = ref(null)

const editTransaction = (transaction) => {
  selectedTransaction.value = transaction
  showTransactionModal.value = true
}

const onTransactionModalClose = () => {
  showTransactionModal.value = false
  selectedTransaction.value = null
}

const searchText = ref(localStorage.getItem('searchText') || '')

const filteredTransactions = computed(() => {
  if (!transactionStore.transactions) {
    return []
  }

  if (!searchText.value) {
    return transactionStore.transactions
  }

  const searchLowerCase = searchText.value.toLowerCase()

  return transactionStore.transactions.filter((transaction) => {
    const description = transaction.description || ''
    return description.toLowerCase().includes(searchLowerCase)
  })
})

watch(
  () => searchText.value,
  (newValue) => {
    localStorage.setItem('searchText', newValue)
  }
)
</script>

<template>
  <TransactionCategoryModal
    v-show="showCategoryModal"
    @close="showCategoryModal = false"
  ></TransactionCategoryModal>
  <TransactionModal
    v-show="showTransactionModal"
    @close="onTransactionModalClose"
    :transactionToEdit="selectedTransaction"
  ></TransactionModal>

  <div class="container">
    <h2 class="h2">Transactions</h2>
    <div class="d-flex gap-2">
      <div class="dropdown mb-3">
        <button
          class="btn btn-success dropdown-toggle w-100"
          type="button"
          id="dropdownMenuButton"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <i class="bi-plus-lg"></i> New
        </button>
        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
          <li>
            <a class="dropdown-item" href="#" @click.prevent="showTransactionModal = true">
              Transaction
            </a>
          </li>
          <li>
            <a class="dropdown-item" href="#" @click.prevent="showCategoryModal = true">
              Category
            </a>
          </li>
        </ul>
      </div>
      <input
        type="text"
        class="form-control mb-4 w-25"
        placeholder="Search..."
        v-model="searchText"
      />
    </div>
    <TransactionList :transactions="filteredTransactions" @edit="editTransaction" />
  </div>
</template>

<style scoped></style>

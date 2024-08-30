<script setup>
import ModalDialog from '../ui/ModalDialog.vue'
import AlertBox from '../ui/AlertBox.vue'

import { ref, watch } from 'vue'
import { useTransactionStore } from '@/stores/transactions'
import { useCategoryStore } from '@/stores/categories'

const transactionStore = useTransactionStore()
const categoryStore = useCategoryStore()

const errorMessage = ref('')
const isLoading = ref(false)

const amount = ref('')
const type = ref('expense')
const description = ref('')
const category_id = ref('')
const date = ref(new Date().toISOString().substring(0, 10))

const setDefaultValues = () => {
  amount.value = ''
  type.value = 'expense'
  description.value = ''
  category_id.value = ''
  date.value = new Date().toISOString().substring(0, 10)
}

const emit = defineEmits(['close'])

const props = defineProps({
  transactionToEdit: Object
})

const isEditMode = ref(false)

watch(
  () => props.transactionToEdit,
  (newValue) => {
    if (newValue) {
      amount.value = newValue.amount
      description.value = newValue.description
      category_id.value = newValue.category ? newValue.category.id : null 
      type.value = newValue.type
      date.value = newValue.date_created
      isEditMode.value = true
    } else {
      setDefaultValues()
      isEditMode.value = false
    }
  },
  { immediate: true }
)

const handleSubmit = async () => {
  isLoading.value = true

  try {
    if (isEditMode.value) {
      await transactionStore.updateTransaction(
        props.transactionToEdit.id,
        amount.value,
        description.value,
        category_id.value,
        type.value,
        date.value
      )
    } else {
      await transactionStore.addTransaction(
        amount.value,
        description.value,
        category_id.value,
        type.value,
        date.value
      )
    }
    await transactionStore.fetchTransactions()
    emit('close')
    setDefaultValues()
  } catch (error) {
    errorMessage.value = error.response?.data.message ? error.response.data.message : error.message
  } finally {
    isLoading.value = false
  }
}

const handleDelete = async () => {
  isLoading.value = true
  try {
    await transactionStore.deleteTransaction(props.transactionToEdit.id)
    await transactionStore.fetchTransactions()
    emit('close')
  } catch (error) {
    errorMessage.value = error.response?.data.message ? error.response.data.message : error.message
  } finally {
    isLoading.value = false
  }
}

const handleClose = () => {
  emit('close')
  setDefaultValues()
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <ModalDialog @close="handleClose">
      <template #title>{{ isEditMode ? 'Edit Transaction' : 'Add Transaction' }}</template>
      <template #body>
        <AlertBox :message="errorMessage" class="mb-3"></AlertBox>
        <div class="btn-group mb-3 w-100" role="group">
          <input
            type="radio"
            class="btn-check"
            value="expense"
            v-model="type"
            id="expense"
            name="type"
          />
          <label for="expense" class="btn btn-outline-dark">Expense</label>

          <input
            type="radio"
            class="btn-check"
            value="income"
            v-model="type"
            id="income"
            name="type"
          />
          <label for="income" class="btn btn-outline-dark">Income</label>
        </div>

        <div class="form-floating mb-3">
          <input
            type="number"
            class="form-control"
            id="amount"
            name="amount"
            placeholder="amount"
            v-model="amount"
            required
          />
          <label for="amount">Amount</label>
        </div>
        <div class="form-floating mb-3">
          <input
            type="text"
            class="form-control"
            id="description"
            name="description"
            placeholder="description"
            v-model="description"
            required
          />
          <label for="description">Description</label>
        </div>
        <div class="form-floating mb-3">
          <select
            class="form-select"
            name="category"
            id="category"
            placeholder="category"
            v-model="category_id"
            required
          >
            <option disabled value="">Select a category</option>
            <option
              v-for="category in categoryStore.categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
          <label for="category">Category</label>
        </div>
        <div class="form-floating">
          <input
            type="date"
            class="form-control"
            id="date"
            name="date"
            placeholder="Date"
            v-model="date"
          />
          <label for="date">Date</label>
        </div>
      </template>
      <template #footer>
        <template v-if="isEditMode">
          <button @click="handleSubmit" type="button" class="btn btn-dark w-100">
            <span v-if="isLoading" class="spinner-border spinner-border-sm"></span>
            {{ isLoading ? '' : 'Save Changes' }}
          </button>
          <button @click="handleDelete" type="button" class="btn btn-danger w-100">
            <span v-if="isLoading" class="spinner-border spinner-border-sm"></span>
            {{ isLoading ? '' : 'Delete' }}
          </button>
        </template>
        <button v-else type="submit" class="btn btn-dark w-100" :disabled="isLoading">
          <span v-if="isLoading" class="spinner-border spinner-border-sm"></span>
          {{ isLoading ? '' : 'Add Transaction' }}
        </button>
      </template>
    </ModalDialog>
  </form>
</template>

<style scoped></style>

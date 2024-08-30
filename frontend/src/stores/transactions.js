import { defineStore } from 'pinia'
import axios from 'axios'
import { ref, computed } from 'vue'

export const useTransactionStore = defineStore('transactions', () => {
  const transactions = ref([])

  const fetchTransactions = async () => {
    const path = '/transactions'
    const res = await axios.get(path, {
      headers: { Authorization: `Bearer ${localStorage.getItem('jwt')}` }
    })

    if (res.status >= 200 && res.status < 300) {
      transactions.value = res.data.data
    }
  }

  const deleteTransaction = async (transaction_id) => {
    const path = `/transactions/${transaction_id}`
    const res = await axios.delete(path, {
      headers: { Authorization: `Bearer ${localStorage.getItem('jwt')}` }
    })

    if (res.status >= 200 && res.status < 300) {
      transactions.value = transactions.value.filter(
        (transaction) => transaction.id !== transaction_id
      )
    }
  }

  const updateTransaction = async (
    transaction_id,
    amount,
    description,
    category_id,
    type,
    date
  ) => {
    await axios.put(
      `/transactions/${transaction_id}`,
      { amount, description, category_id, type, date },
      { headers: { Authorization: `Bearer ${localStorage.getItem('jwt')}` } }
    )
  }

  const addTransaction = async (amount, description, category_id, type, date) => {
    await axios.post(
      '/transactions',
      {
        amount,
        description,
        category_id,
        type,
        date
      },
      {
        headers: { Authorization: `Bearer ${localStorage.getItem('jwt')}` }
      }
    )
  }

  const totalAmount = computed(() => (type) => {
    if (transactions.value.length) {
      return transactions.value
        .filter((transaction) => transaction.type === type)
        .reduce((acc, transaction) => acc + transaction.amount, 0)
    } else {
      return 0
    }
  })

  const totalCount = computed(() => () => transactions.value.length)

  const getTransactionsByType = computed(() => {
    return (type) => transactions.value.filter((transaction) => transaction.type === type)
  })

  return {
    transactions,
    fetchTransactions,
    getTransactionsByType,
    deleteTransaction,
    updateTransaction,
    addTransaction,
    totalAmount,
    totalCount
  }
})

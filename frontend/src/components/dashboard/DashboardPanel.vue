<script setup>
import { onMounted, computed } from 'vue'

import DashboardCard from '@/components/dashboard/DashboardCard.vue'
import DashboardDoughnutChart from '@/components/dashboard/DashboardDoughnutChart.vue'
import DashboardLineChart from '@/components/dashboard/DashboardLineChart.vue'

import { useTransactionStore } from '@/stores/transactions'
const transactionStore = useTransactionStore()

onMounted(() => {
  transactionStore.fetchTransactions()
})

import { useCurrencyFormatter } from '@/composables/currencyFormatter.js'
const formatUSD = useCurrencyFormatter()

const transactionsCount = computed(() => transactionStore.totalCount())
const income = computed(() => formatUSD.format(transactionStore.totalAmount('income')))
const expense = computed(() => formatUSD.format(transactionStore.totalAmount('expense')))
const balance = computed(() =>
  formatUSD.format(transactionStore.totalAmount('income') - transactionStore.totalAmount('expense'))
)

const expenses = computed(() => transactionStore.getTransactionsByType('expense'))
const incomes = computed(() => transactionStore.getTransactionsByType('income'))
</script>

<template>
  <div class="container">
    <h2>Dashboard</h2>
    <div class="row g-4">
      <div class="col-sm-6 col-lg-3">
        <DashboardCard
          icon="bi bi-bank"
          icon-bg-color="bg-primary-subtle"
          icon-color="text-primary"
          title="Balance"
          :value="balance"
        ></DashboardCard>
      </div>
      <div class="col-sm-6 col-lg-3">
        <DashboardCard
          icon="bi bi-cash"
          icon-bg-color="bg-success-subtle"
          icon-color="text-success"
          title="Income"
          :value="income"
        ></DashboardCard>
      </div>

      <div class="col-sm-6 col-lg-3">
        <DashboardCard
          icon="bi bi-wallet2"
          icon-bg-color="bg-danger-subtle"
          icon-color="text-danger"
          title="Expense"
          :value="expense"
        ></DashboardCard>
      </div>
      <div class="col-sm-6 col-lg-3">
        <DashboardCard
          icon="bi bi-list-check"
          icon-bg-color="bg-warning-subtle"
          icon-color="text-warning"
          title="Transactions"
          :value="transactionsCount"
        ></DashboardCard>
      </div>

      <div class="col-lg-6">
        <div class="card h-auto shadow-sm border-0" style="max-height: 400px">
          <div class="card-body d-flex justify-content-center align-items-center">
            <DashboardDoughnutChart :expenses="expenses" class="w-100" />
          </div>
        </div>
      </div>
      <div class="col-lg-6">
        <div class="card h-auto shadow-sm border-0" style="max-height: 400px">
          <div class="card-body d-flex justify-content-center align-items-center">
            <DashboardLineChart :expenses="expenses" :incomes="incomes" class="w-100" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>

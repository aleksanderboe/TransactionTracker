<script setup>
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line } from 'vue-chartjs'
import { computed } from 'vue'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

const props = defineProps({ expenses: Array, incomes: Array })

const monthlyTotals = (items) => {
  const totals = new Array(12).fill(0)
  items.forEach((item) => {
    if (item.date_created) {
      const monthIndex = new Date(item.date_created).getMonth()
      totals[monthIndex] += item.amount
    }
  })
  return totals
}

const incomeData = computed(() => monthlyTotals(props.incomes))
const expenseData = computed(() => monthlyTotals(props.expenses))

const data = computed(() => ({
  labels: [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
  ],
  datasets: [
    {
      label: 'Income',
      backgroundColor: 'rgba(76, 168, 100, 0.5)',
      borderColor: '#4ca864',
      data: incomeData.value,
      fill: false,
      tension: 0.1
    },
    {
      label: 'Expense',
      backgroundColor: 'rgba(202, 74, 74, 0.5)',
      borderColor: '#ca4a4a',
      data: expenseData.value,
      fill: false,
      tension: 0.1
    }
  ]
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true
    }
  },
  plugins: {
    legend: {
      display: true,
      labels: {
        font: {
          size: 20
        }
      }
    },
    tooltip: {
      mode: 'index',
      intersect: false
    }
  }
}
</script>

<template>
  <Line :data="data" :options="options" style="max-height: 300px" />
</template>

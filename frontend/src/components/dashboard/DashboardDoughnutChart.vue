<script setup>
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'vue-chartjs'
import { computed } from 'vue'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({ expenses: { type: Array } })

const sumsByCategory = computed(() => {
  return props.expenses?.reduce((acc, item) => {
    const categoryName = item.category?.name;
    const categoryColor = item.category?.color;

    if (categoryName) {
      if (acc[categoryName]) {
        acc[categoryName].amount += item.amount;
      } else {
        acc[categoryName] = { amount: item.amount, color: categoryColor || '#000' };
      }
    } else {
      if (acc['Uncategorized']) {
        acc['Uncategorized'].amount += item.amount;
      } else {
        acc['Uncategorized'] = { amount: item.amount, color: '#000' };
      }
    }

    return acc;
  }, {});
});


const chartData = computed(() => {
  const labels = []
  const backgroundColors = []
  const data = []

  for (const [category, info] of Object.entries(sumsByCategory.value)) {
    labels.push(category)
    backgroundColors.push(info.color)
    data.push(info.amount)
  }

  return {
    labels: labels,
    datasets: [
      {
        backgroundColor: backgroundColors,
        data: data
      }
    ]
  }
})

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
      labels: {
        usePointStyle: true,
        pointStyle: 'circle',
        boxWidth: 50,
        font: {
          size: 20
        },
        padding: 20
      }
    }
  }
}
</script>

<template>
  <Doughnut :data="chartData" :options="options" style="max-height: 300px" />
</template>

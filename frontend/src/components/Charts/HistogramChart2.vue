<template>
  <div class="chart-card">
    <div class="chart-header flex justify-between items-center">
      <h3 class="inline-flex items-center gap-2" v-html="title"></h3>
      <ToggleQuestionMark :explanation="explanationText" />
    </div>
    <div class="chart-body w-full">
      <canvas ref="histogramCanvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue';
import ToggleQuestionMark from "../Reusable/ToggleQuestionMark.vue";
import { chartTheme } from './../../assets/chartTheme';

import {
  Chart,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
} from 'chart.js';

Chart.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);

const props = defineProps({
  title: { type: String, default: 'Histogram' },
  xAxisLabel: { type: String, default: 'X Axis' },
  yAxisLabel: { type: String, default: 'Y Axis' },
  data: {
    type: Object,
    required: true,
    validator: v => v?.labels && v?.datasets
  }
});

const histogramCanvas = ref(null);
const chartInstance = ref(null);

onMounted(() => {
  if (!props.data) return;

  chartInstance.value = new Chart(histogramCanvas.value, {
    type: 'bar',
    data: {
      ...props.data,
      datasets: props.data.datasets.map(ds => ({
        ...ds,
        backgroundColor: ds.backgroundColor || chartTheme.colors.primary,
        borderColor: ds.borderColor || chartTheme.colors.secondary,
        borderWidth: 1
      }))
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          labels: { color: chartTheme.defaults.legendColor }
        },
        tooltip: {
          enabled: true,
          backgroundColor: '#ffffff',
          titleColor: chartTheme.defaults.textColor,
          bodyColor: chartTheme.defaults.textColor
        }
      },
      scales: {
        x: { grid: { display: false } },
        y: { grid: { color: chartTheme.defaults.gridlineColor } }
      }
    }
  });
});

watch(
  () => props.data,
  (newData) => {
    if (!newData) return;

    // Destroy previous chart if exists
    if (chartInstance.value) {
      chartInstance.value.destroy();
    }

    // Create a new chart with updated data
    chartInstance.value = new Chart(histogramCanvas.value, {
      type: 'bar',
      data: {
        ...newData,
        datasets: newData.datasets.map(ds => ({
          ...ds,
          backgroundColor: ds.backgroundColor || chartTheme.colors.primary,
          borderColor: ds.borderColor || chartTheme.colors.secondary,
          borderWidth: 1
        }))
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            labels: { color: chartTheme.defaults.legendColor }
          },
          tooltip: {
            enabled: true,
            backgroundColor: '#ffffff',
            titleColor: chartTheme.defaults.textColor,
            bodyColor: chartTheme.defaults.textColor
          }
        },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: chartTheme.defaults.gridlineColor } }
        }
      }
    });
  },
  { deep: true }
);

onBeforeUnmount(() => {
  chartInstance.value?.destroy();
});
</script>

<style scoped>
.chart-card {
  background: #ffffff;
  border: 1px solid #e6e6e6;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.chart-header h3 {
  margin: 0 0 16px;
  font-size: 18px;
  font-weight: 600;
}

.chart-body {
  position: relative;
  height: 300px;
}

.chart-body canvas {
  max-height: 100%;
}
</style>



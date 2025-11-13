<template>
  <div class="key-metrics grid grid-cols-3 gap-4">
    <!-- Class Overview Cards -->
    <div
      v-for="c in classOverviewData"
      :key="c.classId"
      class="metric-card bg-white shadow rounded p-4 flex items-center justify-between cursor-pointer" 
      @click="goToClass(c)"  
    >
      <div class="flex items-center">
        <div class="icon bg-blue-100 text-blue-500 p-2 rounded-full mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4h16v16H4z" />
          </svg>
        </div>
        <div>
          <p class="text-lg font-semibold">{{ c.classId }}</p>
          <ul class="text-sm text-blue-500">
            <li>Instances: {{ c.instances }}</li>
            <li>Violations: {{ c.violations }}</li>
            <li>Satisfaction Rate: {{ c.satisfaction }}%</li>
          </ul>
        </div>
      </div>
      <div class="sparkline">
        <sparkline-chart :data="[7, 1, 10, 5]" color="blue" />
      </div>
    </div>
  </div>
</template>

<script setup>
import SparklineChart from '../Charts/SparklineChart.vue'
import { useRouter } from 'vue-router'  

const router = useRouter()              

const classOverviewData = [
  { classId: 'dbo:StadiumShape', instances: 120, violations: 25, satisfaction: 80 },
  { classId: 'dbo:ComicStripShape', instances: 98, violations: 12, satisfaction: 88 },
  { classId: 'dbo:AmphibianShape', instances: 76, violations: 8, satisfaction: 90 }
]

const goToClass = (c) => {
  router.push({ name: 'ClassDetailedView', params: { classId: c.classId } })
}
</script>

<style scoped>
.key-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.metric-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-radius: 0.5rem;
  background-color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s; 
}
.metric-card:hover {
  transform: scale(1.02);
}

.icon {
  flex-shrink: 0;
}

.sparkline {
  width: 100px;
  height: 40px;
}
</style>

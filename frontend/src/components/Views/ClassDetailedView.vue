<template>
  <div class="class-view p-4">
    <button @click="goBack" class="bg-blue-500 text-white px-4 py-2 rounded mb-4">
      Back to Overview
    </button>

    <!-- Header -->
    <div class="header-section mb-6">
      <h1 class="text-2xl font-bold mb-2 text-primary">Class: {{ className }}</h1>
      <div class="header-content flex justify-between items-center bg-gray-100 p-4 rounded">
        <div>
          <p class="font-medium">Total Instances:</p>
          <span class="text-blue-600 font-semibold">{{ totalInstances }}</span>
        </div>
        <div>
          <p class="font-medium">
            Total Violations:
            <span class="text-red-500 font-bold">{{ totalViolations }}</span>
          </p>
        </div>
        <div>
          <p class="font-medium">Satisfaction Rate:</p>
          <span class="text-green-500 font-semibold">{{ satisfactionRate }}%</span>
        </div>
      </div>
    </div>

    <!-- Metric Sections -->
    <div class="main-content space-y-6">
      <div class="key-metrics grid grid-cols-2 gap-4">
        <!-- Violations per Instance -->
        <div class="metric-card bg-white shadow rounded p-4 flex flex-col justify-between">
          <h3 class="text-lg font-semibold mb-2">Violations per Instance</h3>
          <BarChart
            :title="'Violations per Instance'"
            :xAxisLabel="'Instances'"
            :yAxisLabel="'Violations'"
            :data="violationDistributionData"
          />
        </div>

        <!-- Constraint Satisfaction -->
        <div class="metric-card bg-white shadow rounded p-4 flex flex-col justify-between">
          <h3 class="text-lg font-semibold mb-2">Constraint Satisfaction</h3>
          <BarChart
            :title="'Constraint Satisfaction'"
            :xAxisLabel="'Type'"
            :yAxisLabel="'%'"
            :data="constraintSatisfactionData"
          />
        </div>
      </div>

      <!-- Example Instances -->
      <div class="metric-card bg-white shadow rounded p-4">
        <h3 class="text-lg font-semibold mb-3">Example Instances</h3>
        <ul class="text-sm text-blue-500">
          <li v-for="(ex, i) in exampleInstances" :key="i">
            {{ ex.node }} --> {{ ex.property }}: {{ ex.value }}
          </li>
        </ul>
      </div>

      <!-- Constraint Definitions -->
      <div class="metric-card bg-white shadow rounded p-4">
        <h3 class="text-lg font-semibold mb-3">Constraint Definitions</h3>
        <ul class="text-sm text-blue-500">
          <li v-for="(def, i) in constraintDefinitions" :key="i">{{ def }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BarChart from './../Charts/BarChart.vue'

const route = useRoute()
const router = useRouter()

const className = ref('')
const totalInstances = ref(120)
const totalViolations = ref(25)
const satisfactionRate = ref(72)

const violationDistributionData = ref({
  labels: ['Instance 1', 'Instance 2', 'Instance 3', 'Instance 4'],
  datasets: [
    {
      label: 'Violations',
      data: [2, 6, 5, 18],
      backgroundColor: 'rgba(30, 136, 229, 0.7)',
      borderColor: 'rgba(30, 136, 229, 1)',
      borderWidth: 1
    }
  ]
})

const constraintSatisfactionData = ref({
  labels: ['Satisfied', 'Violated'],
  datasets: [
    {
      label: 'Satisfaction',
      data: [72, 28],
      backgroundColor: ['rgba(33, 150, 243, 0.7)', 'rgba(13, 71, 161, 0.7)'],
      borderColor: ['rgba(33, 150, 243, 1)', 'rgba(13, 71, 161, 1)'],
      borderWidth: 1
    }
  ]
})

const exampleInstances = ref([
  { node: 'ex:Stadium1', property: 'dbo:capacity', value: '60000' },
  { node: 'ex:Stadium2', property: 'dbo:location', value: 'London' },
  { node: 'ex:Stadium3', property: 'dbo:team', value: 'Chelsea FC' }
])

const constraintDefinitions = ref([
  'sh:minCount --> Each instance must have at least one label',
  'sh:datatype --> Must be xsd:string',
  'sh:maxCount --> No more than 3 values allowed',
  'sh:class --> Must belong to dbo:Place'
])

onMounted(() => {
  const classId = route.params.classId
  if (classId) className.value = classId
})

const goBack = () => {
  router.push({ name: 'ClassOverview' })
}
</script>

<style scoped>
.metric-card {
  background-color: white;
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.text-primary {
  color: #1565c0;
}
</style>

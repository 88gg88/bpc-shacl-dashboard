<template>
  <div class="class-view p-4">
    <button @click="goBack" class="bg-blue-500 text-white px-4 py-2 rounded mb-4">
      Back to Overview
    </button>

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

    <div class="main-content space-y-6">
      <div class="key-metrics grid grid-cols-3 gap-4">
        <div class="plot bg-gray-100 p-4 rounded">
          <h3 class="text-md font-medium">1. Violations per Instance</h3>
          <BarChart
            :title="'Violations per Instance'"
            :xAxisLabel="'Instances'"
            :yAxisLabel="'Violations'"
            :data="violationDistributionData"
          />
        </div>

        <div class="plot bg-gray-100 p-4 rounded">
          <h3 class="text-md font-medium">2. Constraint Satisfaction</h3>
          <BarChart
            :title="'Constraint Satisfaction'"
            :xAxisLabel="'State'"
            :yAxisLabel="'%'"
            :data="constraintSatisfactionData"
          />
        </div>

        <div class="plot bg-gray-100 p-4 rounded">
          <h3 class="text-md font-medium">3. Example Instances</h3>
          <table class="table-auto w-full text-left border-collapse border border-gray-300">
            <thead class="bg-gray-200">
              <tr>
                <th class="border border-gray-300 px-4 py-2">Node</th>
                <th class="border border-gray-300 px-4 py-2">Property</th>
                <th class="border border-gray-300 px-4 py-2">Value</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(ex, i) in exampleInstances" :key="i" class="hover:bg-gray-50">
                <td class="border border-gray-300 px-4 py-2">{{ ex.node }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ ex.property }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ ex.value }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="bottom-section bg-gray-100 p-4 rounded mt-6">
        <h2 class="text-lg font-semibold mb-4">Constraint Definitions</h2>

        <table class="table-auto w-full text-left border-collapse border border-gray-300">
          <thead class="bg-gray-200">
            <tr>
              <th class="border border-gray-300 px-4 py-2">Constraint</th>
              <th class="border border-gray-300 px-4 py-2">Meaning</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(def, i) in constraintDefinitions" :key="i" class="hover:bg-gray-50">
              <td class="border border-gray-300 px-4 py-2">{{ def.constraint }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ def.meaning }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="bottom-section bg-gray-100 p-4 rounded mt-6">
        <h2 class="text-lg font-semibold mb-4">List of Violations</h2>

        <table class="table-auto w-full text-left border-collapse border border-gray-300">
          <thead class="bg-gray-200">
            <tr>
              <th class="border border-gray-300 px-4 py-2">Instance</th>
              <th class="border border-gray-300 px-4 py-2">Property</th>
              <th class="border border-gray-300 px-4 py-2">Constraint</th>
              <th class="border border-gray-300 px-4 py-2">Message</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="v in violations"
              :key="v.id"
              class="hover:bg-gray-50"
            >
              <td class="border border-gray-300 px-4 py-2">{{ v.instance }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ v.property }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ v.constraint }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ v.message }}</td>
            </tr>
          </tbody>
        </table>
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
  labels: ['1', '2', '3', '4'],
  datasets: [
    {
      label: 'Violations',
      data: [2, 6, 5, 18],
      backgroundColor: ['rgba(54,162,235,0.2)'],
      borderColor: ['rgba(54,162,235,1)'],
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
      backgroundColor: ['rgba(54,162,235,0.2)'],
      borderColor: ['rgba(54,162,235,1)'],
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
  { constraint: 'sh:minCount', meaning: 'Each instance must have at least one label' },
  { constraint: 'sh:datatype', meaning: 'Must be xsd:string' },
  { constraint: 'sh:maxCount', meaning: 'No more than 3 values allowed' },
  { constraint: 'sh:class', meaning: 'Must belong to dbo:Place' }
])

const violations = ref([
  { id: 1, instance: '1', property: 'dbo:capacity', constraint: 'sh:minCount', message: 'Missing required value' },
  { id: 2, instance: '2', property: 'dbo:location', constraint: 'sh:datatype', message: 'Invalid datatype' },
  { id: 3, instance: '3', property: 'dbo:team', constraint: 'sh:maxCount', message: 'Too many values' },
  { id: 4, instance: '4', property: 'dbo:capacity', constraint: 'sh:class', message: 'Wrong class type' }
])

onMounted(() => {
  const id = route.params.classId
  if (id) className.value = id
})

const goBack = () => {
  router.push({ name: 'ClassOverview' })
}
</script>

<style scoped>
.text-primary { color: #1565c0; }
</style>

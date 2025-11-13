<template>
  <div class="propertypath-view p-4">
    <button @click="goBack" class="bg-blue-500 text-white px-4 py-2 rounded mb-4">
      Back to Overview
    </button>

    <div class="header-section mb-6">
      <h1 class="text-2xl font-bold mb-2 text-primary">Property Path: {{ propertyPath }}</h1>
      <div class="header-content flex justify-between items-center bg-gray-100 p-4 rounded">
        <div>
          <p class="font-medium">Path Type:</p>
          <span class="text-green-500 font-semibold">{{ pathType }}</span>
        </div>
        <div>
          <p class="font-medium">
            Total Violations:
            <span class="text-red-500 font-bold">{{ totalViolations }}</span>
          </p>
        </div>
      </div>
    </div>
<div class="main-content space-y-6">

      <div class="key-metrics grid grid-cols-3 gap-4">
        <div class="plot bg-gray-100 p-4 rounded">
          <h3 class="text-md font-medium">1. Path Occurrence Frequency</h3>

          <table class="table-auto w-full text-left border-collapse border border-gray-300">
            <thead class="bg-gray-200">
              <tr>
                <th class="border border-gray-300 px-4 py-2">Shape</th>
                <th class="border border-gray-300 px-4 py-2">Occurrences</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, i) in occurrenceTable" :key="i" class="hover:bg-gray-50">
                <td class="border border-gray-300 px-4 py-2">{{ row.shape }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ row.count }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="plot bg-gray-100 p-4 rounded">
          <h3 class="text-md font-medium">2. Distribution of Violations</h3>
          <BarChart
            :title="'Violation Distribution'"
            :xAxisLabel="'Focus Nodes'"
            :yAxisLabel="'Number of Violations'"
            :data="violationDistributionData"
          />
        </div>

        <div class="plot bg-gray-100 p-4 rounded">
          <h3 class="text-md font-medium">3. Example Triples</h3>

          <table class="table-auto w-full text-left border-collapse border border-gray-300">
            <thead class="bg-gray-200">
              <tr>
                <th class="border border-gray-300 px-4 py-2">Shape</th>
                <th class="border border-gray-300 px-4 py-2">Constraint</th>
                <th class="border border-gray-300 px-4 py-2">Count</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, i) in exampleTriples" :key="i" class="hover:bg-gray-50">
                <td class="border border-gray-300 px-4 py-2">{{ row.shape }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ row.constraint }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ row.count }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="plots-section grid grid-cols-3 gap-4">
        <div class="plot bg-gray-100 p-4 rounded">
          <h3 class="text-md font-medium">4. Path Type Breakdown</h3>
          <BarChart
            :title="'Path Type Breakdown'"
            :xAxisLabel="'Property Path Types'"
            :yAxisLabel="'Violations'"
            :data="pathTypeData"
          />
        </div>

        <div class="plot bg-gray-100 p-4 rounded">
          <h3 class="text-md font-medium">5. Violation Examples</h3>

          <table class="table-auto w-full text-left border-collapse border border-gray-300">
            <thead class="bg-gray-200">
              <tr>
                <th class="border border-gray-300 px-4 py-2">Focus Node</th>
                <th class="border border-gray-300 px-4 py-2">Message</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(v, i) in violationExamplesData" :key="i" class="hover:bg-gray-50">
                <td class="border border-gray-300 px-4 py-2">{{ v.focusNode }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ v.message }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div></div>
      </div>

      <div class="bottom-section bg-gray-100 p-4 rounded mt-6">
        <h2 class="text-lg font-semibold mb-4">List of Violations</h2>

        <table class="table-auto w-full text-left border-collapse border border-gray-300">
          <thead class="bg-gray-200">
            <tr>
              <th class="border border-gray-300 px-4 py-2">Focus Node</th>
              <th class="border border-gray-300 px-4 py-2">Property Path</th>
              <th class="border border-gray-300 px-4 py-2">Constraint</th>
              <th class="border border-gray-300 px-4 py-2">Message</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="v in violations" :key="v.id" class="hover:bg-gray-50">
              <td class="border border-gray-300 px-4 py-2">{{ v.focusNode }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ v.propertyPath }}</td>
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
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import BarChart from './../Charts/BarChart.vue'
import ViolationExamplesChart from './../Charts/ViolationExamplesChart.vue'
const route = useRoute()
const router = useRouter()

const propertyPath = ref("")
const pathType = ref("")
const totalViolations = ref(0)

const occurrenceTable = ref([
  { shape: 'shs:StadiumShape', count: 3 },
  { shape: 'shs:AmphibianShape', count: 2 },
  { shape: 'shs:ComicStripShape', count: 4 }
])

const exampleTriples = ref([
  { shape: 'shs:StadiumShape', constraint: 'sh:InConstraintComponent', count: 2379 },
  { shape: 'shs:AmphibianShape', constraint: 'sh:InConstraintComponent', count: 729 },
  { shape: 'shs:ComicStripShape', constraint: 'sh:InConstraintComponent', count: 718 }
])

const violationDistributionData = ref({
  labels: ['Node 1', 'Node 2', 'Node 3'],
  datasets: [
    {
      label: 'Violations',
      data: [12, 5, 8],
      backgroundColor: ['rgba(54,162,235,0.2)'],
      borderColor: ['rgba(54,162,235,1)'],
      borderWidth: 1
    }
  ]
})

const pathTypeData = ref({
  labels: ['Datatype Property', 'Object Property', 'Annotation Property'],
  datasets: [
    {
      label: 'Violations',
      data: [10, 20, 5],
      backgroundColor: ['rgba(54,162,235,0.2)'],
      borderColor: ['rgba(54,162,235,1)'],
      borderWidth: 1
    }
  ]
})

const violationExamplesData = ref([
  { focusNode: "Node 1", message: "Missing value for foaf:age" },
  { focusNode: "Node 2", message: "Invalid datatype for foaf:name" }
])

const violations = ref([
  { id: 1, focusNode: "http://example.com/123", propertyPath: "foaf:age", constraint: "sh:minCount", message: "Min count not met" },
  { id: 2, focusNode: "http://example.com/456", propertyPath: "foaf:name", constraint: "sh:datatype", message: "Invalid datatype" }
])

onMounted(() => {
  const id = route.params.pathId
  const pathData = {
    1: { path: "book:hasAuthor", type: "IRI", violations: 10 },
    2: { path: "book:hasTitle", type: "Literal", violations: 5 },
    3: { path: "book:publishedBy", type: "IRI", violations: 2 }
  }[id]

  if (pathData) {
    propertyPath.value = pathData.path
    pathType.value = pathData.type
    totalViolations.value = pathData.violations
  }
})
const goBack = () => {
  router.push({ name: "PropertyPathOverview" })
}
</script>
<style scoped>
.text-primary { color: #1565c0; }
</style>

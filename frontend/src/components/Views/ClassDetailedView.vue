<template>
  <div class="class-detailed-view p-6 max-w-7xl mx-auto">
    <div class="header-section bg-gray-100 p-4 rounded mb-6 shadow flex items-center justify-between">
      <div>
        <button
          @click="goBack"
          class="px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 flex items-center gap-2"
        >
          Back to Class Overview
        </button>
      </div>

      <div class="flex flex-col items-center flex-grow text-center">
        <h1 class="text-2xl font-semibold text-gray-800">
          Class: {{ shorten(className) }}
        </h1>
        <button
          @click="showDefinition = !showDefinition"
          class="text-blue-600 text-sm mt-1 hover:underline"
        >
          {{ showDefinition ? "Hide Definition" : "Show Definition" }}
        </button>
      </div>

      <div class="w-[120px]"></div>
    </div>

    <transition name="fade">
      <section v-if="showDefinition" class="bg-gray-50 p-6 rounded-xl mb-8 shadow">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Active Constraint Types</h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <article
            v-for="def in constraintDefinitions"
            :key="def.constraint"
            class="flex items-center justify-between bg-white p-4 rounded-lg shadow-sm"
          >
            <div class="flex items-center gap-3">
              <code class="font-mono text-xs bg-gray-200 px-2 py-1 rounded">{{ def.constraint }}</code>
              <span class="text-gray-700">{{ constraintMeaning(def.constraint) }}</span>
            </div>
            <span class="text-gray-500 text-xs">{{ def.count ?? 0 }}x</span>
          </article>
        </div>
      </section>
    </transition>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
      <div class="summary-card">
        <h3 class="summary-title">Total Instances</h3>
        <p class="summary-value">{{ data.totalInstances ?? 0 }}</p>
      </div>

      <div class="summary-card">
        <div class="flex justify-between items-end">
          <div>
            <h3 class="summary-title">Instances with Violations</h3>
            <p class="summary-value text-red-600">{{ data.instancesWithViolations ?? 0 }}</p>
          </div>
          <div class="text-right">
            <p class="text-xs text-gray-500">most affected</p>
            <p class="text-lg font-semibold text-orange-600">
              {{ shorten(data.mostAffectedInstance) || "-" }}
            </p>
          </div>
        </div>
      </div>

      <div class="summary-card">
        <div class="flex justify-between items-end">
          <div>
            <h3 class="summary-title">Violated Properties</h3>
            <p class="summary-value">{{ data.violatedProperties ?? 0 }}</p>
          </div>
          <div class="text-right">
            <p class="text-xs text-gray-500">most violated path</p>
            <p class="text-lg font-semibold text-orange-600">
              {{ shorten(data.mostViolatedPath) || "-" }}
            </p>
          </div>
        </div>
      </div>

      <div class="summary-card">
        <div class="flex justify-between items-end">
          <div>
            <h3 class="summary-title">Constraints Triggered</h3>
            <p class="summary-value">{{ data.constraintsTriggered ?? 0 }}</p>
          </div>
          <div class="text-right">
            <p class="text-xs text-gray-500">most triggered</p>
            <p class="text-lg font-semibold text-orange-600">
              {{ shorten(data.mostTriggeredConstraint) || "-" }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
      <BarChart
        :title="'Violations per Instance'"
        :xAxisLabel="'Instances'"
        :yAxisLabel="'Violations'"
        :data="violationsPerInstanceChart"
      />

      <BarChart
        :title="'Violations per Property'"
        :xAxisLabel="'Properties'"
        :yAxisLabel="'Violations'"
        :data="violationsPerPropertyChart"
      />

      <BarChart
        :title="'Violations per Constraint Type'"
        :xAxisLabel="'Constraints'"
        :yAxisLabel="'Triggers'"
        :data="violationsPerConstraintChart"
      />
    </div>

    <div class="bg-white rounded-xl shadow-lg overflow-hidden">
      <div class="px-6 py-4 bg-gray-50 border-b">
        <h2 class="text-xl font-semibold text-gray-800">
          All Instances of <code class="text-blue-600 font-mono">{{ shorten(className) }}</code>
        </h2>
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-100">
            <tr>
              <th class="table-head">Instance</th>
              <th class="table-head">Violation Context</th>
              <th class="table-head">Violations</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-gray-200">
            <tr
              v-for="(inst, idx) in instances"
              :key="inst.node + '-' + idx"
              class="hover:bg-gray-50 transition"
            >
              <td class="px-6 py-4 align-top">
                <code class="text-sm font-medium text-blue-700">{{ shorten(inst.node) }}</code>
              </td>

              <td class="px-6 py-4 text-sm text-gray-700 align-top">
                <div v-if="inst.violations?.length" class="space-y-2">
                  <div
                    v-for="(v, vi) in inst.violations.slice(0, 3)"
                    :key="vi"
                    class="bg-gray-50 border rounded px-3 py-2"
                  >
                    <div class="text-xs">
                      <span class="font-semibold">path:</span>
                      <code class="ml-1">{{ shorten(v.path) || "-" }}</code>
                    </div>

                    <div class="text-xs" v-if="v.value || v.valueShort">
                      <span class="font-semibold">value:</span>
                      <span class="ml-1 text-gray-600">{{ v.valueShort || v.value }}</span>
                    </div>

                    <div class="text-xs" v-if="v.constraint">
                      <span class="font-semibold">constraint:</span>
                      <span class="ml-1 text-gray-600">{{ v.constraint }}</span>
                    </div>
                  </div>

                  <div v-if="inst.violations.length > 3" class="text-xs text-gray-400 italic">
                    + {{ inst.violations.length - 3 }} more...
                  </div>
                </div>
                <span v-else class="text-gray-400 italic">No violations</span>
              </td>

              <td class="px-6 py-4 text-sm align-top">
                <template v-if="inst.violations?.length">
                  <ul class="space-y-1">
                    <li v-for="(v, vi) in inst.violations.slice(0, 10)" :key="vi" class="text-xs">
                      <span class="font-medium text-red-700">{{ v.property }}</span>
                      <span class="text-gray-500 mx-1">-></span>
                      <span class="text-red-600">{{ v.message }}</span>
                      <span v-if="v.constraint" class="text-gray-400 ml-1">({{ v.constraint }})</span>
                    </li>
                  </ul>

                  <div v-if="inst.violations.length > 10" class="text-xs text-gray-400 italic mt-2">
                    + {{ inst.violations.length - 10 }} more...
                  </div>
                </template>
                <span v-else class="text-gray-400 italic">No violations</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import BarChart from "../Charts/BarChart.vue"
import axios from "axios"
import { ref, computed, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"

const route = useRoute()
const router = useRouter()

const className = ref("")
const showDefinition = ref(false)

const data = ref({})
const instances = ref([])
const constraintDefinitions = ref([])

const shorten = (iri) => {
  if (!iri) return ""
  return String(iri).split(/[\/#]/).pop()
}

const constraintMeaning = (c) => {
  const k = shorten(c)
  const meanings = {
    minCountConstraintComponent: "Property is required",
    maxCountConstraintComponent: "Maximum number of values",
    datatypeConstraintComponent: "Wrong datatype",
    classConstraintComponent: "Wrong class type",
    patternConstraintComponent: "Value does not match pattern",
  }
  return meanings[k] || "Constraint triggered"
}

onMounted(async () => {
  const id = route.params.classId
  className.value = id ? decodeURIComponent(String(id)) : "Unknown Class"

  const res = await axios.get("http://localhost:5001/api/class-view/details", {
    params: { class: className.value },
  })

  data.value = res.data || {}
  instances.value = res.data?.instances || []
  constraintDefinitions.value = res.data?.constraintDefinitions || []
})

const violationsPerInstanceChart = computed(() => ({
  labels: instances.value.map(i => shorten(i.node)),
  datasets: [
    {
      label: "Violations",
      data: instances.value.map(i => i.violations?.length || 0),
    },
  ],
}))

const violationsPerPropertyChart = computed(() => {
  const counts = new Map()
  instances.value.forEach(i => {
    ;(i.violations || []).forEach(v => {
      counts.set(v.property, (counts.get(v.property) || 0) + 1)
    })
  })
  const labels = Array.from(counts.keys())
  const chartData = labels.map(l => counts.get(l))
  return {
    labels,
    datasets: [{ label: "Violations", data: chartData }],
  }
})

const violationsPerConstraintChart = computed(() => ({
  labels: constraintDefinitions.value.map(c => c.constraint),
  datasets: [
    {
      label: "Triggers",
      data: constraintDefinitions.value.map(c => c.count || 0),
    },
  ],
}))

const goBack = () => router.push({ name: "ClassOverview" })
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.summary-card {
  @apply bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition;
}
.summary-title {
  @apply text-sm font-medium text-gray-600;
}
.summary-value {
  @apply text-4xl font-bold text-gray-800 mt-2;
}

.table-head {
  @apply px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase;
}

code {
  @apply font-mono text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded;
}
</style>

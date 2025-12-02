<template>
  <div class="class-detailed-view p-6 max-w-7xl mx-auto">
    <!-- top -->
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
        <h1 class="text-2xl font-semibold text-gray-800">Class: {{ className }}</h1>
        <button
          @click="showDefinition = !showDefinition"
          class="text-blue-600 text-sm mt-1 hover:underline"
        >
          {{ showDefinition ? 'Hide Definition' : 'Show Definition' }}
        </button>
      </div>

      <!-- Spacer -->
      <div class="w-[120px]"></div>
    </div>

    <!-- Definition Toggle -->
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
              <span class="text-gray-700">{{ def.meaning }}</span>
            </div>
            <span class="text-gray-500 text-xs">{{ def.count ?? '?' }}×</span>
          </article>
        </div>
      </section>
    </transition>

    <!-- Summary Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
      <div class="summary-card">
        <h3 class="summary-title">Total Instances</h3>
        <p class="summary-value">{{ totalInstances }}</p>
      </div>
      <div class="summary-card">
        <div class="flex justify-between items-end">
          <div>
            <h3 class="summary-title">Instances with Violations</h3>
            <p class="summary-value text-red-600">{{ violatingInstances }}</p>
          </div>
          <div class="text-right">
            <p class="text-xs text-gray-500">most affected</p>
            <p class="text-lg font-semibold text-orange-600">{{ mostViolatedInstance || '—' }}</p>
          </div>
        </div>
      </div>
      <div class="summary-card">
        <div class="flex justify-between items-end">
          <div>
            <h3 class="summary-title">Violated Properties</h3>
            <p class="summary-value">{{ violatedPropertiesCount }}</p>
          </div>
          <div class="text-right">
            <p class="text-xs text-gray-500">most violated path</p>
            <p class="text-lg font-semibold text-orange-600">{{ mostViolatedProperty || '—' }}</p>
          </div>
        </div>
      </div>
      <div class="summary-card">
        <div class="flex justify-between items-end">
          <div>
            <h3 class="summary-title">Constraints Triggered</h3>
            <p class="summary-value">{{ triggeredConstraintsCount }}</p>
          </div>
          <div class="text-right">
            <p class="text-xs text-gray-500">most triggered</p>
            <p class="text-lg font-semibold text-orange-600">{{ mostTriggeredConstraint || '—' }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Instances Table -->
    <div class="bg-white rounded-xl shadow-lg overflow-hidden">
      <div class="px-6 py-4 bg-gray-50 border-b">
        <h2 class="text-xl font-semibold text-gray-800">
          All Instances of <code class="text-blue-600 font-mono">{{ className }}</code>
        </h2>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-100">
            <tr>
              <th class="table-head">Instance</th>
              <th class="table-head">Key Properties</th>
              <th class="table-head text-center">Status</th>
              <th class="table-head">Violations</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr
              v-for="inst in instances"
              :key="inst.id"
              :class="{
                'bg-green-50': inst.violations.length === 0,
                'bg-red-50': inst.violations.length > 0,
              }"
              class="hover:bg-gray-50 transition"
            >
              <td class="px-6 py-4">
                <code class="text-sm font-medium text-blue-700">{{ shortenIri(inst.node) }}</code>
              </td>

              <td class="px-6 py-4 text-sm">
                <div class="space-y-1">
                  <div v-for="prop in inst.properties" :key="prop.property">
                    <span class="font-medium">{{ prop.label || prop.property.split(':').pop() }}:</span>
                    <span class="text-gray-600 ml-1">{{ prop.value }}</span>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-center">
                <span
                  :class="inst.violations.length === 0
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'"
                  class="px-3 py-1 rounded-full text-xs font-semibold"
                >
                  {{ inst.violations.length === 0
                    ? 'Clean'
                    : `${inst.violations.length} issue${inst.violations.length > 1 ? 's' : ''}` }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm">
                <template v-if="inst.violations.length">
                  <ul class="space-y-1">
                    <li v-for="v in inst.violations" :key="v.id" class="text-xs">
                      <span class="font-medium text-red-700">{{ v.property }}</span>
                      <span class="text-gray-500 mx-1">→</span>
                      <span class="text-red-600">{{ v.message }}</span>
                    </li>
                  </ul>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const className = ref('')
const showDefinition = ref(false)

const totalInstances = ref(87)

const instances = ref([
  {
    id: 1,
    node: 'http://example.org/WembleyStadium',
    properties: [
      { property: 'rdfs:label', label: 'Name', value: 'Wembley Stadium' },
      { property: 'dbo:capacity', label: 'Capacity', value: '90,000' },
      { property: 'dbo:location', label: 'Location', value: 'London' },
    ],
    violations: [],
  },
  {
    id: 2,
    node: 'http://example.org/OldTrafford',
    properties: [
      { property: 'rdfs:label', value: 'Old Trafford' },
      { property: 'dbo:capacity', value: '74140' },
    ],
    violations: [
      { property: 'dbo:location', message: 'Missing required property' },
      { property: 'dbo:capacity', message: 'Value must be xsd:integer' },
    ],
  },
])

const violatingInstances = computed(() =>
  instances.value.filter(i => i.violations.length > 0).length
)

const violatedPropertiesCount = computed(() => {
  const unique = new Set()
  instances.value.forEach(i => i.violations.forEach(v => unique.add(v.property)))
  return unique.size
})

const triggeredConstraintsCount = computed(() => {
  const unique = new Set()
  instances.value.forEach(i => {
    i.violations.forEach(v => {
      const match = v.message.match(/\((\w+:\w+)\)/)
      unique.add(match?.[1] || 'unknown')
    })
  })
  return unique.size
})

const mostViolatedInstance = computed(() => 'ex:OldTrafford')
const mostViolatedProperty = computed(() => 'dbo:location')
const mostTriggeredConstraint = computed(() => 'sh:minCount')

const constraintDefinitions = ref([
  { constraint: 'sh:minCount', meaning: 'Property is required', count: 18 },
  { constraint: 'sh:maxCount', meaning: 'Maximum number of values', count: 5 },
  { constraint: 'sh:datatype', meaning: 'Wrong data type', count: 12 },
  { constraint: 'sh:class', meaning: 'Wrong class type', count: 3 },
])

const shortenIri = iri => iri.split(/[\/#]/).pop()

onMounted(() => {
  const id = route.params.classId
  className.value = id
    ? decodeURIComponent(String(id)).replace(/_/g, ':')
    : 'Unknown Class'
})

const goBack = () => router.push({ name: 'ClassOverview' })
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

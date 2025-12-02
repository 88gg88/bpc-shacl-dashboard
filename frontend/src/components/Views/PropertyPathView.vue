<template>
  <div class="property-path-detailed-view p-6 max-w-7xl mx-auto">
    <!-- Header -->
    <div class="header-section bg-gray-100 p-4 rounded mb-6 shadow flex items-center justify-between">
      <button
        @click="goBack"
        class="px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 flex items-center gap-2"
      >
        Back to Property Path Overview
      </button>
      <div class="flex flex-col items-center flex-grow text-center">
        <h1 class="text-2xl font-semibold text-gray-800">Property Path: {{ propertyPath }}</h1>
        <button
          @click="showDefinition = !showDefinition"
          class="text-blue-600 text-sm mt-1 hover:underline"
        >
          {{ showDefinition ? 'Hide Definition' : 'Show Definition' }}
        </button>
      </div>
      <div class="w-[120px]"></div>
    </div>

    <!-- Constraint Definitions -->
    <transition name="fade">
      <section v-if="showDefinition" class="bg-gray-50 p-6 rounded-xl mb-8 shadow">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Constraints Applied to this Path</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <article
            v-for="c in constraintDefinition"
            :key="c.constraint"
            class="flex items-center justify-between bg-white p-4 rounded-lg shadow-sm"
          >
            <div class="flex items-center gap-3">
              <code class="font-mono text-xs bg-gray-200 px-2 py-1 rounded">{{ c.constraint }}</code>
              <span class="text-gray-700">{{ c.meaning }}</span>
            </div>
            <span class="text-gray-500 text-xs">{{ c.count }}×</span>
          </article>
        </div>
      </section>
    </transition>

    <!-- Summary Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
      <div class="summary-card">
        <h3 class="summary-title">Total Occurrences</h3>
        <p class="summary-value">{{ totalOccurrences }}</p>
      </div>
      <div class="summary-card">
        <div class="flex justify-between items-end">
          <div>
            <h3 class="summary-title">Violating Triples</h3>
            <p class="summary-value text-red-600">{{ violatingTriples }}</p>
          </div>
          <div class="text-right">
            <p class="text-xs text-gray-500">Most violated subject</p>
            <p class="text-lg font-semibold text-orange-600">{{ mostViolatedSubject || '—' }}</p>
          </div>
        </div>
      </div>
      <div class="summary-card">
        <div class="flex justify-between items-end">
          <div>
            <h3 class="summary-title">Unique Subjects</h3>
            <p class="summary-value">{{ uniqueSubjects }}</p>
          </div>
          <div class="text-right">
            <p class="text-xs text-gray-500">Violation rate</p>
            <p class="text-lg font-semibold text-orange-600">{{ violationRate }}%</p>
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
            <p class="text-xs text-gray-500">Most common</p>
            <p class="text-lg font-semibold text-orange-600">{{ mostCommonConstraint || '—' }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Triples Table -->
    <div class="bg-white rounded-xl shadow-lg overflow-hidden">
      <div class="px-6 py-4 bg-gray-50 border-b">
        <h2 class="text-xl font-semibold text-gray-800">
          All Triples with <code class="text-purple-600 font-mono">{{ propertyPath }}</code>
        </h2>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-100">
            <tr>
              <th class="table-head">Subject</th>
              <th class="table-head">Value</th>
              <th class="table-head text-center">Status</th>
              <th class="table-head">Violation Details</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr
              v-for="triple in triples"
              :key="triple.id"
              :class="{
                'bg-green-50': triple.violations.length === 0,
                'bg-red-50': triple.violations.length > 0,
              }"
              class="hover:bg-gray-50 transition"
            >
              <td class="px-6 py-4">
                <code class="text-sm font-medium text-blue-700">{{ shortenIri(triple.subject) }}</code>
              </td>
              <td class="px-6 py-4 font-mono text-sm text-gray-800 max-w-md truncate">
                <span v-if="triple.isIRI" class="text-purple-600">&lt;{{ triple.value }}&gt;</span>
                <span v-else>"{{ triple.value }}"</span>
                <span v-if="triple.datatype" class="text-xs text-gray-500 ml-1">^^ {{ triple.datatype }}</span>
              </td>
              <td class="px-6 py-4 text-center">
                <span
                  :class="triple.violations.length === 0
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'"
                  class="px-3 py-1 rounded-full text-xs font-semibold"
                >
                  {{ triple.violations.length === 0
                    ? 'Valid'
                    : `${triple.violations.length} issue${triple.violations.length > 1 ? 's' : ''}` }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm">
                <template v-if="triple.violations.length">
                  <ul class="space-y-1">
                    <li v-for="v in triple.violations" :key="v.id" class="text-xs">
                      <span class="font-mono text-red-700 bg-red-100 px-2 py-0.5 rounded">{{ v.constraint }}</span>
                      <span class="text-gray-700 ml-2">{{ v.message }}</span>
                    </li>
                  </ul>
                </template>
                <span v-else class="text-gray-400 italic">No issues</span>
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

const propertyPath = ref('')
const showDefinition = ref(false)

const totalOccurrences = ref(342)

const triples = ref([
  {
    id: 1,
    subject: 'http://example.org/WembleyStadium',
    value: '90000',
    datatype: 'xsd:integer',
    isIRI: false,
    violations: [],
  },
  {
    id: 2,
    subject: 'http://example.org/OldTrafford',
    value: '74,140',
    violations: [
      {
        constraint: 'sh:datatype',
        message: 'Value must be xsd:integer, not string with comma',
      },
    ],
  },
  {
    id: 3,
    subject: 'http://example.org/CampNou',
    value: '99.354',
    violations: [
      { constraint: 'sh:datatype', message: 'Expected xsd:integer' },
      { constraint: 'sh:pattern', message: 'Does not match "^\\d+$"' },
    ],
  },
])

const violatingTriples = computed(() => triples.value.filter(t => t.violations.length > 0).length)
const uniqueSubjects = computed(() => new Set(triples.value.map(t => t.subject)).size)
const violationRate = computed(() =>
  totalOccurrences.value > 0
    ? Math.round((violatingTriples.value / totalOccurrences.value) * 100)
    : 0
)

const mostViolatedSubject = computed(() => 'OldTrafford')
const mostCommonConstraint = computed(() => 'sh:datatype')

const triggeredConstraintsCount = computed(() => {
  const set = new Set()
  triples.value.forEach(t => t.violations.forEach(v => set.add(v.constraint)))
  return set.size
})

const constraintDefinition = ref([
  { constraint: 'sh:datatype', meaning: 'Must be correct datatype (e.g. xsd:integer)', count: 38 },
  { constraint: 'sh:pattern', meaning: 'Value must match regex', count: 7 },
  { constraint: 'sh:minInclusive', meaning: 'Minimum value allowed', count: 2 },
])

const shortenIri = iri => iri.split(/[\/#]/).pop()

onMounted(() => {
  const id = route.params.path
  propertyPath.value = id ? decodeURIComponent(String(id)).replace(/_/g, ':') : 'unknown property'
})

const goBack = () => router.push({ name: 'PropertyPathOverview' })
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
  @apply font-mono text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded;
}
</style>

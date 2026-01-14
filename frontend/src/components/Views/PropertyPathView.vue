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
          {{ showDefinition ? 'Hide Constraints' : 'Show Constraints' }}
        </button>
      </div>
      <div class="w-[120px]"></div>
    </div>
    <!-- Constraint Definitions -->
    <transition name="fade">
      <section v-if="showDefinition" class="bg-gray-50 p-6 rounded-xl mb-8 shadow">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">
          Violated Constraints for this Path ({{ constraintDefinition.length }})
        </h3>
        <div v-if="constraintDefinition.length === 0" class="text-gray-500 italic">
          No constraint violations recorded for this path.
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <article
            v-for="c in constraintDefinition"
            :key="c.constraint"
            class="flex items-center justify-between bg-white p-4 rounded-lg shadow-sm"
          >
            <div class="flex items-center gap-3">
              <code class="font-mono text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded">
                {{ c.constraint }}
              </code>
              <span class="text-gray-700">{{ c.meaning }}</span>
            </div>
            <span
              class="text-gray-500 text-xs font-medium">{{ c.count }}x
            </span>
          </article>
        </div>
      </section>
    </transition>
    <!-- Summary Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
      <div class="summary-card">
        <h3 class="summary-title">Total Violations</h3>
        <p class="summary-value">{{ totalOccurrences }}</p>
      </div>
      <div class="summary-card">
        <div class="flex justify-between items-end">
          <div>
            <h3 class="summary-title">Unique Subjects</h3>
            <p class="summary-value text-red-600">{{ uniqueSubjects }}</p>
          </div>
          <div class="text-right">
            <p class="text-xs text-gray-500">Most violated subject</p>
            <p class="text-lg font-semibold text-orange-600">{{ mostViolatedSubject ||'-' }}</p>
          </div>
        </div>
      </div>
      <div class="summary-card">
        <div class="flex justify-between items-end">
          <div>
            <h3 class="summary-title">Avg. Violation per Subject</h3>
            <p class="summary-value">{{ avgViolation }}</p>
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
            <p class="text-lg font-semibold text-orange-600">{{ mostCommonConstraint || '-' }}</p>
          </div>
        </div>
      </div>
    </div>
    <!-- Charts -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
      <HistogramChart2
        :title="'Top 5 Most Violated Subjects'"
        :xAxisLabel="'Subjects'"
        :yAxisLabel="'Violations'"
        :data="topViolatedSubjectsData"/>
      <HistogramChart2
        :title="'Top 5 Most Violated Constraint Types'"
        :xAxisLabel="'Constraints'"
        :yAxisLabel="'Violations'"
        :data="topViolatedConstraintsData"/>
      <HistogramChart2
        :title="'Top 5 Most Common Violation Types'"
        :xAxisLabel="'Violation Type'"
        :yAxisLabel="'Count'"
        :data="mostCommonViolationsData"/>
    </div>

    <!-- Triples Table -->
    <div class="bg-white rounded-xl shadow-lg overflow-hidden mt-10">
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
              <th class="table-head">Violation Details</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr
              v-for="triple in triplesWithViolations"
              :key="triple.fullSubject + triple.fullValue"
              class="hover:bg-gray-50 transition"
            >
              <td class="px-6 py-4">
                <code class="text-sm font-medium text-blue-700">
                  {{ triple.subject }}
                </code>
              </td>
              <td class="px-6 py-4 font-mono text-sm text-gray-800 max-w-md truncate">
                <span v-if="triple.isIRI" class="text-purple-600">&lt;{{ triple.value }}&gt;</span>
                <span v-else>"{{ triple.value }}"</span>
                <span v-if="triple.datatype" class="text-xs text-gray-500 ml-1">^^ {{ triple.datatype }}</span>
              </td>
              <td class="px-6 py-4 text-sm">
                <ul class="space-y-1">
                  <li v-for="(v, index) in triple.violations" :key="index" class="text-xs">
                    <span class="font-mono text-red-700 bg-red-100 px-2 py-0.5 rounded">
                      {{ getConstraint(v.constraint, v.message) }}
                    </span>
                    <span class="text-gray-700 ml-2">{{ v.message || 'Missing required property' }}</span>
                  </li>
                </ul>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import BarChart from "../Charts/BarChart.vue";
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import HistogramChart2 from "@/components/Charts/HistogramChart2.vue";

const route = useRoute();
const router = useRouter();

const propertyPath = ref("");
const showDefinition = ref(false);
const constraintDefinition = ref([]);
const totalOccurrences = ref(0);
//const violatingTriples = ref(0);
const mostViolatedSubject = ref("");
const uniqueSubjects = ref(0);
const triggeredConstraintsCount = ref(0);
const mostCommonConstraint = ref("");
const triplesWithViolations = ref([]);

//first chart
const topViolatedSubjectsData = ref({
  labels: [],
  datasets: [{
    label: 'Violations',
    data: [],
    backgroundColor: '#42A5F5'
  }]
});

//second chart
const topViolatedConstraintsData = ref({
  labels: [],
  datasets: [{
    label: 'Violations',
    data: [],
    backgroundColor: '#42A5F5'
  }]
});

//second chart
const mostCommonViolationsData = ref({
  labels: [],
  datasets: [{
    label: 'Count',
    data: [],
    backgroundColor: '#42A5F5'
  }]
});

onMounted(async () => {
  const encodedPath = route.params.path;
  if (!encodedPath) {
    propertyPath.value = "Unknown path";
    return;
  }

  // Decode the path (we replaced : with _ in routing)
  const decodedPath = decodeURIComponent(encodedPath).replace(/_/g, ":");

  // Display clean name in header
  propertyPath.value = decodedPath.split("#").pop().split("/").pop();

  // Fetch real violated constraints for this path
  try {
    const resp = await axios.get(`/api/property-path-view/constraints/${encodedPath}`);
    constraintDefinition.value = resp.data.constraints.map(c => ({
      constraint: c.constraint,
      meaning: getConstraintMeaning(c.constraint),  // optional helper below
      count: c.count
    }));

    //first card
    const occResp = await axios.get(`/api/property-path-view/total-occurrences/${encodedPath}`);
    totalOccurrences.value = occResp.data.totalOccurrences;

    //second card
    //const vtResp = await axios.get(`/api/property-path-view/violating-triples-count/${encodedPath}`);
    const mvsResp = await axios.get(`/api/property-path-view/most-violated-subject/${encodedPath}`);
    mostViolatedSubject.value = mvsResp.data.subject;
    const usResp = await axios.get(`/api/property-path-view/unique-subjects/${encodedPath}`);
    uniqueSubjects.value = usResp.data.uniqueSubjects;

    //fourth card
    const tcResp = await axios.get(`/api/property-path-view/triggered-constraints-count/${encodedPath}`);
    triggeredConstraintsCount.value = tcResp.data.triggeredConstraintsCount;
    const mccResp = await axios.get(`/api/property-path-view/most-common-constraint/${encodedPath}`);
    mostCommonConstraint.value = mccResp.data.constraint;

    //first chart
    const chartResp = await axios.get(`/api/property-path-view/top-violated-subjects/${encodedPath}`);
    const chartData = chartResp.data.topSubjects;

    topViolatedSubjectsData.value = {
    labels: chartData.map(item => item.subject),
    datasets: [
      {
        label: 'Violations',
        data: chartData.map(item => Number(item.count)),
        backgroundColor: '#42A5F5'
      }
    ]
    };

    //second chart
    const chartResp2 = await axios.get(`/api/property-path-view/top-violated-constraints/${encodedPath}`);
    const chartData2 = chartResp2.data.topConstraints;

    topViolatedConstraintsData.value = {
    labels: chartData2.map(item => item.constraint),
    datasets: [
      {
        label: 'Violations',
        data: chartData2.map(item => Number(item.count)),
        backgroundColor: '#42A5F5'
      }
    ]
    };

    //third chart
    const chartResp3 = await axios.get(`/api/property-path-view/top-violated-messages/${encodedPath}`);
    const chartData3 = chartResp3.data.topMessages;

    mostCommonViolationsData.value = {
    labels: chartData3.map(item => item.message),
    datasets: [
      {
        label: 'Count',
        data: chartData3.map(item => Number(item.count)),
        backgroundColor: '#42A5F5'
      }
    ]
    };

    //bottom table
    const triplesResp = await axios.get(`/api/property-path-view/triples-with-violations/${encodedPath}`);
    triplesWithViolations.value = triplesResp.data.triples;

  } catch (error) {
    console.error("Failed to load constraints for path:", error);
    constraintDefinition.value = [];
    totalOccurrences.value = 0;
    mostViolatedSubject.value = "e";
    uniqueSubjects.value = 0;
    triggeredConstraintsCount.value = 0;
    mostCommonConstraint.value = "e"
  }
});

const getConstraintMeaning = (constraint) => {
  const meanings = {
    "In": "Value must be one of the allowed values (sh:in)",
    "MinCount": "Minimum number of values required",
    "MaxCount": "Maximum number of values allowed",
    "Class": "Value must be of a specific class",
    "Datatype": "Value must have correct datatype",
    "Pattern": "Value must match regex pattern",
    "HasValue": "Must have this exact value",
    "NodeKind": "Value must be IRI, Literal, or Blank Node",
  };
  return meanings[constraint] || "Constraint violation";
};

const triples2 = ref([
  {
    id: 1,
    subject: "http://example.org/WembleyStadium",
    value: "90000",
    datatype: "xsd:integer",
    isIRI: false,
    violations: [],
  },
  {
    id: 2,
    subject: "http://example.org/OldTrafford",
    value: "74,140",
    violations: [
      { id: "v1", constraint: "sh:datatype", message: "Value must be xsd:integer, not string with comma" },
    ],
  },
  {
    id: 3,
    subject: "http://example.org/CampNou",
    value: "99.354",
    violations: [
      { id: "v2", constraint: "sh:datatype", message: "Expected xsd:integer" },
      { id: "v3", constraint: "sh:pattern", message: "Does not match \"^\\d+$\"" },
    ],
  },
]);

//const violatingTriples = computed(() => triples.value.filter(t => t.violations.length > 0).length);

//const uniqueSubjects = computed(() => new Set(triples.value.map(t => t.subject)).size);

const avgViolation = computed(() =>
  totalOccurrences.value > 0 ? Math.round((totalOccurrences.value / uniqueSubjects.value)*10) / 10 : 0
);

const getConstraint = (constraint, message) => {
  if (constraint) return constraint;

  if (message.includes("Less than 1 values") || message.includes("minCount")) return "MinCount";
  if (message.includes("not in list")) return "In";
  if (message.includes("datatype")) return "Datatype";
  if (message.includes("pattern")) return "Pattern";
  if (message.includes("class")) return "Class";
  return "Unknown";
};

//const mostViolatedSubject = computed(() => "OldTrafford");
//const mostCommonConstraint = computed(() => "sh:datatype");

//const triggeredConstraintsCount = computed(() => {
  //const set = new Set();
  //triples.value.forEach(t => t.violations.forEach(v => set.add(v.constraint)));
  //return set.size;
//});

//const constraintDefinition = ref([
  //{ constraint: "sh:datatype", meaning: "Must be correct datatype (e.g. xsd:integer)", count: 38 },
  //{ constraint: "sh:pattern", meaning: "Value must match regex", count: 7 },
  //{ constraint: "sh:minInclusive", meaning: "Minimum value allowed", count: 2 },
//]);

const triplesWithViolations2 = computed(() =>
  triples2.value.filter(t => t.violations.length > 0)
);

const shortenIri = iri => iri.split(/[\/#]/).pop();

const violationsPerSubjectChart = computed(() => {
  const counts = new Map();
  triples2.value.forEach(t => {
    if (t.violations.length > 0) {
      const key = shortenIri(t.subject);
      counts.set(key, (counts.get(key) || 0) + t.violations.length);
    }
  });
  const labels = Array.from(counts.keys());
  const data = labels.map(l => counts.get(l) || 0);
  return { labels, datasets: [{ label: "Violations", data }] };
});
const violationsPerConstraintChart = computed(() => {const counts = new Map();
  triples2.value.forEach(t =>
    t.violations.forEach(v => {
      counts.set(v.constraint, (counts.get(v.constraint) || 0) + 1);
    })
  );
  const labels = Array.from(counts.keys());
  const data = labels.map(l => counts.get(l) || 0);
  return { labels, datasets: [{ label: "Violations", data }] };
});

const violationsByMessageCategoryChart = computed(() => {
  const counts = new Map();
  triples2.value.forEach(t =>
    t.violations.forEach(v => {
      counts.set(v.message, (counts.get(v.message) || 0) + 1);
    })
  );
  const labels = Array.from(counts.keys());
  const data = labels.map(l => counts.get(l) || 0);
  return { labels, datasets: [{ label: "Violations", data }] };
});

const goBack = () => router.push({ name: "PropertyPathOverview" });
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

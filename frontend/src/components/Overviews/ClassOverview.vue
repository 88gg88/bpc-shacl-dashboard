<template>
  <div class="class-overview p-6 w-full">
    <!-- tags -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
      <div
        v-for="(tag, i) in tags"
        :key="i"
        class="bg-white rounded-xl shadow p-6 hover:shadow-md transition"
      >
        <div class="flex justify-between items-center">
          <div>
            <h3 class="text-sm font-medium text-gray-600 mb-1">{{ tag.title }}</h3>
            <p class="text-4xl font-bold text-gray-800">{{ tag.value }}</p>
          </div>
        </div>
      </div>
    </div>
    <!-- charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-10">
      <div class="bg-white rounded-xl shadow p-6">
        <HistogramChart
          :title="'Top 5 Classes by Instances'"
          :xAxisLabel="'Classes'"
          :yAxisLabel="'Instances'"
          :data="instancesChart"
        />
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <HistogramChart
          :title="'Top 5 Classes by Violations'"
          :xAxisLabel="'Classes'"
          :yAxisLabel="'Violations'"
          :data="violationsChart"
        />
      </div>
    </div>
    <!-- Table Section -->
    <div class="bg-white rounded-xl shadow overflow-hidden">
      <div class="bg-gray-50 px-6 py-4 border-b">
        <h2 class="text-xl font-semibold text-gray-800">Class Details</h2>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-100">
            <tr>
              <th
                v-for="(column, index) in columns"
                :key="index"
                class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase cursor-pointer"
                @click="sortColumn(column)"
              >
                {{ column.label }}
                <span class="ml-1">
                  {{ sortKey === column.field ? (sortOrder === 'asc' ? '▲' : '▼') : '' }}
                </span>
              </th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-700 uppercase"></th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 bg-white">
            <tr
              v-for="classX in sortedPaginatedData"
              :key="classX.id"
              class="hover:bg-gray-50 cursor-pointer"
              @click="goToClass(classX)"
            >
              <td class="px-6 py-4">
                <code class="text-sm bg-blue-50 text-blue-800 px-2 py-1 rounded">{{ classX.classId }}</code>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ classX.instances }}</td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ classX.violations }}</td>
              <td class="px-6 py-4 text-center">
                <font-awesome-icon icon="arrow-right" class="text-blue-500 hover:text-blue-700" />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- Pagination -->
      <div class="flex justify-between items-center px-6 py-4 bg-gray-50 border-t">
        <button
          :disabled="currentPage === 1"
          @click="prevPage"
          class="px-4 py-2 border rounded hover:bg-gray-50 disabled:opacity-50"
        >Previous
        </button>
        <span class="text-gray-700">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        <button
          :disabled="currentPage === totalPages"
          @click="nextPage"
          class="px-4 py-2 border rounded hover:bg-gray-50 disabled:opacity-50"
        >Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * ClassOverview component
 *
 * detailed description incoming...
 */
import SparklineChart from "../Charts/SparklineChart.vue";
import HistogramChart from "../Charts/HistogramChart.vue";
import { useRouter } from "vue-router";
import { ref, computed } from "vue";

const router = useRouter();

// Mock data for tags
const tags = [
  { title: "Total Classes", value: 25 },
  { title: "Total Violations", value: 125},
  { title: "Avg Violations per Class", value: 5 },
  { title: "Most Violated Class", value: "Stadium" },
];
// Mock data for the table
const classes = ref([
  { id: 1, classId: "dbo:Stadium", instances: 120, violations: 25},
  { id: 2, classId: "dbo:ComicStrip", instances: 98, violations: 12},
  { id: 3, classId: "dbo:Amphibian", instances: 76, violations: 8 },
]);

// Mock data for the charts
const instancesChart = {
  labels: ["Stadium", "ComicStrip", "Amphibian"],
  datasets: [
    {
      label: "Instances",
      data: [120, 98, 76],
      backgroundColor: "#42A5F5",
    },
  ],
};

const violationsChart = {
  labels: ["Stadium", "ComicStrip", "Amphibian"],
  datasets: [
    {
      label: "Violations",
      data: [25, 12, 8],
      backgroundColor: "#66BB6A",},
  ],
};

// Pagination logic
const currentPage = ref(1);
const pageSize = ref(5);
const totalPages = computed(() => Math.ceil(classes.value.length / pageSize.value));

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return classes.value.slice(start, start + pageSize.value);
});
const sortedPaginatedData = computed(() => {
  const data = paginatedData.value;
  if (sortKey.value) {
    return [...data].sort((a, b) => {
      const result = a[sortKey.value].toString().localeCompare(b[sortKey.value].toString(), undefined, { numeric: true });
      return sortOrder.value === "asc" ? result : -result;
    });
  }
  return data;
});

const sortKey = ref("");
const sortOrder = ref("asc");

const columns = ref([
  { label: "Class", field: "name"},
  { label: "Instances", field: "instances"},
  { label: "Violations", field: "violations"},
])

const sortColumn = (column) => {
  if (sortKey.value === column.field) {
    sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
  } else {
    sortKey.value = column.field;
    sortOrder.value = "asc";
  }
};

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};
const goToClass = (c) => {
  router.push({ name: "ClassDetailedView", params: { classId: c.classId } });
};
</script>

<style scoped>
.summary-card {
  @apply bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition;
}
.summary-title {
  @apply text-sm font-medium text-gray-600;
}
.summary-value {
  @apply text-4xl font-bold text-gray-800 mt-1;
}
.table-head {
  @apply px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider;
}
code {
  @apply font-mono text-sm bg-blue-50 text-blue-800 px-2 py-1 rounded;
}
</style>

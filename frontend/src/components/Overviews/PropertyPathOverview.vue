<template>
  <div class="propertypath-overview p-6 w-full">
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
    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-10">
      <div class="bg-white rounded-xl shadow p-6">
        <HistogramChart
          :title="'Top 10 Most Violated Paths'"
          :xAxisLabel="'Path'"
          :yAxisLabel="'Violations'"
          :data="histogramData"
        />
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <BarChart
          :title="'Path Type Distribution'"
          :xAxisLabel="'Path Types'"
          :yAxisLabel="'Occurrences'"
          :data="barChartData"
        />
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <HistogramChart
          :title="'Top 10 Most frequent constraint Violation'"
          :xAxisLabel="'Constraint'"
          :yAxisLabel="'Violations'"
          :data="histogramData2"
        />
      </div>
    </div>
    <!-- Table Section -->
    <div class="bg-white rounded-xl shadow overflow-hidden">
      <div class="bg-gray-50 px-6 py-4 border-b">
        <h2 class="text-xl font-semibold text-gray-800">Property Path Details</h2>
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
              v-for="path in sortedPaginatedData"
              :key="path.id"
              class="hover:bg-gray-50 cursor-pointer"
              @click="goToPropertyPath(path)"
            >
              <td class="px-6 py-4">
                <code class="text-sm bg-blue-50 text-blue-800 px-2 py-1 rounded">{{ path.path }}</code>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ path.type }}</td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ path.description }}</td>
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
        >
          Previous
        </button>
        <span class="text-gray-700">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        <button
          :disabled="currentPage === totalPages"
          @click="nextPage"
          class="px-4 py-2 border rounded hover:bg-gray-50 disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import HistogramChart from "../Charts/HistogramChart.vue";
import BarChart from "../Charts/BarChart.vue";
import HorizontalBoxPlotChart from "../Charts/HorizontalBoxPlotChart.vue";
import { ref, computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

// tags
const tags = ref([
  { title: "Total Violations", value: 50 },
  { title: "Total Property Paths Violated", value: 13 },
  { title: "Most violated Path", value: "book:hasAuthor" },
  { title: "Most violated constraint", value: "minCount" },
]);

// data
const histogramData = {
  labels: ['1', '2', '3', '4'],
  datasets: [{ label: 'Violations', data: [10, 15, 20, 5], backgroundColor: '#42A5F5' }],
};

const histogramData2 = {
  labels: ['1-2', '3-4', '5-6', '7-8'],
  datasets: [{ label: 'Violations', data: [10, 15, 20, 5], backgroundColor: '#42A5F5' }],
};

const barChartData = {
  labels: ['IRI', 'Literal', 'Blank Node'],
  datasets: [{ label: 'Occurrences', data: [25, 15, 10], backgroundColor: ['#42A5F5', '#66BB6A', '#FF5252'] }],
};

// const boxPlotData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Table data
const propertyPaths = ref([
  { id: 1, path: "book:hasAuthor", type: "IRI", description: "Indicates the author of a book." },
  { id: 2, path: "book:hasTitle", type: "Literal", description: "Indicates the title of a book." },
  { id: 3, path: "book:publishedBy", type: "IRI", description: "Indicates the publisher of the book." },
]);

// Pagination
const currentPage = ref(1);
const pageSize = ref(5);
const totalPages = computed(() => Math.ceil(propertyPaths.value.length / pageSize.value));

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return propertyPaths.value.slice(start, start + pageSize.value);
});

const sortKey = ref("");
const sortOrder = ref("asc");

const sortedPaginatedData = computed(() => {
  const data = paginatedData.value;
  if (!sortKey.value) return data;
  return [...data].sort((a, b) => {
    const result = a[sortKey.value]?.toString().localeCompare(b[sortKey.value]?.toString() || '', undefined, { numeric: true });
    return sortOrder.value === "asc" ? result : -result;
  });
});

const columns = ref([
  { label: "Property Path", field: "path" },
  { label: "Type", field: "type" },
  { label: "Description", field: "description" },
]);

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

const goToPropertyPath = (path) => {
  router.push({ name: "PropertyPathView", params: { path: path.path } });
};
</script>

<style scoped>
.propertypath-overview {
  @apply w-full;
}

code {
  @apply font-mono text-sm bg-blue-50 text-blue-800 px-2 py-1 rounded;
}
</style>

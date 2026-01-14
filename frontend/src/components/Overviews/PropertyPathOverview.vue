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
            <p class="text-4xl font-bold text-gray-800 truncate max-w-full" :title="tag.value">{{ tag.value }}</p>
          </div>
        </div>
      </div>
    </div>
    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-10">
      <div class="bg-white rounded-xl shadow p-6">
        <HistogramChart2
          :title="'Top 10 Most Violated Paths'"
          :xAxisLabel="'Property Path'"
          :yAxisLabel="'Violations'"
          :data="topViolatedPathsData"
        />
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <HistogramChart2
          :title="'Path Type Distribution'"
          :xAxisLabel="'Path Types'"
          :yAxisLabel="'Occurrences'"
          :data="pathTypeData"
        />
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <HistogramChart2
          :title="'Top 10 Most Violated Constraints'"
          :xAxisLabel="'Constraint'"
          :yAxisLabel="'Violations'"
          :data="topViolatedConstraintsData"
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
              v-for="row in tableData"
              :key="row.rawPath"
              class="hover:bg-gray-50 cursor-pointer"
              @click="goToPropertyPath(row)"
            >
              <td class="px-6 py-4">
                <code class="text-sm bg-blue-50 text-blue-800 px-2 py-1 rounded">{{ row.path }}</code>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600 text-center font-medium">
                {{ row.violations.toLocaleString() }}
              </td>
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
import HistogramChart2 from "../Charts/HistogramChart2.vue";
import BarChart from "../Charts/BarChart.vue";
import HorizontalBoxPlotChart from "../Charts/HorizontalBoxPlotChart.vue";
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();

// tags
const tags = ref([
  { title: "Total Violations", value: "Loading..." },
  { title: "Total Property Paths Violated", value: "Loading..." },
  { title: "Most violated Path", value: "Loading..." },
  { title: "Most violated constraint", value: "Loading..." },
]);

//first chart
const topViolatedPathsData = ref({
  labels: [],
  datasets: [{
    label: 'Violations',
    data: [],
    backgroundColor: '#42A5F5'
  }]
});

//second chart
const pathTypeData = ref({
  labels: [],
  datasets: [{
    label: 'Occurrences',
    data: [],
    backgroundColor: ['#42A5F5', '#66BB6A', '#FF5252', '#FFA726', '#AB47BC', '#26A69A', '#FF7043']
  }]
});

//third chart
const topViolatedConstraintsData = ref({
  labels: [],
  datasets: [{
    label: 'Violations',
    data: [],
    backgroundColor: '#42A5F5'
  }]
});

//table
const tableData = ref([]);
const totalItems = ref(0);
const currentPage = ref(1);
const pageSize = ref(10);
const sortKey = ref("violations");
const sortOrder = ref("desc");

const loadTableData = async () => {
  try {
    const response = await axios.get("/api/property-path/path-details", {
      params: {
        page: currentPage.value,
        page_size: pageSize.value,
        sort_by: sortKey.value,
        sort_order: sortOrder.value
      }
    });
    tableData.value = response.data.items;
    totalItems.value = response.data.total;
  } catch (error) {
    console.error("Failed to load table:", error);
    tableData.value = [];
    totalItems.value = 0;
  }
};

onMounted(async () => {
  try {
    const totalV = await axios.get("/api/property-path/total-violations");
    tags.value[0].value = totalV.data.totalViolations;

    const totalPaths = await axios.get("/api/property-path/violated-paths-count");
    tags.value[1].value = totalPaths.data.totalViolatedPaths;

    const mostPath = await axios.get("/api/property-path/most-violated-path");
    const path = mostPath.data.mostViolatedPath;
    const count = mostPath.data.violationCount;
    tags.value[2].value = `${path} (${count})`;

    const mostConst = await axios.get("/api/property-path/most-violated-constraint");
    tags.value[3].value = `${mostConst.data.mostViolatedConstraint} (${mostConst.data.violationCount})`;

    const chartResp = await axios.get("/api/property-path/top-violated-paths");
    const chartData = chartResp.data.topPaths;

    topViolatedPathsData.value = {
    labels: chartData.map(item => item.path),
    datasets: [
      {
        label: 'Violations',
        data: chartData.map(item => Number(item.count)),
        backgroundColor: '#42A5F5'
      }
    ]
    };

    const typeResp = await axios.get("/api/property-path/path-type-distribution");
    const typeData = typeResp.data.pathTypes;

    pathTypeData.value = {
    labels: typeData.map(item => item.type),
    datasets: [
      {
        label: 'Occurrences',
        data: typeData.map(item => Number(item.count)),
        backgroundColor: '#42A5F5'
      }
    ]
    };

    const constResp = await axios.get("/api/property-path/top-violated-constraints");
    const constData = constResp.data.topConstraints;

    topViolatedConstraintsData.value = {
    labels: constData.map(item => item.constraint),
    datasets: [
      {
        label: 'Violations',
        data: constData.map(item => Number(item.count)),
        backgroundColor: '#42A5F5'
      }
    ]
    };

    await loadTableData();

  } catch (error) {
    console.error("Failed to fetch stats:", error);

    tags.value.forEach(tag => tag.value = "Error");

    if (topViolatedPathsData.value.labels.length === 0) {
      topViolatedPathsData.value.labels = ["No data"];
      topViolatedPathsData.value.datasets[0].data = [0];
    }
    if (topViolatedConstraintsData.value.labels.length === 0) {
      topViolatedConstraintsData.value.labels = ["No data"];
      topViolatedConstraintsData.value.datasets[0].data = [0];
    }
    if (pathTypeData.value.labels.length === 0) {
      pathTypeData.value.labels = ["No data"];
      pathTypeData.value.datasets[0].data = [0];
    }
  }
});

// mockdata

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
//const currentPage = ref(1);
//const pageSize = ref(5);
const totalPages = computed(() => Math.ceil(propertyPaths.value.length / pageSize.value));

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return propertyPaths.value.slice(start, start + pageSize.value);
});

//const sortKey = ref("");
//const sortOrder = ref("asc");

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
  { label: "Violations", field: "violations" }
]);

const sortColumn = (column) => {
  if (sortKey.value === column.field) {
    sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
  } else {
    sortKey.value = column.field;
    sortOrder.value = "desc";
  }
  loadTableData()
};

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};
const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};

const goToPropertyPath = (row) => {
  const encoded = encodeURIComponent(row.rawPath).replace(/:/g, "_");
  router.push({ name: "PropertyPathView", params: { path: encoded } });
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

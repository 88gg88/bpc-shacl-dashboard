<template>
  <div class="class-overview p-4">
    <!-- Tags Section -->
    <div class="grid grid-cols-4 gap-4 mb-6">
      <div
        v-for="(tag, i) in tags"
        :key="i"
        class="flex items-center bg-white rounded-lg shadow p-6 hover:shadow-md transition"
      >
        <div class="flex-grow">
          <h3 class="text-sm font-medium text-gray-600 mb-1">{{ tag.title }}</h3>
          <p class="text-3xl font-bold text-gray-800">{{ tag.value }}</p>
        </div>
        <div class="flex items-center justify-center bg-gray-200 rounded-full w-12 h-12">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none"
               viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4 4h16v16H4z" />
          </svg>
        </div>
      </div>
    </div>

    <!-- Plots Section -->
    <div class="grid grid-cols-3 gap-4 mb-6">
      <BarChart
        :title="'Instances per Class'"
        :xAxisLabel="'Classes'"
        :yAxisLabel="'Instances'"
        :data="instancesChart"
      />
      <BarChart
        :title="'Violations per Class'"
        :xAxisLabel="'Classes'"
        :yAxisLabel="'Violations'"
        :data="violationsChart"
      />
      <BarChart
        :title="'Satisfaction Rates'"
        :xAxisLabel="'Classes'"
        :yAxisLabel="'%'"
        :data="satisfactionChart"
      />
    </div>

    <!-- Table Section -->
    <div class="bg-white border border-gray-200 p-6 rounded-lg shadow-lg">
      <h2 class="text-2xl font-bold text-gray-700 mb-4">Class Details</h2>
      <table class="w-full border-collapse">
        <thead class="bg-gray-200">
          <tr>
            <th
              v-for="(column, index) in columns"
              :key="index"
              class="text-left px-6 py-3 border-b border-gray-300 text-gray-600 font-medium cursor-pointer"
              @click="sortColumn(column)">
              {{ column.label }}
              <span class="sort-indicator" >
                {{ sortKey === column.field ? (sortOrder === 'asc' ? ' ▲' : ' ▼') : '' }}
              </span>
            </th>
            <th class="text-center px-6 py-3 border-b border-gray-300 text-gray-600 font-medium"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="classX in sortedPaginatedData"
            :key="classX.id"
            class="even:bg-gray-50 hover:bg-blue-50 transition-colors"
            @click="goToClass(classX)"
          >
            <td class="px-6 py-4 border-b border-gray-300">{{ classX.classId }}</td>
            <td class="px-6 py-4 border-b border-gray-300">{{ classX.instances }}</td>
            <td class="px-6 py-4 border-b border-gray-300">{{ classX.violations }}</td>
            <td class="px-6 py-4 border-b border-gray-300">{{ classX.satisfaction }}</td>
            <td class="px-6 py-4 border-b border-gray-300 text-center">
              <button class="text-blue-600 hover:text-blue-800">
                <font-awesome-icon icon="arrow-right" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="flex justify-between items-center mt-4">
        <button
          :disabled="currentPage === 1"
          @click="prevPage"
          class="px-4 py-2 bg-gray-200 text-gray-600 rounded hover:bg-gray-300 disabled:opacity-50"
        >
          Previous
        </button>
        <span class="text-gray-700">Page {{ currentPage }} of {{ totalPages }}</span>
        <button
          :disabled="currentPage === totalPages"
          @click="nextPage"
          class="px-4 py-2 bg-gray-200 text-gray-600 rounded hover:bg-gray-300 disabled:opacity-50"
        >
          Next
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
import BarChart from "../Charts/BarChart.vue";
import { useRouter } from "vue-router";
import { ref, computed } from "vue";

const router = useRouter();

// Mock data for tags
const tags = [
  { title: "Total Classes", value: 25 },
  { title: "Avg Violations per Class", value: 5 },
  { title: "Avg Satisfaction Rate (%)", value: "72%" },
  { title: "Most Violated Class", value: "StadiumShape" },
];

// Mock data for the table
const classes = ref([
  { id: 1, classId: "dbo:Stadium", instances: 120, violations: 25, satisfaction: 80 },
  { id: 2, classId: "dbo:ComicStrip", instances: 98, violations: 12, satisfaction: 88 },
  { id: 3, classId: "dbo:Amphibian", instances: 76, violations: 8, satisfaction: 90 },
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
      backgroundColor: "#66BB6A",
    },
  ],
};

const satisfactionChart = {
  labels: ["Stadium", "ComicStrip", "Amphibian"],
  datasets: [
    {
      label: "Satisfaction",
      data: [80, 88, 90],
      backgroundColor: "#FF5252",
    },
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
  { label: "Satisfaction", field: "satisfaction"}
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
</script> <style scoped>
.sparkline {
  width: 100px;
  height: 50px;
}
</style>

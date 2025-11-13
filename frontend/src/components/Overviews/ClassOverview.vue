<template>
  <div class="p-4">
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

    <div class="grid grid-cols-3 gap-4">
      <div
        v-for="c in classOverviewData"
        :key="c.classId"
        class="bg-white shadow rounded p-4 flex items-center justify-between cursor-pointer hover:shadow-lg transition"
        @click="goToClass(c)"
      >
        <div class="flex items-center">
          <div class="bg-blue-100 text-blue-500 p-2 rounded-full mr-4">
            <svg xmlns="http://www.w3.org/2000/svg"
                 class="h-6 w-6"
                 fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 4h16v16H4z" />
            </svg>
          </div>

          <div>
            <p class="text-lg font-semibold">{{ c.classId }}</p>
            <ul class="text-sm text-blue-500">
              <li>Instances: {{ c.instances }}</li>
              <li>Violations: {{ c.violations }}</li>
              <li>Satisfaction Rate: {{ c.satisfaction }}%</li>
            </ul>
          </div>
        </div>

        <div class="sparkline">
          <sparkline-chart :data="[7, 1, 10, 5]" color="blue" />
        </div>
      </div>
    </div> </div>
</template>

<script setup>
import SparklineChart from "../Charts/SparklineChart.vue";
import BarChart from "../Charts/BarChart.vue";
import { useRouter } from "vue-router";

const router = useRouter();
const tags = [
  { title: "Total Classes", value: 25 },
  { title: "Avg Violations per Class", value: 5 },
  { title: "Avg Satisfaction Rate (%)", value: "72%" },
  { title: "Most Violated Class", value: "StadiumShape" },
];

const classOverviewData = [
  { classId: "dbo:StadiumShape", instances: 120, violations: 25, satisfaction: 80 },
  { classId: "dbo:ComicStripShape", instances: 98, violations: 12, satisfaction: 88 },
  { classId: "dbo:AmphibianShape", instances: 76, violations: 8, satisfaction: 90 },
];

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
const goToClass = (c) => {
  router.push({ name: "ClassDetailedView", params: { classId: c.classId } });
};
</script> <style scoped>
.sparkline {
  width: 100px;
  height: 50px;
}
</style>

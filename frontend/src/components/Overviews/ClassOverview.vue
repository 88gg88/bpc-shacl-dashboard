<template>
  <div class="class-overview p-6 w-full">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
      <div
        v-for="(tag, i) in tags"
        :key="i"
        class="bg-white rounded-xl shadow p-6"
      >
        <h3 class="text-sm text-gray-600">{{ tag.title }}</h3>
        <p class="text-4xl font-bold">{{ tag.value }}</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-10">
      <HistogramChart
        title="Top 5 Classes by Instances"
        xAxisLabel="Classes"
        yAxisLabel="Instances"
        :data="instancesChart"
      />
      <HistogramChart
        title="Top 5 Classes by Violations"
        xAxisLabel="Classes"
        yAxisLabel="Violations"
        :data="violationsChart"
      />
    </div>

    <div class="bg-white rounded-xl shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-100">
          <tr>
            <th class="px-6 py-3 text-left">Class</th>
            <th class="px-6 py-3 text-left">Instances</th>
            <th class="px-6 py-3 text-left">Violations</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="c in classes"
            :key="c.id"
            class="hover:bg-gray-50 cursor-pointer"
            @click="goToClass(c)"
          >
            <td class="px-6 py-4">
              <code>{{ c.classLabel }}</code>
            </td>
            <td class="px-6 py-4">{{ c.instances }}</td>
            <td class="px-6 py-4">{{ c.violations }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import HistogramChart from "../Charts/HistogramChart.vue"
import axios from "axios"
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

const tags = ref([])
const classes = ref([])
const instancesChart = ref({ labels: [], datasets: [] })
const violationsChart = ref({ labels: [], datasets: [] })

const shorten = (iri) => {
  if (!iri) return ""
  return String(iri).split(/[\/#]/).pop()
}

onMounted(async () => {
  const res = await axios.get("http://localhost:5001/api/class-view/overview")

  tags.value = [
    { title: "Total Classes", value: res.data.totalClasses },
    { title: "Total Violations", value: res.data.totalViolations },
    { title: "Avg Violations per Class", value: res.data.avgViolationsPerClass },
    { title: "Most Violated Class", value: shorten(res.data.mostViolatedClass) },
  ]

  classes.value = (res.data.classes || []).map((c, i) => ({
    id: i,
    classUri: c.class,
    classLabel: shorten(c.class),
    instances: c.instances,
    violations: c.violations,
  }))

  instancesChart.value = {
    labels: (res.data.topInstances || []).map((c) => shorten(c.class)),
    datasets: [
      {
        label: "Instances",
        data: (res.data.topInstances || []).map((c) => c.instances),
      },
    ],
  }

  violationsChart.value = {
    labels: (res.data.topViolations || []).map((c) => shorten(c.class)),
    datasets: [
      {
        label: "Violations",
        data: (res.data.topViolations || []).map((c) => c.violations),
      },
    ],
  }

  console.log("instancesChart", instancesChart.value)
  console.log("violationsChart", violationsChart.value)
})

const goToClass = (c) => {
  router.push({
    name: "ClassDetailedView",
    params: { classId: encodeURIComponent(c.classUri) },
  })
}
</script>

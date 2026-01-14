<template>
  <div class="key-metrics grid grid-cols-3 gap-4">
    <div class="metric-card bg-white shadow rounded p-4 flex items-center justify-between">
      <div class="flex items-center">
        <div class="icon bg-blue-100 text-blue-500 p-2 rounded-full mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4h16v16H4z" />
          </svg>
        </div>
        <div>
          <p class="text-lg font-semibold">Path Occurrence Frequency</p>
          <ul class="text-sm text-blue-500">
            <li v-for="shape in shapesUsingThisPath" :key="shape">{{ shape }}</li>
          </ul>
        </div>
      </div>
      <div class="sparkline">
        <sparkline-chart :data="[7, 1, 10, 5]" color="blue" />
      </div>
    </div>

    <div class="metric-card bg-white shadow rounded p-4 flex items-center justify-between">
      <div class="flex items-center">
        <div class="icon bg-blue-100 text-blue-500 p-2 rounded-full mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636a9 9 0 11-12.728 0M15 12h.01M9 12h.01M15 16h.01M9 16h.01M12 12.5l-3-3m0 0h6m-6 0l3 3" />
          </svg>
        </div>
        <div>
          <p class="text-lg font-semibold">Distribution of Violations</p>
          <ul class="text-sm text-blue-500">
            <li v-for="(count, node) in violationsByFocusNode" :key="node">{{ node }}: {{ count }}</li>
          </ul>
        </div>
      </div>
      <div class="sparkline">
        <sparkline-chart :data="[7, 1, 10, 5]" color="blue" />
      </div>
    </div>

    <div class="metric-card bg-white shadow rounded p-4 flex items-center justify-between">
      <div class="flex items-center">
        <div class="icon bg-blue-100 text-blue-500 p-2 rounded-full mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h18v18H3z" />
          </svg>
        </div>
        <div>
          <p class="text-lg font-semibold">Example Triples</p>
          <ul class="text-sm text-blue-500">
            <li v-for="triple in exampleViolations" :key="triple">{{ triple }}</li>
          </ul>
        </div>
      </div>
      <div class="sparkline">
        <sparkline-chart :data="[7, 1, 10, 5]" color="blue" />
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * Metrics component
 *
 * Displays key metrics about property paths in a dashboard format.
 * Shows information such as shapes using this path, violations by focus node,
 * constraint components, and example violations, each with a small sparkline chart.
 *
 * @example
 * // Basic usage in a parent component template:
 * // <Metrics />
 *
 * @prop {Array} [shapesUsingThisPath=['Shape 1', 'Shape 2', 'Shape 3']] - Shapes using this property path
 * @prop {Object} [violationsByFocusNode] - Object mapping focus nodes to violation counts
 * @prop {Array} [constraintComponents] - Array of constraint components related to this path
 * @prop {Array} [exampleViolations] - Examples of violations for this property path
 *
 * @dependencies
 * - vue (Composition API)
 * - ../Charts/SparklineChart.vue
 *
 * @style
 * - Grid layout with responsive card design.
 * - Cards with icons, titles, metric values, and sparkline charts.
 * - Color-coded icons and list items for visual categorization.
 *
 * @returns {HTMLElement} A grid of four metric cards displaying property path information,
 * each with an icon, title, list of related data, and mini sparkline chart. Cards show shapes using
 * this path, violations by focus node, constraint components, and example violations with color coding.
 */
import SparklineChart from '../Charts/SparklineChart.vue'

const shapesUsingThisPath = [
  'shs:StadiumShape',
  'shs:AmphibianShape',
  'shs:ComicStripShape'
]

const violationsByFocusNode = {
  'Node A': 2379,
  'Node B': 729,
  'Node C': 718
}

const exampleViolations = [
  'shs:StadiumShape --> sh:InConstraintComponent -->2379 violations',
  'shs:AmphibianShape --> sh:InConstraintComponent --> 729 violations',
  'shs:ComicStripShape --> sh:InConstraintComponent --> 718 violations'
]
</script>

<style scoped>
.key-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.metric-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-radius: 0.5rem;
  background-color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.icon {
  flex-shrink: 0;
}

.sparkline {
  width: 100px;
  height: 40px;
}
</style>






















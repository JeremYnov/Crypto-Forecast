<script setup lang="ts">
import { computed, defineComponent, onMounted, reactive, ref } from "vue";
import { Chart, registerables } from "chart.js";
import axios from "axios";
import { CHART_COLORS, months } from "../chartjs/Utils";
import DoughnutChart from "../components/DataVizualization/DoughnutChart.vue";
import LineChart from "../components/DataVizualization/LineChart.vue";

Chart.register(...registerables);

const numericData = ref(""); // use const because you dont want to lose this value
const loadingState = ref("");

// Fetch Data Feature
const fetchNumericData = () => {
  loadingState.value = "loading";
  return axios.get("/api/docs").then((response) => {
    loadingState.value = "success";
    numericData.value = JSON.parse(response.data.replace(/NaN/g, 0));
  });
};
onMounted(() => {
  fetchNumericData();
});
</script>

<template>
  <div style="width: 400px">
    <!-- <div>{{ characters }}</div> -->
    <DoughnutChart />
    <LineChart />
    <div v-for="(element, key) in numericData" :key="key">
      <p>TEST {{ key }} = {{ element }}</p>
    </div>
  </div>
</template>

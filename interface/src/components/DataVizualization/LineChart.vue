<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import { LineChart, useLineChart } from "vue-chart-3";
import axios from "axios";
import type { ChartData, ChartOptions } from "chart.js";

const low = ref([]);

const numericData = ref(null); // use const because you dont want to lose this value

// Fetch Data Feature
const fetchNumericData = async () => {
  return await axios.get("/api/docs").then((response) => {
    numericData.value = response.data.replace(/NaN/g, 0);
    console.log(numericData.value);
  });
};

onMounted(() => {
  fetchNumericData();
});

const getData = computed<ChartData<"line">>(() => ({
  labels: [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
  ],
  datasets: [
    {
      label: "Low",
      data: [
        65,
        59,
        80,
        81,
        56,
        55,
        40,
        65,
        59,
        80,
        81,
        56,
        55,
        40,
        65,
        59,
        80,
        81,
        56,
        55,
        40,
        65,
        59,
        80,
        81,
        56,
        55,
        40,
        65,
        59,
        80,
        81,
        56,
        55,
        40,
      ],
      fill: false,
      borderColor: "#4bc0c0",
    },
    {
      label: "High",
      data: [
        28,
        48,
        40,
        19,
        86,
        27,
        90,
        28,
        48,
        40,
        19,
        86,
        27,
        90,
        28,
        48,
        40,
        19,
        86,
        27,
        90,
        28,
        48,
        40,
        19,
        86,
        27,
        90,
        28,
        48,
        40,
        19,
        86,
        27,
        90,
      ],
      fill: false,
      borderColor: "#565656",
    },
  ],
}));

const options = computed<ChartOptions<"line">>(() => ({
  plugins: {
    title: {
      display: true,
      text: "Sentiment Analysis",
    },
  },
}));

const { lineChartProps } = useLineChart({
  options,
  chartData: getData,
});
</script>

<template>
  <LineChart v-bind="lineChartProps" />
</template>

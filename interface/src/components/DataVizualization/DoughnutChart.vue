<script setup lang="ts">
import { computed, ref } from "vue";
import { DoughnutChart, useDoughnutChart } from "vue-chart-3";
import type { ChartData, ChartOptions } from "chart.js";

const dataValues = ref([30, 40, 60]);
const dataLabels = ref(["Negative", "Positive", "Neutral"]);
const toggleLegend = ref(true);

const testData = computed<ChartData<"doughnut">>(() => ({
  labels: dataLabels.value,
  datasets: [
    {
      data: dataValues.value,
      backgroundColor: ["#FF0000", "#008000", "#808080"],
    },
  ],
}));

const options = computed<ChartOptions<"doughnut">>(() => ({
  scales: {
    myScale: {
      type: "logarithmic",
      position: toggleLegend.value ? "left" : "right",
    },
  },
  plugins: {
    legend: {
      position: toggleLegend.value ? "top" : "bottom",
    },
    title: {
      display: true,
      text: "Sentiment Analysis",
    },
  },
}));

const { doughnutChartProps, doughnutChartRef } = useDoughnutChart({
  chartData: testData,
  options,
});
</script>

<template>
  <DoughnutChart v-bind="doughnutChartProps" />
</template>

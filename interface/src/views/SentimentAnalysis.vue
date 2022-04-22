<script setup lang="ts">
import { computed, defineComponent, onMounted, reactive, ref } from "vue";
import { DoughnutChart, useDoughnutChart } from "vue-chart-3";
import { Chart, ChartData, ChartOptions, registerables } from "chart.js";
import axios from "axios";

const state = reactive({
  pokemons: [],
});

const fetchPokemon = () => {
  axios.get("https://pokeapi.co/api/v2/pokemon?offset=0").then((response) => {
    state.pokemons = response.data.results;
  });
};

fetchPokemon();

Chart.register(...registerables);

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
  <div style="width: 400px">
    <DoughnutChart v-bind="doughnutChartProps" />
    <div>{{ state.pokemons }}</div>
  </div>
</template>

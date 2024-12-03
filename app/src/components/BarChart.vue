<template>
  <div>
    <!-- <apexchart type="bar" :options="chartOptions" :series="series"></apexchart> -->
    <apexchart type="bar" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>

<script>
export default {
  name: "BarChart",
  props: {
    data: {
      type: Array,
      required: true,
    },
    labels: {
      type: Array,
      required: true,
    },
    title:{
      type:String,
      required:true
    }
  },
  computed: {
    chartOptions() {
      // Ensure processedData is available before using it
      if (!this.data || !this.labels) {
        return {};  // Return an empty object if processedData is not available yet
      }

      return {
        chart: {
          type: 'bar',
          toolbar: {
            show: false,
          },
        },
        xaxis: {
          categories: this.labels,
        },
        title: {
          text: this.title,
          align: 'center',
        },
        theme: {
          mode: this.$store.getters.isDarkTheme ? 'dark' : 'light',
        },
      };
    },
    series() {
      // Ensure processedData is available before using it
      if (!this.data || !this.labels) {
        return [];  // Return an empty array if influencerEarningsData is not available yet
      }

      return [
        {
          name: "Earnings",
          data: this.data,
        },
      ];
    },
  },
};
</script>

<style scoped>
.apexcharts-tooltip {
  color: #333;
}
.dark .apexcharts-tooltip {
  color: #f4f4f4;
}
</style>

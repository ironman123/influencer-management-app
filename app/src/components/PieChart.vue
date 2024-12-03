<template>
    <div>
      <apexchart type="pie" :options="chartOptions" :series="series"></apexchart>
    </div>
  </template>
  
  <script>
  export default {
    name: "PieChart",
    props: {
      data: {
        type: Array,
        required: true,
      },
      labels: {
        type: Array,
        required: true,
      },
      title: {
        type: String,
        required: true,
      },
    },
    computed: {
      chartOptions() {
        // Ensure data and labels are available before using them
        if (!this.data || !this.labels) {
          return {}; // Return an empty object if data is not available yet
        }
  
        return {
          chart: {
            type: 'pie',
          },
          labels: this.labels,
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
        // Ensure data is available before using it
        if (!this.data) {
          return []; // Return an empty array if data is not available yet
        }
  
        return this.data;
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
  
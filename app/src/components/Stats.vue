<template>
    <div :class="['stats-page', { dark: isDarkTheme }]">
      <!-- Tabs -->
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab" 
          @click="setActiveTab(tab)" 
          :class="[ { active: activeTab === tab }, { dark: isDarkTheme } ]"
        >
          {{ tab }}
        </button>
      </div>
      <div v-if="activeTab === 'Bar'" class="chart-section">
        <BarChart
          v-if="processedBarData.labels.length && processedBarData.data.length"
          :data="processedBarData.data"
          :labels="processedBarData.labels"
          :title="barTitle"
        />
        <p v-else>Loading...</p> <!-- Display loading message if data is not ready -->
      </div>
      <div v-if="activeTab === 'Pie'" class="chart-section">
        <PieChart
          v-if="processedPieData.labels.length && processedPieData.data.length"
          :data="processedPieData.data"
          :labels="processedPieData.labels"
          :title="pieTitle"
        />
      </div>
      <p v-else>Loading...</p> <!-- Display loading message if data is not ready -->
    </div>
  </template>
  
  <script>
  import { mapGetters } from "vuex";
  import BarChart from "./BarChart.vue"
  import PieChart from "./PieChart.vue"
  
  export default {
    name: "StatsPage",
    components: {
      BarChart,
      PieChart
    },
    data() {
        return {
          activeTab: "Bar",
          tabs: ['Bar','Pie'],
          barTitle:"",
          pieTitle:"",
          requests: [], // This will store the fetched requests
          influencerRequests: {
            accepted: 20,
            rejected: 10,
            completed: 15,
          },
          sponsorCompletedRequests: [],
        };
    },
    computed: {
      ...mapGetters(["isDarkTheme", "token","processedBarData","processedPieData","userType"]),
    },
    methods: {
      setActiveTab(tab) {
        this.activeTab = tab;
      },
    },
    mounted() {     
      
    },
    created(){
      if(this.userType == "Influencer"){
        this.barTitle = "Monthly Earnings"
        this.pieTitle = "Request Breakdown"
        this.$store.dispatch('processInfluencerBarData');
        this.$store.dispatch('processInfluencerPieData');
      }
      else if(this.userType == "Sponsor"){
        this.barTitle = "Requests Completed By Influencers"
        this.pieTitle = "Active Campaign Proportion"
        this.$store.dispatch('processSponsorBarData');
        this.$store.dispatch('processSponsorPieData');
        console.log(this.processedPieData)
      }
    },
    watch:{
    }
  };
  </script>
  
<style scoped>
    .stats-page {
        flex-grow: 1;
        padding: 0.25rem;
        min-height: 86vh;
        max-height: 86vh;
        overflow: auto;
        background: #f9f9f9;
        color: #333;
        transition: background 0.3s ease, color 0.3s ease;
    }
  
  .stats-page.dark {
    background: #1e1e1e;
    color: #f4f4f4;
  }
  
  .tabs {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .tabs button {
    padding: 0.5rem 1rem;
    border: none;
    background: #eee;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s ease, color 0.3s ease;
  }
  
  .tabs button.active {
    background: #555;
    color: white;
  }
  
  .tabs button.dark {
    background: #333;
    color: #f4f4f4;
  }
  
  .tabs button.active.dark {
    background: #4124e2;
    color: #fff;
  }
  
  .charts {
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }
  
  .chart-section {
    background: #f4f4f4;
    border-radius: 5px;
    padding: 1rem;
  }
  
  .chart-section.dark {
    background: #333;
  }
  </style>
  
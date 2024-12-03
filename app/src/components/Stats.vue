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
      <div v-if="activeTab === 'Influencer'" class="chart-section">
        <h2>Monthly Earnings</h2>
        <BarChart
          v-if="processedData.labels.length && processedData.data.length"
          :data="processedData.data"
          :labels="processedData.labels"
        />
        <p v-else>Loading...</p> <!-- Display loading message if data is not ready -->
      </div>
    </div>
  </template>
  
  <script>
  import { mapGetters } from "vuex";
  import BarChart from "./BarChart.vue"
  
  export default {
    name: "StatsPage",
    components: {
      BarChart
    },
    data() {
        return {
          activeTab: "Influencer",
          tabs: ["Influencer", "Sponsor"],
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
      ...mapGetters(["isDarkTheme", "token","processedData"]),
    },
    methods: {
      setActiveTab(tab) {
        this.activeTab = tab;
      },
      // processInfluencerBarData() {
      //     //if (!this.requests || this.requests.length === 0) {
      //     //  return { influencerEarnings: [], months: [] };
      //     //}

      //   const completedRequests = this.requests.filter(req => req.status === 'Completed');
      //   const monthlyEarnings = {};

      //   completedRequests.forEach(req => {
      //     const EndDate = new Date(req.end_date);
      //     const month = EndDate.toLocaleString("default", { month: "long", timeZone: "UTC" });
      //     console.log(month)
      //     if (!monthlyEarnings[month]) {
      //       monthlyEarnings[month] = 0;
      //     }
      //     monthlyEarnings[month] += req.paymentAmount;
          
      //   });

      //   const monthsData = Object.keys(monthlyEarnings);
      //   const influencerEarningsData = Object.values(monthlyEarnings);
      //   console.log("Processed Data:", { influencerEarningsData, monthsData });
      //   this.processedData = { influencerEarningsData, monthsData };
      // // Return processed data
      // },
      // async fetchRequests() {
      // try {
      //   const url = "http://127.0.0.1:5000/auth/requests";
      //   const headers = {
      //     "Content-Type": "application/json",
      //     "Authorization": this.token,
      //   };
      //   const response = await fetch(url, { method: "GET", headers });
      //   if (!response.ok) {
      //     throw new Error(`API error: ${response.status}`);
      //   }
      //   const data = await response.json();
      //   this.requests = data;
      //   // After fetching the requests, process the data
      //   } catch (error) {
      //     console.error("Failed to fetch requests:", error);
      //   }
      // },
    },
    mounted() {
      //this.fetchStats();
      
      
    },
    created(){
      this.$store.dispatch('processBarData');
    },
    watch:{
      processedData(v){
        console.log(v)
      }
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
  
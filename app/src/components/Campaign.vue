<template>
    <div class="campaign-page">
      <!-- Tabs -->
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab" 
          @click="setActiveTab(tab)" 
          :class="{ active: activeTab === tab }"
        >
          {{ tab }}
        </button>
      </div>
      <!-- Campaign List -->
      <div class="campaign-list">
        
        <CampaignCard
          v-for="campaign in filteredCampaigns" :key="campaign.id"
          :campaign="campaign"
          :userType="userType"
          :userName="userName"
          :userID="userID"
        />
        
      </div>
    </div>
  </template>
  
  <script>
  import {mapState} from 'vuex';
  import CampaignCard from './CampaignCard.vue';
  export default {
    name: "CampaignPage",
    props: {
      
    },
    components:{
      CampaignCard
    },
    data() {
      return {
        tabs: ["All", "My", "Active", "Completed"],
        activeTab: "All",
        campaigns: [],
      };
    },
    computed: {
      ...mapState(['userType','user','userName','userID','searchQuery']),
      filteredCampaigns() {
        let filtered = this.campaigns;
        
        // Filter by tab
        if (this.activeTab === "My") {
          filtered = filtered.filter((c) => c.owner === this.user);
          console.log("Filetered: ",filtered)
        } else if (this.activeTab !== "All") {
          filtered = filtered.filter((c) => c.status === this.activeTab);
          console.log("Filetered: ",filtered)
        }
  
        // Filter by search query
        if (this.searchQuery) {
          filtered = filtered.filter((c) =>
            c.name.toLowerCase().includes(this.searchQuery.toLowerCase())
          );
          console.log("Search Filtered: ",filtered)
        }
  
        return filtered;
      },
    },
    watch:{
    },
    mounted(){
      this.fetchCampaigns();
    },  
    methods: {
      setActiveTab(tab) {
        this.activeTab = tab;
      },
      async fetchCampaigns(){
        try{
          const url = 'http://127.0.0.1:5000/auth/campaigns'
          const headers = {
            "Content-Type":"application/json",
            "search-query":"yololo"
          }
          const response = await fetch(url,{
            method:"GET",
            headers:headers,
          });
          if(!response.ok)
          {
            throw new Error(`API error: ${response.status}`);
          }
          const data = await response.json();
          this.campaigns = data;
        }
        catch(error)
        {
          console.error("Failed to fetch campaigns:", error);
        }
      }
    },
  };
  </script>
  
  <style scoped>
  .campaign-page {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    padding: 0.25rem;
    min-height: 86vh;
    max-height: 86vh;
  }
  .tabs {
    display: flex;
    gap: 1rem;
  }
  .tabs button {
    padding: 0.5rem 1rem;
    cursor: pointer;
    border: none;
    background: #eee;
    border-radius: 5px;
  }
  .tabs button.active {
    background: #555;
    color: white;
  }
  .campaign-list {
    margin-top: 0.5rem;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
  }
  .campaign-item {
    background: #f4f4f4;
    border-radius: 5px;
  }
  </style>
  
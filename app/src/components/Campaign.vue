<template>
  <div :class="['campaign-page', { dark: isDarkTheme }]">
    <!-- Tabs -->
    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab" 
        @click="setActiveTab(tab)" 
        :class="[
          { active: activeTab === tab },
          { dark: isDarkTheme }
        ]"
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
        @edit-campaign="editCampaign"
        @toggle-flag="toggleFlag"
        @request-ad="requestAd"
      />
    </div>
    <button v-if="this.userType ==='Sponsor'" :class="['add-btn', { dark: isDarkTheme }]" @click="showAddCampaignForm = true">+</button>
    <CampaignForm 
      v-if="showAddCampaignForm" 
      :data="data"
      @close="closePopup"
    />
    <RequestForm
      v-if="showAddRequestForm"
      :data="data"
      @close="closePopup"
    />
  </div>
</template>

<script>
import { mapState, mapGetters } from "vuex";
import CampaignCard from "./CampaignCard.vue";
import CampaignForm from "./CampaignForm.vue";
import RequestForm from "./RequestForm.vue";

export default {
  name: "CampaignPage",
  components: {
    CampaignCard,
    CampaignForm,
    RequestForm
  },
  data() {
    return {
      data:null,
      activeTab: "All",
      campaigns: [],
      showAddCampaignForm: false,
      showAddRequestForm: false,
    };
  },
  computed: {
    ...mapState(["userType", "user", "userName", "userID", "searchQuery"]),
    ...mapGetters(["isDarkTheme","token"]),
    tabs() {
      const baseTabs = ["All", "Active", "Completed"];
      if (this.userType === "Sponsor") {
        baseTabs.push("My", "Private", "Flagged");
      } else if (this.userType === "admin") {
        baseTabs.push("Private", "Flagged");
      }
      return baseTabs;
    },
    filteredCampaigns() {
      let filtered = this.campaigns;

      // Filter by tab
      if (this.activeTab === "My") {
        filtered = filtered.filter((c) => c.ownerID === this.user);
      }
      else if(this.activeTab === "Private"){
        filtered = filtered.filter((c) => c.visibility === "private");
      }
      else if (this.activeTab === "Active") {
        filtered = filtered.filter((c) => c.status === "Active");
      }
      else if (this.activeTab === "Completed") {
        filtered = filtered.filter((c) => c.status === "Completed");
      }
      else if(this.activeTab === "Flagged"){
        filtered = filtered.filter((c) => c.status === "Flagged");
      }
      

      // Filter by search query
      if (this.searchQuery) {
        filtered = filtered.filter((c) =>
          c.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }

      return filtered;
    },
  },
  mounted() {
    this.fetchCampaigns();
  },
  methods: {
    editCampaign(d){
      this.showAddCampaignForm = true;
      this.data=d;
    },
    requestAd(d)
    {
      this.data = {
        selectedCampaign:`${d.id},${d.sponsor_id}`,
        from_:this.userID,
        campaign_id:d.id,
        requirements:'',
        status:'Pending'
      }
      this.showAddRequestForm = true;
    },
    closePopup(){
      this.showAddRequestForm = false;
      this.showAddCampaignForm = false;
      this.data=null;
    },
    setActiveTab(tab) {
      this.activeTab = tab;
    },
    async fetchCampaigns() {
      try {
        const url = "http://127.0.0.1:5000/auth/campaigns";
        const headers = {
          "Content-Type": "application/json",
          "Authorization":this.token,
          // "search-query": this.searchQuery,
        };
        const response = await fetch(url, {
          method: "GET",
          headers: headers,
        });
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        const data = await response.json();
        this.campaigns = data;
      } catch (error) {
        console.error("Failed to fetch campaigns:", error);
      }
    },
    async toggleFlag(campaign){
      try{
        const flag = campaign.status;
        const response = await fetch('http://127.0.0.1:5000/auth/campaigns', {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": this.token
                    },
                    body: JSON.stringify({ id:campaign.id,flag: flag }),
                });
                if (!response.ok) {
                    const error = await response.json();
                    console.error("Error updating flag:", error.message);
                    return;
                }
                const data = await response.json();
                
                // Update the local user flag
                
                campaign.status = data.flag;
      }
      catch(error)
      {
        console.error("Failed to fetch users:", error);
      }
    },
  },
};
</script>

<style scoped>
.add-btn {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  width: 3rem;
  height: 3rem;
  border: none;
  border-radius: 50%;
  background: #47c002;
  color: #fff;
  font-size: 1.5rem;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: background 0.3s ease;
}
.add-btn.dark{
  background: #4124e2;
}
.add-btn:hover {
  background: #4ed400;
}
.add-btn.dark:hover {
  background: #4d2ff7;
}
.campaign-page {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 0.25rem;
  min-height: 86vh;
  max-height: 86vh;
  background: #f9f9f9;
  color: #333;
  transition: background 0.3s ease, color 0.3s ease;
}

.campaign-page.dark {
  background: #1e1e1e;
  color: #f4f4f4;
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

.campaign-list {
  margin-top: 0.5rem;
  padding: 0.25rem;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.campaign-item {
  background: #f4f4f4;
  border-radius: 5px;
  transition: background 0.3s ease;
}

.campaign-item.dark {
  background: #333;
}
</style>

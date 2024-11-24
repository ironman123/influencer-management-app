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
      />
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from "vuex";
import CampaignCard from "./CampaignCard.vue";

export default {
  name: "CampaignPage",
  components: {
    CampaignCard,
  },
  data() {
    return {
      tabs: ["All", "My", "Active", "Completed"],
      activeTab: "All",
      campaigns: [],
    };
  },
  computed: {
    ...mapState(["userType", "user", "userName", "userID", "searchQuery"]),
    ...mapGetters(["isDarkTheme"]),
    filteredCampaigns() {
      let filtered = this.campaigns;

      // Filter by tab
      if (this.activeTab === "My") {
        filtered = filtered.filter((c) => c.owner === this.user);
      } else if (this.activeTab !== "All") {
        filtered = filtered.filter((c) => c.status === this.activeTab);
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
    setActiveTab(tab) {
      this.activeTab = tab;
    },
    async fetchCampaigns() {
      try {
        const url = "http://127.0.0.1:5000/auth/campaigns";
        const headers = {
          "Content-Type": "application/json",
          "search-query": "yololo",
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

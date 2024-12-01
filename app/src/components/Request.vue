<template>
  <div :class="['request-page', { dark: isDarkTheme }]">
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
    <!-- Request List -->
    <div class="request-list">
      <RequestCard
        v-for="request in filteredRequests" :key="request.id"
        :request="request"
        :userType="userType"
        :userName="userName"
        :userID="userID"
        @edit-request="editRequest"
        @update-status="updateCardStatus"
        @negotiate="negotiate"
      />
    </div>
    <button v-if="this.userType!=='admin'" :class="['add-btn', { dark: isDarkTheme }]" @click="showAddRequestForm = true">+</button>
    <RequestForm 
      v-if="showAddRequestForm" 
      :data="data"
      @close="closePopup"
    />
    <NegotiateForm
      v-if="showNegotiateForm"
      :adRequestId="adRequestId"
      @close="closePopup"
    />
  </div>
</template>

<script>
import { mapState, mapGetters } from "vuex";
import RequestCard from "./RequestCard.vue";
import RequestForm from "./RequestForm.vue";
import NegotiateForm from "./Negotiate.vue"

export default {
  name: "RequestPage",
  components: {
    RequestCard,
    RequestForm,
    NegotiateForm
  },
  data() {
    return {
      data:null,
      activeTab: "All",
      requests: [],
      adRequestId:null,
      showAddRequestForm: false,
      showNegotiateForm:false
    };
  },
  computed: {
    ...mapState(["userType", "user", "userName", "userID", "searchQuery"]),
    ...mapGetters(["isDarkTheme","token"]),
    tabs() {
      const baseTabs = ["All", "Accepted", "Pending", "Completed","Rejected"];
      return baseTabs;
    },
    filteredRequests() {
      let filtered = this.requests;
      console.log('Filtering')
      // Filter by tab
      if (this.activeTab === "Accepted") {
        filtered = filtered.filter((c) => c.status === "Accepted");
      }
      else if (this.activeTab === "Pending") {
        filtered = filtered.filter((c) => c.status === "Pending");
      }
      else if (this.activeTab === "Completed") {
        filtered = filtered.filter((c) => c.status === "Completed");
      }
      else if (this.activeTab === "Rejected") {
        filtered = filtered.filter((c) => c.status === "Rejected");
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
    this.fetchRequests();
  },
  methods: {
    editRequest(d){
      this.data=d;
      this.data.id =d.id
      this.data.selectedCampaign=`${d.campaign_id},${d.sponsor_id}`
      this.showAddRequestForm = true
    },
    negotiate(request){
      this.adRequestId = request.id;
      this.showNegotiateForm=true;
    },
    closePopup(){
      this.adRequestId=null;
      this.showNegotiateForm=false;
      this.showAddRequestForm = false;
      this.data=null;
    },
    setActiveTab(tab) {
      this.activeTab = tab;
    },
    async fetchRequests() {
      try {
        const url = "http://127.0.0.1:5000/auth/requests";
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
        this.requests = data;
      } catch (error) {
        console.error("Failed to fetch requests:", error);
      }
    },
    async updateCardStatus(request,status,rating=null)
    {
      try{
        const body = {id:request.id,status:status}
        if(rating !== null && status === 'Completed')
        {
          console.log('Rating added:', rating);
          body.rating=rating;  
        }
        console.log(body,' : ', status)
        const response = await fetch('http://127.0.0.1:5000/auth/requests',{
        method:"PUT",
        headers:{
          "Content-Type": "application/json",
          "Authorization": this.token
        },
        body:JSON.stringify(body)
        })  
        if(!response.ok)
        {
          const error = await response.json();
          console.error("Error Updating status",error.message);
          return;
        }
        const data = await response.json();
        request.status = data.status;
        if (rating !== null) 
        {
          console.log(`Rating of ${rating} successfully submitted.`);
        }
      }
      catch(error)
      {
        console.error("Failed to fetch users:", error);
      }
      
    }
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
.request-page {
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

.request-page.dark {
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

.request-list {
  margin-top: 0.5rem;
  padding: 0.25rem;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.request-item {
  background: #f4f4f4;
  border-radius: 5px;
  transition: background 0.3s ease;
}

.request-item.dark {
  background: #333;
}
</style>

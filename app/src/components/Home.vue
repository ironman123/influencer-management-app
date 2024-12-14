<template>
    <div :class="['home-page', { dark: isDarkTheme }]">
      <div v-if="this.userType == 'Influencer'">
        <h1>Total Earnings: {{ totalEarnings }} </h1>
        <h1>Monthly Earnings: {{ monthlyEarnings }} </h1>
        <h1>Average Rating: {{ averageInfluencerRating }} </h1>
        <!-- <h1>Average Rating: {{ this.rating }}</h1> -->
      </div>
      
      <div v-if="this.userType == 'admin'">
        <h2>New Sponsors</h2>
        <div class="user-list">
          <UserCard
            v-for="user in filteredSponsors" :key="user.id"
            :user="user"
            :userType="userType"
            :userName="userName"
            :userID="userID"
            @toggle-flag="toggleUserFlag"
          @authorize="authorizeUser"
          />
        </div>
      </div>
      
      <h2>Latest Campaigns</h2>
      <div class="campaign-list">
        <CampaignCard
          v-for="campaign in filteredCampaigns" :key="campaign.id"
          :campaign="campaign"
          :userType="userType"
          :userName="userName"
          :userID="userID"
          @editCampaign="editCampaign"
          @requestAd="requestAd"
          @toggle-flag="toggleCampaignFlag"
        />
      </div>
      
      <div v-if="this.userType != 'admin'">
        <h2>Recent Requests</h2>
        <div class="request-list">
        <RequestCard
          v-for="request in filteredRequests" :key="request.id"
            :request="request"
            :userType="userType"
            :userName="userName"
            :userID="userID"
            @editRequest="editRequest"
            @update-status="updateCardStatus"
            @negotiate="negotiate"
          />
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
          <NegotiateForm
              v-if="showNegotiateForm"
              :adRequestId="adRequestId"
              @close="closePopup"
          />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapState, mapGetters } from "vuex";
  import CampaignCard from "./CampaignCard.vue";
  import RequestCard from "./RequestCard.vue";
  import CampaignForm from "./CampaignForm.vue";
  import RequestForm from "./RequestForm.vue";
  import NegotiateForm from "./Negotiate.vue";
  import UserCard from "./UserCard.vue";
  
  export default {
    name: "HomePage",
    components: {
      CampaignCard,
      RequestCard,
      CampaignForm,
      RequestForm,
      NegotiateForm,
      UserCard
    },
    data() {
      return {
        campaigns: [],
        requests: [],
        sponsors:[],
        totalEarnings: 0,
        monthlyEarnings: 0,
        latestCampaigns: [],
        latestRequests: [],
        latestSponsors: [],
        showAddCampaignForm: false,
        showAddRequestForm: false,
        showNegotiateForm:false,
        adRequestId:null,
        data: null,
      };
    },
    computed: {
      ...mapState(["userType", "user", "userName", "userID",'searchQuery','months','influencerEarnings']),
      ...mapGetters(["isDarkTheme", "token"]),
      averageInfluencerRating(){
        const completedRequests = this.requests.filter((r) => r.status === 'Completed');
        if (completedRequests.length === 0) {
          return 0; // Return 0 if no completed requests
        }
        const totalRating = completedRequests.reduce((sum, request) => sum + Number(request.rating), 0);
        const avg = totalRating / completedRequests.length;
        return avg.toFixed(2);
      },
      filteredSponsors() {
        return this.latestSponsors.filter((user) =>
          user.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      },
      filteredCampaigns() {
        return this.latestCampaigns.filter((campaign) =>
          campaign.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          campaign.description.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      },
    
      filteredRequests() {
          return this.latestRequests.filter((request) =>
            request.campaignName.toLowerCase().includes(this.searchQuery.toLowerCase())
          );
        },
      },
    mounted() {
      this.fetchData();
    },
    methods: {
      async fetchData() {
        try {
          // Fetch campaigns and requests from the API
          await Promise.all([this.fetchCampaigns(), this.fetchRequests(),this.fetchUsers()]);
          
          // Get the latest 3 campaigns
          this.latestCampaigns = this.campaigns.filter((c)=>c.status !== 'Completed').slice(-3);
  
          // Get the latest requests
          this.latestRequests = this.requests.filter((r)=>r.status !== 'Completed').slice(-3);

          // Get the latest sponsors
          this.latestSponsors = this.sponsors.filter((s)=>s.flag !== 'Authorized').slice(-3);
  
          // Calculate total and monthly earnings
          this.calculateEarnings();
        } catch (error) {
          console.error("Failed to fetch data:", error);
        }
      },
      
      async fetchUsers(){
        try {
          const url = "http://127.0.0.1:5000/auth/users";
          const headers = {
            "Content-Type": "application/json",
            "Authorization":this.token,
            "search-query": this.searchQuery,
          };
          const response = await fetch(url, {
            method: "GET",
            headers: headers,
          });
          if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
          }
          const data = await response.json();
          this.sponsors = data.filter((s)=>s.userType === 'Sponsor');
        } catch (error) {
          console.error("Failed to fetch users:", error);
        }
      },

      async fetchCampaigns() {
        const url = "http://127.0.0.1:5000/auth/campaigns";
        const headers = {
          "Content-Type": "application/json",
          "Authorization": this.token,
        };
        try {
          const response = await fetch(url, { method: "GET", headers });
          if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
          }
          const data = await response.json();
          this.campaigns = data;
        } catch (error) {
          console.error("Failed to fetch campaigns:", error);
        }
      },
  
      async fetchRequests() {
        const url = "http://127.0.0.1:5000/auth/requests";
        const headers = {
          "Content-Type": "application/json",
          "Authorization": this.token,
        };
        try {
          const response = await fetch(url, { method: "GET", headers });
          if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
          }
          const data = await response.json();
          this.requests = data;
        } catch (error) {
          console.error("Failed to fetch requests:", error);
        }
      },
  
      calculateEarnings() {
        let total = 0;
        let monthly = 0;
        const currentMonth = new Date().getMonth();
  
        // Loop through requests to calculate earnings
        this.requests.forEach(request => {
          if (request.status === "Completed") {
            total += request.paymentAmount;
            
            const requestDate = new Date(request.start_date);
            if (requestDate.getMonth() === currentMonth) {
              monthly += request.paymentAmount;
            }
          }
        });
  
        // Update earnings in the component's data
        this.totalEarnings = total;
        this.monthlyEarnings = monthly;
      },
  
      // Handle editing a campaign
      editCampaign(d) {
        this.showAddCampaignForm = true;
        this.data = d;
      },
  
      // Handle requesting an ad for a campaign
        requestAd(d) {
          this.data = {
            selectedCampaign: `${d.id},${d.sponsor_id}`,
            from_: this.userID,
            campaign_id: d.id,
            requirements:'',
            status: 'Pending',
          };
          // You could trigger the modal to request the ad, for example
          this.showAddRequestForm = true;
        },
        negotiate(request)
        {
            this.adRequestId = request.id;
            this.showNegotiateForm=true;
        },
      // Handle editing a request
        editRequest(d) {
          this.data = { ...d }; // Copy the original data to avoid mutation
          this.data.selectedCampaign = `${d.campaign_id},${d.sponsor_id}`;
          this.showAddRequestForm = true;
        },
        closePopup(){
            this.adRequestId=null;
            this.showNegotiateForm=false;
            this.showAddRequestForm = false;
            this.showAddCampaignForm = false;
            this.data=null;
        },
        async toggleUserFlag(user){
          try {
                const flag = user.flag === "Authorized" ? "Flagged" : "Authorized";

              // Send PUT request to update the flag in the database
                const response = await fetch('http://127.0.0.1:5000/auth/users', {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": this.token
                    },
                    body: JSON.stringify({ id:user.id,flag: flag }),
                });

                if (!response.ok) {
                    const error = await response.json();
                    console.error("Error updating flag:", error.message);
                    return;
                }

                const data = await response.json();

                // Update the local user flag
                user.flag = data.flag;
            }catch (error) {
              console.error("Failed to fetch users:", error);
            }
        },
        async authorizeUser(user){
            try{
                const response = await fetch('http://127.0.0.1:5000/auth/users', {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": this.token
                    },
                    body: JSON.stringify({ id:user.id,flag:"Authorized" }),
                });

                if (!response.ok) {
                    const error = await response.json();
                    console.error("Error authorizing:", error.message);
                    return;
                }

                const data = await response.json();

                // Update the local user flag
                user.flag = data.flag;
            }catch(error) {
              console.error("Failed to fetch users:", error);
            }
        },
      // Handle updating the status of the request
    async updateCardStatus(request,status,rating=null)
    {
        try{
          const body = {id:request.id,status:status}
          if(rating !== null && status === 'Completed')
          {
            console.log('Rating added:', rating);
            body.rating=rating;  
          }
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
      },
      async toggleCampaignFlag(campaign){
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
  
      // Optional: API call to update the status in the backend
      async updateRequestStatusInBackend(requestId, newStatus) {
        const url = `http://127.0.0.1:5000/auth/requests`;
        const headers = {
          "Content-Type": "application/json",
          "Authorization": this.token,
        };
        const body = JSON.stringify({
          id: requestId,
          status: newStatus,
        });
        
        try {
          const response = await fetch(url, {
            method: "PUT",
            headers,
            body,
          });
          if (!response.ok) {
            throw new Error(`Failed to update status: ${response.status}`);
          }
          // Optionally, update any other parts of the UI
        } catch (error) {
          console.error("Failed to update request status:", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .home-page {
    flex-grow: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    padding: 0.25rem;
    min-height: 86vh;
    max-height: 86vh;
    background: #f9f9f9;
    color: #333;
    transition: background 0.3s ease, color 0.3s ease;
  }
  
  .home-page.dark {
    background: #1e1e1e;
    color: #f4f4f4;
  }
  
  h1, h2 {
    font-size: 1.5rem;
    margin: 1rem 0;
  }
  
  .campaign-list, .request-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .campaign-list {
    margin-top: 1rem;
  }
  
  .request-list {
    margin-top: 1rem;
  }
  </style>
  
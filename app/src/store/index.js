import { createStore } from 'vuex';

export default createStore({
  state: {
    // Initialize isDarkTheme with the value from localStorage or set it to false if not available
    isDarkTheme: JSON.parse(localStorage.getItem('isDarkTheme')) || false,
    searchQuery: "",
    isAuthenticated: localStorage.getItem('isAuthenticated') === 'true',
    user: localStorage.getItem('user') || null,
    userType: localStorage.getItem('userType') || null,
    userName: localStorage.getItem('userName') || null,
    token: localStorage.getItem('token') || null,
    userID: localStorage.getItem('userID') || null,

    processedBarData: {
      data: [],
      labels: [],
    },
    processedPieData: {
      data: [],
      labels: [],
    },
  },
  mutations: {
    setAuth(state, payload) {
      state.isAuthenticated = true;
      state.user = payload.email;
      state.userType = payload.userType;
      state.userName = payload.userName;
      state.token = payload.token;
      state.userID = payload.userID;

      localStorage.setItem('isAuthenticated', true);
      localStorage.setItem('user', payload.email);
      localStorage.setItem('userType', payload.userType);
      localStorage.setItem('token', payload.token);
      localStorage.setItem('userName', payload.userName);
      localStorage.setItem('userID', payload.userID);
    },
    resetAuth(state) {
      state.isAuthenticated = false;
      state.userType = null;
      state.token = null;
      state.userName = null;
      state.user = null;
      state.userID = null;

      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('userType');
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      localStorage.removeItem('userName');
      localStorage.removeItem('userID');
    },
    setProcessedBarData(state,payload)
    {
      state.processedBarData = payload;
      
    },
    setProcessedPieData(state,payload)
    {
      state.processedPieData = payload;
      
    },
    toggleDarkTheme(state) {
      state.isDarkTheme = !state.isDarkTheme;
      // Update localStorage whenever the theme is toggled
      localStorage.setItem('isDarkTheme', JSON.stringify(state.isDarkTheme));
      
    },
    setSearchQuery(state, query) {
      state.searchQuery = query;
    }
  },
  actions: {
    signIn({ commit }, data) {
      commit('setAuth', data);
    },
    signOut({ commit }) {
      commit('resetAuth');
    },
    toggleTheme({ commit }) {
      commit('toggleDarkTheme');
    },
    setSearchQuery({ commit }, query) {
      commit('setSearchQuery', query);
    },
    resetSearchQuery({ commit }) {
      commit('setSearchQuery', "");
    },
    async processInfluencerBarData({ commit,getters }){
      try {
        const url = "http://127.0.0.1:5000/auth/requests";
        const headers = {
          "Content-Type": "application/json",
          "Authorization": getters.token,
        };
        const response = await fetch(url, { method: "GET", headers });
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        const requests = await response.json();
        const completedRequests = requests.filter(req => req.status === 'Completed');
        const monthlyEarnings = {};

        completedRequests.forEach(req => {
          const EndDate = new Date(req.end_date);
          const month = EndDate.toLocaleString("default", { month: "long", timeZone: "UTC" });
          if (!monthlyEarnings[month]) {
            monthlyEarnings[month] = 0;
          }
          monthlyEarnings[month] += req.paymentAmount;
          
        });

        const labels = Object.keys(monthlyEarnings);
        const data = Object.values(monthlyEarnings);
        commit( 'setProcessedBarData',{ data, labels });
        // After fetching the requests, process the data
      } catch (error) {
        console.error("Failed to fetch requests:", error);
      }
    },
    async processInfluencerPieData({ commit,getters }){
      try {
        const url = "http://127.0.0.1:5000/auth/requests";
        const headers = {
          "Content-Type": "application/json",
          "Authorization": getters.token,
        };
        const response = await fetch(url, { method: "GET", headers });
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        const requests = await response.json();
        
        const statusCounts = {
          Completed: 0,
          Accepted: 0,
          Rejected: 0,
          Pending: 0,
        };
    
        // Process the requests data
        requests.forEach(req => {
          if (req.status in statusCounts) {
            statusCounts[req.status] += 1;
          }
        });
    
        // Prepare data and labels for the Pie Chart
        const labels = Object.keys(statusCounts);
        const data = Object.values(statusCounts);
        
        commit( 'setProcessedPieData',{ data, labels });
        // After fetching the requests, process the data
      } catch (error) {
        console.error("Failed to fetch requests:", error);
      }
    },
    async processSponsorBarData({ commit,getters }){
      try {
        const url = "http://127.0.0.1:5000/auth/requests";
        const headers = {
          "Content-Type": "application/json",
          "Authorization": getters.token,
        };
        const response = await fetch(url, { method: "GET", headers });
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        const requests = await response.json();
        const completedRequests = requests.filter(req => req.status === 'Completed');
        
        const influencerCompletionCount = {};
        
        completedRequests.forEach(req => {
          const influencerName = req.influencer; // Assuming `toUser` is the influencer's full name
          if (!influencerCompletionCount[influencerName]) {
            influencerCompletionCount[influencerName] = 0;
          }
          influencerCompletionCount[influencerName] += 1;
        });
        
        // Extract labels and data for the chart
        const labels = Object.keys(influencerCompletionCount);
        const data = Object.values(influencerCompletionCount);
        
        console.log({ labels, data });
        commit( 'setProcessedBarData',{ data, labels });
        // After fetching the requests, process the data
      } catch (error) {
        console.error("Failed to fetch requests:", error);
      }

    },
    async processSponsorPieData({ commit, getters }) {
      try {
        const url = "http://127.0.0.1:5000/auth/requests";
        const headers = {
          "Content-Type": "application/json",
          "Authorization": getters.token,
        };
        const response = await fetch(url, { method: "GET", headers });
    
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
    
        const requests = await response.json();
    
        // Initialize a mapping for campaign request counts
        const campaignRequests = {};
    
        // Current date to filter active campaigns
        const currentDate = new Date();
    
        requests.forEach(req => {
          const campaignEndDate = new Date(req.end_date);
    
          // Only consider active campaigns
          if (campaignEndDate >= currentDate) {
            const campaignName = req.campaignName;
    
            if (!campaignRequests[campaignName]) {
              campaignRequests[campaignName] = 0;
            }
            campaignRequests[campaignName] += 1;
          }
        });
    
        // Prepare data and labels for the Pie Chart
        const labels = Object.keys(campaignRequests);
        const data = Object.values(campaignRequests);
    
        // Commit the processed data to the Vuex store
        commit('setProcessedPieData', { data, labels });
      } catch (error) {
        console.error("Failed to fetch requests:", error);
      }
    }    
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
    userType: (state) => state.userType,
    token: (state) => state.token,
    user: (state) => state.user,
    userID: (state) => state.userID,
    userName: (state) => state.userName,
    isDarkTheme: (state) => state.isDarkTheme,
    searchQuery: (state) => state.searchQuery,
    processedBarData:(state)=>state.processedBarData,
    processedPieData:(state)=>state.processedPieData,
  },
});

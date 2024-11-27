<template>
    <div :class="['user-page', { dark: isDarkTheme }]">
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
      <!-- user List -->
      <div class="user-list">
        <UserCard
          v-for="user in filteredUsers" :key="user.id"
          :user="user"
          :userType="userType"
          :userName="userName"
          :userID="userID"
          @toggle-flag="toggleFlag"
          @authorize="authorize"
        />
      </div>
      
    </div>
  </template>
  
  <script>
  import { mapState, mapGetters } from "vuex";
  import UserCard from "./UserCard.vue";
  
  export default {
    name: "UserPage",
    components: {
      UserCard,
    },
    data() {
      return {
        activeTab: "All",
        tabs:['All','Influencer','Sponsor','Unauthorized','Authorized','Flagged'],
        users: [],
        showAdduserForm: false,
      };
    },
    computed: {
      ...mapState(["userType", "user", "userName", "userID", "searchQuery"]),
      ...mapGetters(["isDarkTheme","token"]),
      filteredUsers() {
        let filtered = this.users;
  
        // Filter by tab
        if (this.activeTab === "Authorized")
        {
            filtered = filtered.filter((c) => c.flag === "Authorized");
        }
        else if (this.activeTab === "Unauthorized")
        {
            filtered = filtered.filter((c) => c.flag === "Unauthorized");
        }
        else if (this.activeTab === "Flagged")
        {
            filtered = filtered.filter((c) => c.flag === "Flagged");
        }
        else if (this.activeTab !== "All") {
            filtered = filtered.filter((c) => c.userType === this.activeTab);
        }        

        console.log("Users: ",filtered)
  
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
      this.fetchUsers();
    },
    methods: {
        setActiveTab(tab) {
            this.activeTab = tab;
        },
        async fetchUsers() {
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
              this.users = data;
            } catch (error) {
              console.error("Failed to fetch users:", error);
            }
        },
        async toggleFlag(user) {
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
        async authorize(user){
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
  .user-page {
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
  
  .user-page.dark {
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
  
  .user-list {
    margin-top: 0.5rem;
    padding: 0.25rem;
    display: flex;
    max-width: 81vw;
    flex-direction: row;
    flex-wrap: wrap;
    overflow-y: auto;
    gap: 0.75rem;
  }
  
  .user-item {
    background: #f4f4f4;
    border-radius: 5px;
    transition: background 0.3s ease;
  }
  
  .user-item.dark {
    background: #333;
  }
  </style>
  
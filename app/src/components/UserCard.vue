<template>
  <div :class="['user-card card mb-3', { dark: isDarkTheme }]">
    <div :class="['card-header d-flex justify-content-between align-items-center', { dark: isDarkTheme }]">
      <!-- Card Title aligned to the start -->
      <h5 class="card-title mb-0">{{ user.name }}</h5>
      <div>  
        <!-- Status Badge aligned to the end with color changes based on the status -->
        <div>
          <span style="margin-right: 0.5rem;" :class="[ 
                  'badge', 
                  { 'bg-info': user.userType === 'Influencer', 
                    'bg-primary': user.userType === 'Sponsor' }, 
                  { dark: isDarkTheme } 
              ]"
          >
              {{ user.userType }}
          </span>
          <span :class="[ 
                  'badge', 
                  { 'bg-danger': user.flag === 'Flagged', 
                    'bg-warning': user.flag === 'Unauthorized', 
                    'bg-success': user.flag === 'Authorized' }, 
                  { dark: isDarkTheme } 
              ]"
          >
              {{ user.flag }}
          </span>
        </div>
      </div>
    </div>
    <div :class="['card-footer d-flex justify-content-between align-items-center', { dark: isDarkTheme }]">
      <!-- Buttons on the left -->
      <div>
        <button
          v-if="isAdmin"
          class="btn btn-secondary btn-sm"
          @click="toggleFlag"
        >
          Toggle Flag
        </button>
        <button
          v-if="isAdmin && user.userType === 'Sponsor' && user.flag === 'Unauthorized'"
          class="btn btn-success btn-sm"
          @click="authorize"
        >
          Authorize
        </button>
      </div>
      <!-- Rating on the right -->
      <div v-if="user.userType=='Influencer'" style="margin-left: auto;">
        <span style="font-size: 1.1em; color: yellow;">⭐</span>{{ user.rating }}
      </div>
    </div>
  </div>
</template>

  
<script>
  import { mapGetters } from 'vuex';
  export default {
    name: "UserCard",
    props: {
      user: {
        type: Object,
        required: true,
      },
      userType: {
        type: String, // e.g., 'admin', 'sponsor', 'influencer'
        required: true,
      },
      userName: {
        type: String,
        required: true,
      },
      userID: {
        type: String,
        required: true,
      },
    },
    computed: {
      ...mapGetters(['isDarkTheme']),
      isSponsor() {
        return this.user.sponsor_id === Number(this.userID);
      },
      isAdmin() {
        return this.userType === "admin";
      },
      isInfluencer() {
        return this.userType === "influencer";
      },
    },
    methods: {
      formatDate(date) {
        const options = { year: "numeric", month: "long", day: "numeric" };
        return new Date(date).toLocaleDateString(undefined, options);
      },
      toggleFlag() {
        this.$emit('toggle-flag',this.user);
      },
      authorize(){
        this.$emit('authorize',this.user);
      }
    },
  };
</script>
  
  <style scoped>
  .user-card {
    min-height: 6rem;
    border: 1px solid #ddd;
    border-radius: 0.25rem;
    width: 20rem;
    transition: background 0.3s ease, color 0.3s ease;
  }
  
  .user-card.dark {
    background-color: #333;
    color: #f4f4f4;
  }
  
  .card-header {
    background-color: #f8f9fa;
  }
  
  .card-header.dark {
    background-color: #444;
  }
  
  .card-body {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  
  .card-body.dark {
    background-color: #444;
  }
  
  .card-footer {
    display: flex;
    flex-direction: row;
    background-color: #f8f9fa;
  }
  
  .card-footer.dark {
    background-color: #444;
  }
  
  .badge {
    font-size: 0.8rem;
    padding: 0.5em;
  }
  
  .badge.dark {
    color: #f4f4f4;
  }
  
  .btn {
    margin-right: 0.5em;
  }
  
  .card-text {
    overflow: auto;
    text-overflow: ellipsis;
    /* word-break: break-word;
    word-wrap: break-word; */
    max-width: 60rem;
    max-height: 6rem;
  }
  
  .card-text::-webkit-scrollbar {
    display: none;
  }
  
  .card-text.dark {
    color: #f4f4f4;
  }
  </style>
  
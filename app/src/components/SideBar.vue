<template>
  <div :class="['sidebar', { collapsed: isCollapsed }, {dark: isDarkTheme}]">
    <button @click="toggleSidebar" class="toggle-btn">
      <img src="/sidebaricons/toggle.png" alt="Toggle" height="30vh"/>
    </button>
    <div class="sidebar-items">
      <SidebarItem
        v-for="item in filteredItems"
        :key="item.name"
        :name="item.name"
        :icon="item.icon"
        :isCollapsed="isCollapsed"
        @click="handleItemClick(item.name)"
      />
    </div>
  </div>
</template>

<script>
  import SidebarItem from './SidebarItem.vue';
  import { mapGetters } from 'vuex';
  export default{
    name: 'SideBar',
    props:{
    },
    data(){
      return {
        isCollapsed: false,
        items: [
          { name: 'Home', icon: '/sidebaricons/home.png', route: '/home', roles: ['admin', 'Influencer', 'Sponsor'] },
          { name: 'Users', icon: '/sidebaricons/users.png', route: 'users', roles: ['admin'] },
          { name: 'Campaigns', icon: '/sidebaricons/campaigns.png', route: 'campaigns', roles: ['admin','Influencer','Sponsor'] },
          { name: 'Requests', icon: '/sidebaricons/requests.png', route: 'requests', roles: ['admin','Influencer','Sponsor'] },
          { name: 'Settings', icon: '/sidebaricons/settings.png', route: '/settings', roles: ['admin', 'Influencer'] },
          { name: 'Profile', icon: '/sidebaricons/profile.png', route: '/profile', roles: ['admin', 'Influencer', 'Sponsor'] },
          
        ],
      }
    },
    methods:{
      toggleSidebar(){
        this.isCollapsed = !this.isCollapsed;
      },
      handleItemClick(route){
        this.$emit('changePage',route)
      }
    },
    computed: {
      ...mapGetters(['userType','isDarkTheme']),
      filteredItems() {
        return this.items.filter((item) => item.roles.includes(this.userType));
      },
    },
    components:{
      SidebarItem
    }
  }
</script>

<style scoped>
  .sidebar {
    width: 15rem;
    transition: width 0.3s ease;
    background-color: #f4f4f4;
    /* color:rgb(21, 40, 56); */
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
  }
  .sidebar.collapsed {
    width: 3.75rem;
  }

  .sidebar.dark {
    background-color: #1e1e1e;
    color: #cad7d8;
  }
  .sidebar.dark .toggle-btn {
    filter: brightness(0.95);
  }
  .toggle-btn {
    margin-bottom: 1rem;
    cursor: pointer;
    align-self: flex-end;
    background: none;
    border: none;
    outline: none;
    padding: 0;

  }
  .sidebar-items {
    display: flex;
    flex-direction: column;
    gap: 1.75rem;
    align-self: flex-start;
    margin-top: 1rem;
  }
</style>
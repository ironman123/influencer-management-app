<template>
    <div :class="{ 'dark-theme': isDarkTheme }" id="page-container">
        <NavBar 
          :isDarkTheme="isDarkTheme" 
          @toggle-theme="toggleTheme"
          @sign-out="console.log('Signout Caught at Container')"
        />
      
        <main>
          <div class="page-content">
            <router-view :isDarkTheme="isDarkTheme" :userRole="userRole"/> <!-- This Renders SignIn/Dashboard Conditionally-->
          </div>
        </main>

        <footer>
            <p>Footer content here</p>
        </footer>
    </div>
</template>
  
<script>
  import NavBar from './Navbar.vue';
  // import DashBoard from './DashBoard.vue';
  
  export default {
    name: "PageContainer",
    components: {
      NavBar,
      // DashBoard
    },
    data() {
      return {
        isDarkTheme: false,
        userRole: 'influencer'
      };
    },
    methods: {
      toggleTheme() {
        this.isDarkTheme = !this.isDarkTheme;
      },
    },
  };
</script>
  
<style scoped>
    #page-container {
        font-family: Arial, sans-serif;
        color: #333;
        display: flex;
        flex-direction: column;
        min-height: 100vh; /* Full viewport height */
    }
  
    main {
        flex-grow: 1;
        padding: 0;
        /* min-height: 86vh; */
        max-height: 86vh;
        overflow-y: auto;
    }
    .page-content {
        flex-grow: 1;
        /* padding: 2px; */
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 81vh;   
    }

        
    footer {
        padding: 3px;
        background-color: #c7c7c7;
        text-align: center;
        max-height: 5vh;
    }

    .dark-theme {
        background-color: #313131;
        color: #f1f1f1;
    }

    .dark-theme main {
        color: #f1f1f1; /* White text color */
    }
</style>
  
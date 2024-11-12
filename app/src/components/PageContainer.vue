<template>
    <div :class="{ 'dark-theme': isDarkTheme }" id="page-container">
      <NavBar :isDarkTheme="isDarkTheme" @toggle-theme="toggleTheme" />
      
      <main>
        <div>
            <router-view />
        </div>
      </main>

      <footer>
        <p>Footer content here</p>
      </footer>
    </div>
</template>
  
<script>
  import NavBar from './Navbar.vue';
  
  export default {
    name: "PageContainer",
    components: {
      NavBar,
    },
    data() {
      return {
        isDarkTheme: false,
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
        flex-grow: 1; /* Takes remaining space */
        padding: 20px;
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
  
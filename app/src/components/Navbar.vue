<template>
    <nav class="navbar">
        <div class="left-content content" >
            <img src="../assets/logo.png" alt="logo" height="36vh" style="margin-right: 45px;">
            <a>Aasdasdad</a>
            <a>A asda</a>
            
        </div>
        <div v-if="isAuthenticated" class="center-content" style="min-width: 100px; margin-left: auto; margin-right: 3rem">
            <div class="form-inline search-bar" style="display: flex;">
                <input 
                    class="form-control mr-sm-2" 
                    style="margin-right: 1vh;" 
                    type="search" 
                    placeholder="Search..." 
                    aria-label="Search" 
                    v-model="searchQuery" 
                >
            </div>
        </div>
        <div class="right-content content" >
            <button @click="toggleTheme" class="theme-toggle" style=" display: flex; align-items: center; ">
                <img :src="isDarkTheme ? sunIcon : moonIcon" :alt="isDarkTheme ? 'Light Mode' : 'Dark Mode'" class="theme-icon" height=33vh/>
                <!-- {{ isDarkTheme ? 'Light Mode' : 'Dark Mode' }} -->
            </button>
            <router-link v-if="!isAuthenticated && $route.path !== '/register'" to="/register"><button class="btn btn-primary">Register</button></router-link>
            <router-link v-if="!isAuthenticated && $route.path !== '/'" to="/"><button class="btn btn-warning">Sign In</button></router-link>
            <button v-if="isAuthenticated" @click="signOut" class="btn btn-danger">Sign Out</button>
        </div>

    </nav>
    
</template>

<script>
    import sunIcon from '@/assets/sun.png';
    import moonIcon from '@/assets/moon.png';
    import {mapGetters,mapActions,mapState} from 'vuex';

    export default {
        name: "NavBar",
        props:{
            
        },
        data()
        {
            return{
                sunIcon,
                moonIcon,   
            }
        },
        computed:{
            ...mapState(['searchQuery']),
            ...mapGetters(['isAuthenticated','isDarkTheme']),
            searchQuery: {
                get() {
                    return this.$store.state.searchQuery; // Get searchQuery from Vuex state
                },
                set(value) {
                    this.setSearchQuery(value); // Dispatch Vuex action to update searchQuery
                },
            },
        },
        created(){
        },
        methods:
        {
            ...mapActions(['toggleTheme','setSearchQuery']),
            signOut() {
                this.$store.dispatch('signOut');
                this.$router.push('/');
            },
            
        },
        watch:
        {

        }
    }
</script>

<style scoped>
    .navbar 
    {
        height: 9vh;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-direction: row;
        padding: 10px;
        background-color: #555;
        color: white;
    }
    .content
    {
        display: flex;
        align-items: center;
        padding: 0 4.5vh;
    }
    
    .theme-toggle 
    {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        margin-right: 15px;
    }
    .navbar a 
    {
        margin-left: 15px;
        color: white;
        text-decoration: none;
    }
    .navbar a:hover 
    {
        text-decoration: underline;
    }

</style>
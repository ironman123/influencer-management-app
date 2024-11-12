<template>
    <nav class="navbar">
        <div class="left-content content" >
            <img src="../assets/logo.png" alt="logo" height="36vh" style="margin-right: 45px;">
            <a>Aasdasdad</a>
            <a>A asda</a>
            <a>Adasdasdsad sad</a>
        </div>
        <div class="right-content content" >
            <button @click="toggleTheme" class="theme-toggle" style=" display: flex; align-items: center; ">
                <img :src="isDarkTheme ? sunIcon : moonIcon" :alt="isDarkTheme ? 'Light Mode' : 'Dark Mode'" class="theme-icon" height=33vh/>
                <!-- {{ isDarkTheme ? 'Light Mode' : 'Dark Mode' }} -->
            </button>
            <router-link v-if="$route.path !== '/register'" to="/register">Register</router-link>
            <router-link v-if="$route.path !== '/'" to="/">Sign In</router-link>
        </div>

    </nav>
    
</template>

<script>
    import sunIcon from '@/assets/sun.png';
    import moonIcon from '@/assets/moon.png';

    export default {
        name: "NavBar",
        data()
        {
            return{
                sunIcon,
                moonIcon
            }
        },
        props:
        {
            isDarkTheme: Boolean,        
        },
        methods:
        {
            toggleTheme()
            {
                this.$emit("toggle-theme");
            }
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
        padding: 0 6vh;
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
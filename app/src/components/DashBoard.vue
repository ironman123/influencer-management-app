<template>
    <div id="dashboard">
        <SideBar 
            id="side-bar" 
            @changePage="navigatePage" 
            :isDarkTheme="isDarkTheme"
            :userRole="userRole"
        >
        </SideBar>
        <router-view
            id="page-content"
            :isDarkTheme="isDarkTheme"
            >
        </router-view>
        
    </div>
</template>

<script>
    import SideBar from './SideBar.vue'
    
    export default{
        name: "DashBoard",
        props:{
            isDarkTheme:{
                type:Boolean,
                default: false,
            },
            userRole: {
                type: String,
                default: 'admin',
                required: true,
            },
        },
        data(){
            return{
                currentPage: 'Home',
            }
        },
        components:{
            SideBar,
        },
        methods:{
            navigatePage(route) {
                this.$router.push(route);
            },
        }
    }
</script>

<style scoped>
    #dashboard
    {
        display: flex;
        min-height: 86vh;
        min-width: 100vw;
    }
    #page-content
    {
        flex-grow: 1;
    }
</style>
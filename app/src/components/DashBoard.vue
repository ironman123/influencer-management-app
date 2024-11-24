<template>
    <div id="dashboard">
        <SideBar 
            id="side-bar" 
            @changePage="navigatePage" 
        >
        </SideBar>
        <router-view
            id="page-content"
            >
        </router-view>
        
    </div>
</template>

<script>
    import SideBar from './SideBar.vue'
    import { mapGetters } from 'vuex';
    
    export default{
        name: "DashBoard",
        props:{
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
        },
        computed:{
            ...mapGetters(['isDarkTheme'])
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
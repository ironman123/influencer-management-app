<template>
    <div id="dashboard">
        <SideBar id="side-bar"></SideBar>
        <PageContent id="page-content"></PageContent>
    </div>
</template>

<script>
    import SideBar from './SideBar.vue'
    import PageContent from './PageContent.vue';
    export default{
        name: "DashBoard",
        props:{
            isDarkTheme:{
                type:Boolean,
                default: false,
            }
        },
        data(){
            return{

            }
        },
        components:{
            SideBar,
            PageContent
        }
    }
</script>

<style scoped>
    #dashboard
    {
        display: flex;
        background-color: aqua;
        min-height: 86vh;
        min-width: 100vw;
    }
    #page-content
    {
        flex-grow: 1;
    }
</style>
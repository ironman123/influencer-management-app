import Vue from 'vue';
import Router from 'vue-router';
import SignIn from './components/SignIn.vue';
import RegisterForm from './components/Register.vue';
//import PageContainer from './components/PageContainer.vue';


Vue.use(Router);

const isAuthenticated = false;

const routes = [
    {
        path: '/',
        component: isAuthenticated ? RegisterForm : SignIn
    },
    {
        path: '/register', 
        component: RegisterForm
    }
    
];

export default new Router({
    mode: 'history',
    routes
});
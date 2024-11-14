import Vue from 'vue';
import Router from 'vue-router';
import SignIn from './components/SignIn.vue';
import RegisterForm from './components/Register.vue';
import DashBoard from './components/DashBoard.vue';


Vue.use(Router);

const isAuthenticated = true;

const routes = [
    {
        path: '/',
        component: isAuthenticated ? DashBoard : SignIn
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
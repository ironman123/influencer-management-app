import Vue from 'vue';
import Router from 'vue-router';
import HomePage from './components/Home.vue';
import AboutPage from './components/About.vue';

Vue.use(Router);

const routes = [
    { path: '/', component: HomePage },
    { path: '/about', component: AboutPage }
];

export default new Router({
    mode: 'history',
    routes
});
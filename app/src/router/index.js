// router.js
import { createRouter, createWebHistory } from 'vue-router';
import SignIn from '../components/SignIn.vue';
import RegisterForm from '../components/Register.vue';
import DashBoard from '../components/DashBoard.vue';
import store from '../store'


const routes = [
  {
    path: '/',
    component: SignIn,
    beforeEnter:(to,from,next)=>{
      if (store.state.isAuthenticated) {
        next('/dashboard');
      } else if (from.path !== '/'){
        next();
      } else{
        next();
      }
    },
  },
  {
    path: '/dashboard',
    component: DashBoard,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/register',
    component: RegisterForm,
  },
];

const router = createRouter({
  history: createWebHistory(),  // Use createWebHistory for Vue 3
  routes,
});

router.beforeEach((to, from, next) => {
  
  next();
});

export default router;

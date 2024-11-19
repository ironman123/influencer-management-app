// router.js
import { createRouter, createWebHistory } from 'vue-router';
import SignIn from '../components/SignIn.vue';
import RegisterForm from '../components/Register.vue';
import DashBoard from '../components/DashBoard.vue';
import store from '../store'


let count = 10;

setInterval(()=>{console.log(store.state.isAuthenticated)},1000)

const routes = [
  {
    path: '/',
    beforeEnter:(to,from,next)=>{
      if (store.state.isAuthenticated) {
        next('/dashboard');
      } else if (from.path !== '/'){
        next();
      } else{
        next();
      }
    },
    component: SignIn,
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
  console.log(count++);
  next();
});

export default router;

// router.js
import { createRouter, createWebHistory } from 'vue-router';
import SignIn from '../components/SignIn.vue';
import RegisterForm from '../components/Register.vue';
import DashBoard from '../components/DashBoard.vue';
import store from '../store'
import CampaignPage from '@/components/Campaign.vue';
import RequestPage from '@/components/Request.vue';
import UserPage from '@/components/Users.vue';
import HomePage from '@/components/Home.vue'


const routes = [
  {
    path: '/',
    component: SignIn,
    // beforeEnter:(to,from,next)=>{
    //   if (store.state.isAuthenticated) {
    //     next('/dashboard');
    //   } else{
    //     next();
    //   }
    // },
    children:[
          
    ]
  },
  {
    name:'Dashboard',
    path: '/dashboard',
    component: DashBoard,
    props: true,
    meta: { requiresAuth: true },
    children:[
      {
        name:'Home',
        path: '',
        component: HomePage,
        props: true,
        meta: { requiresAuth: true },
      },
      {
        name:'Campaigns',
        path: 'campaigns',
        component: CampaignPage,
        props: true,
        meta: { requiresAuth: true },
      },
      {
        name:'Requests',
        path: 'requests',
        component: RequestPage,
        props: true,
        meta: { requiresAuth: true },
      },
      {
        name:'Users',
        path: 'users',
        component: UserPage,
        props: true,
        meta: { requiresAuth: true },
      }
    ]
  },
  {
    path: '/register',
    component: RegisterForm,
  },
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

async function validateToken() {
  const token = localStorage.getItem("token");
  if (!token) return false;
  console.log(token);
  try {
    const response = await fetch("http://127.0.0.1:5000/auth/check-token", {
      method: "GET",
      headers: {
        Authorization: token,
      },
    });

    if (response.ok) {
      const data = await response.json();
      console.log("Token validation success:", data);
      return true;
    } else {
      console.warn("Token validation failed.");
      return false;
    }
  } catch (error) {
    console.error("Error validating token:", error);
    return false;
  }
}

router.beforeEach(async(to, from, next) => {
  const isAuthenticated = await validateToken();
  console.log(isAuthenticated);
  if (to.meta.requiresAuth) 
  {    
    if (!isAuthenticated) {
      store.dispatch('signOut')
      next("/"); // Redirect to login
    }
    
  }
  else if (isAuthenticated && to.path === '/')
  {
    next('/dashboard')
  }
  
  next();
});

export default router;

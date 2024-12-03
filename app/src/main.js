import { createApp } from 'vue'
import App from './App.vue'
import store from './store';
import router from './router';
import VueApexCharts from 'vue3-apexcharts';
import 'bootstrap/dist/css/bootstrap.min.css';

//setInterval(()=>{console.log('isAuth in Main:',store.state.isAuthenticated)},1000)

// createApp(App)
// .use(store)
// .use(router)
// .mount('#app')

const app = createApp(App);

app
  .use(store) // Add the Vuex store
  .use(router) // Add the Vue Router
  .use(VueApexCharts) // Add Vue-ApexCharts
  .component('apexchart', VueApexCharts) // Register the ApexCharts component globally
  .mount('#app'); // Mount the app

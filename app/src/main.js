import { createApp } from 'vue'
import App from './App.vue'
import store from './store';
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css';

//setInterval(()=>{console.log('isAuth in Main:',store.state.isAuthenticated)},1000)

createApp(App)
.use(store)
.use(router)
.mount('#app')

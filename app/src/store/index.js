// store.js
import { createStore } from 'vuex';

export default createStore({
  state: {
    isAuthenticated: localStorage.getItem('isAuthenticated') === 'true',
    user: localStorage.getItem('user') || null,
    userType: localStorage.getItem('userType') || null,
    token: localStorage.getItem('token') || null
  },
  mutations: {
    setAuth(state,payload) {
      state.isAuthenticated = true;
      state.user = payload.email;
      state.userType = payload.user_type;
      state.token = payload.token;

      localStorage.setItem('isAuthenticated',true);
      localStorage.setItem('user',payload.email);
      localStorage.setItem('userType',payload.user_type);
      localStorage.setItem('token',payload.token);
    },
    resetAuth(state){
      state.isAuthenticated = false;
      state.userType = null;
      state.token = null;
      state.user = null;

      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('userType');
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      
    }
  },
  actions: {
    signIn({commit},data){
      commit('setAuth',data);
    },
    signOut({ commit }) {
      commit('resetAuth');
    },
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
    userType: (state) => state.userType,
    token: (state) => state.token,
    user: (state)=> state.user,
  },
});

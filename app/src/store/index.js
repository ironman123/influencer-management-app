// store.js
import { createStore } from 'vuex';

export default createStore({
  state: {
    isAuthenticated: localStorage.getItem('isAuthenticated') === 'true',
    userType: localStorage.getItem('userType') || null,
    token: localStorage.getItem('token') || null
  },
  mutations: {
    setAuth(state,payload) {
      state.isAuthenticated = true;
      state.userType = payload.user_type;
      state.token = payload.token;

      localStorage.setItem('isAuthenticated',true);
      localStorage.setItem('userType',payload.user_type);
      localStorage.setItem('token',payload.token);
    },
    resetAuth(state){
      state.isAuthenticated = false;
      localStorage.clear();
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
  },
});

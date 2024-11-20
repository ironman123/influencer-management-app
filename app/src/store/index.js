// store.js
import { createStore } from 'vuex';

export default createStore({
  state: {
    isAuthenticated: localStorage.getItem('isAuthenticated') === 'true',
  },
  mutations: {
    setAuth(state,status) {
      state.isAuthenticated = status;
      localStorage.setItem('isAuthenticated',status);
    },
  },
  actions: {
    signIn({commit}){
      commit('setAuth',true);
    },
    signOut({ commit }) {
      commit('setAuth',false);
    },
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
  },
});

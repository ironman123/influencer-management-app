// store.js
import { createStore } from 'vuex';

export default createStore({
  state: {
    isAuthenticated: false,
  },
  mutations: {
    setAuthenticated(state) {
      state.isAuthenticated = true;
    },
    clearAuthentication(state) {
      state.isAuthenticated = false;
    },
  },
  actions: {
    signIn({commit}){
      commit('setAuthenticated');
    },
    signOut({ commit }) {
      commit('clearAuthentication');
    },
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
  },
});

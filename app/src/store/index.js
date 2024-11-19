// store.js
import { createStore } from 'vuex';

export default createStore({
  state: {
    isAuthenticated: true,
  },
  mutations: {
    setAuthenticated(state, value) {
      state.isAuthenticated = value;
    },
    clearAuthentication(state) {
      state.isAuthenticated = false;
    },
  },
  actions: {
    signOut({ commit }) {
      commit('clearAuthentication');
    },
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
  },
});

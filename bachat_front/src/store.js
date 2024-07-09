import { createStore } from 'vuex';

export default createStore({
  state: {
    isLoggedIn: false
  },
  mutations: {
    setLoggedIn(state, status) {
      state.isLoggedIn = status;
    }
  },
  actions: {
    login({ commit }) {
      commit('setLoggedIn', true);
    },
    logout({ commit }) {
      commit('setLoggedIn', false);
    }
  }
});

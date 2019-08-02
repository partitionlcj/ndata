import Vue from 'vue';
import aisTool from 'ais-components';
import api from '../../api/index';

const state = {
  name: '',
  role: '',
}

const getters = {
  hasInfo(state) {
    return Boolean(aisTool.Cookie.getData("ops-role") == "ROLE_NDATA_USER");
  }
}

const actions = {
  async login({ commit }) {
    let name = aisTool.Cookie.getData("ops-name")
    let role = aisTool.Cookie.getData("ops-role")
    commit('LOGIN', { name, role });
    return role;
  }
};

const mutations = {
  LOGIN(state, info) {
    state.name = info.name;
    state.role = info.role;
  },
  LOGOUT(state, info) {
    aisTool.Cookie.delData('ops-name');
    aisTool.Cookie.delData('ops-role');
    aisTool.Cookie.delData('mars_token');
    state.name = '';
    state.role = '';
  }
};

export default {
  state,
  getters,
  actions,
  mutations
}

import api from '../../api';

const state = {
  domains: [],
  envs: []
}

const getters = {}

const actions = {
  async getMeta({ state, commit }) {
    if (state.domains.length === 0) {
      let data = await api.getMeta();
      let domains = data.data.domain;
      commit('SET_DOMAIN', domains);
    }
  },
  async getEnv({ state, commit }) {
    if (state.envs.length === 0) {
      let response = await api.config('ops-env');
      const envs = response['ops-env'];
      commit('SET_ENV', envs);
    }
  }
};

const mutations = {
  SET_DOMAIN(state, domains) {
    state.domains = domains;
  },
  SET_ENV(state, envs) {
    state.envs = envs;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
}

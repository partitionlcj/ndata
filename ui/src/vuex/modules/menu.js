import route from '../../config/menu';

//state
const state = {
  menu: null,
  crumb: [],
  labelText: ''
};

//创建getters
const getters = {}

//创建actions
const actions = {}

//提交状态改变
const mutations = {
  BREADCRUMB(state, crumb) {
    state.crumb = crumb;
  },
  SET_AUTH_MENU(state) {
    state.menu = route.base;
  },
  SET_LABEL_TEXT(state, text) {
    state.labelText = text;
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}

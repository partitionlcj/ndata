import Vue from 'vue';
import Vuex from 'vuex';
import menu from './modules/menu.js';
import user from './modules/user';
import meta from './modules/meta';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    menu,
    user,
    meta
  }
});

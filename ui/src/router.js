import Vue from 'vue';
import VueRouter from 'vue-router';
import store from './vuex';
import aisTool from 'ais-components';
import util from './util/index';

Vue.use(VueRouter);

// 定义一个能够被 Webpack 自动代码分割的异步组件
//导航栏
const Main = () =>
  import('./views/main');
const Summary = () =>
  import( /* webpackChunkName: "report" */ './views/report/Summary');
const FbIntentReport = () =>
  import( /* webpackChunkName: "report" */ './views/report/FbIntentReport');
const FbQueryDetail = () =>
  import( /* webpackChunkName: "report" */ './views/report/FbQueryDetail');
const FbQueryDetailDebug = () =>
  import( /* webpackChunkName: "report" */ './views/report/FbQueryDetailDebug');
const FbVosDebug = () =>
  import( /* webpackChunkName: "report" */ './views/report/FbVosDebug');
const FbAsrDebug = () =>
  import( /* webpackChunkName: "report" */ './views/report/FbAsrDebug');
const FbVosEvent = () =>
  import( /* webpackChunkName: "report" */ './views/report/FbVosEvent');
const FbVehLog = () =>
  import( /* webpackChunkName: "report" */ './views/report/FbVehLog');
const FbReport = () =>
  import( /* webpackChunkName: "report" */ './views/report/FbReport');
const FbBadcase = () =>
  import( /* webpackChunkName: "report" */ './views/report/FbBadcase');
const Dashboard = () =>
  import( /* webpackChunkName: "report" */ './views/report/Dashboard');


const routes = [{
  path: '/report', //  引导页
  component: Main,
  children: [{
    path: 'dashboard',
    name: 'dashboard',
    meta: {
      keepAlive: true,
      bread: [{
        label: 'Dashboard',
        to: '/report/dashboard'
      }],
    },
    component: Dashboard
  }, {
    path: 'summary',
    name: 'summary',
    meta: {
      keepAlive: true,
      bread: [{
        label: 'summary',
        to: '/report/summary'
      }],
    },
    component: Summary
  }, {
    path: 'intent_report',
    name: 'intent-report',
    meta: {
      keepAlive: true,
      bread: [{
        label: '实车用户intent分布',
        to: '/report/intent_report'
      }],
    },
    component: FbIntentReport
  }, {
    path: 'query_detail/:domain/:intent',
    name: 'query-detail',
    meta: {
      keepAlive: true,
      bread: [{
        label: ' 详情'
      }],
    },
    component: FbQueryDetail
  }, {
    path: 'badcase',
    name: 'report-badcase',
    meta: {
      keepAlive: true,
      bread: [{
        label: 'badcase'
      }],
    },
    component: FbBadcase
  }, {
    path: ':type',
    name: 'report',
    meta: {
      keepAlive: true,
      bread: [{
        label: ' 报表'
      }],
    },
    component: FbReport
  }]
}, {
  path: '/debug',
  component: Main,
  children: [{
    path: '',
    name: 'debug',
    meta: {
      bread: [{
        label: 'debug',
        to: '/debug'
      }],
    },
    component: FbQueryDetailDebug
  }]
}, {
  path: '/vos_debug',
  component: Main,
  children: [{
    path: '',
    name: 'vos_debug',
    meta: {
      bread: [{
        label: 'vos_debug',
        to: '/vos_debug'
      }],
    },
    component: FbVosDebug
  }]
  },
  {
    path: '/asr_debug',
    component: Main,
    children: [{
      path: '',
      name: 'asr_debug',
      meta: {
        bread: [{
          label: 'asr_debug',
          to: '/asr_debug'
        }],
      },
      component: FbAsrDebug
    }
  ]
  },
  {
    path: '/vos_event',
    component: Main,
    children: [{
      path: '',
      name: 'vos_event',
      meta: {
        bread: [{
          label: 'vos_event',
          to: '/vos_event'
        }],
      },
      component: FbVosEvent
    }]
  },
{
  path: '/veh_log',
  component: Main,
  children: [{
    path: '',
    name: 'veh_log',
    meta: {
      bread: [{
        label: 'veh_log',
        to: '/veh_log'
      }],
    },
    component: FbVehLog
  }]
},{
  path: '/fact_data',
  component: Main,
  children: [{
    path: '',
    name: 'fact-data',
    meta: {
      bread: [{
        label: '实车用户数据',
        to: '/fact_data'
      }],
    },
    component: FbQueryDetail
  }]
}, {
  path: '*',
  redirect: '/report/dashboard' //  url错误重回定向
}];

const router = new VueRouter({
  routes
});

function main(role, to, next) {
  const actions = [];
  const crumbs = aisTool.getCrumbs(to);
  store.commit('SET_LABEL_TEXT', util.getLabelTextFromObj(to.params));
  store.commit('SET_AUTH_MENU');
  actions.forEach((action) => {
    store.dispatch(action);
  });
  aisTool.goToNextPage(role, to.meta.auth, next);
}

function ssoLogin(){
  var l = window.location
  var base_url = l.protocol+"//"+l.hostname+':'+l.port
  document.location = 'https://anno.x-tetris.com/sso/?auth_url='+base_url+'/api/auth_token&redirect_url='+base_url
}

router.beforeEach((to, from, next) => {
  const isLogin = !!aisTool.Cookie.getData('mars_token');
  
  if (!isLogin) {
    ssoLogin()
  } else {
    if ( ! /chrome/i.test(navigator.userAgent)) {
      alert('请使用chrome浏览器');
    }
    const hasInfo = store.getters.hasInfo;
    if (hasInfo) {
      const role = store.state.user.role;
      main(role, to, next);
    } else {
      alert("你没有权限！")
      ssoLogin()
    }
  }
});

export default router;

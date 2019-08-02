import Vue from 'vue';
import App from './App';
import store from './vuex';
import router from './router';
import iView from 'iview';
import AisComponents from 'ais-components';
import ECharts from 'vue-echarts/components/ECharts.vue';
import 'echarts/lib/chart/line';
import 'echarts/lib/chart/custom';
import 'echarts/lib/chart/radar';
import 'echarts/lib/chart/bar';
import 'echarts/lib/chart/pie';
import 'echarts/lib/chart/funnel';
import 'echarts/lib/component/tooltip';
import 'echarts/lib/component/title';
import 'echarts/lib/component/legend';
import 'echarts/lib/chart/map';
import './css/common.css'; /* 引入公共的样式文件 */
import 'iview/dist/styles/iview.css';
import 'ais-components/dist/ais-components.css';
import './theme/index.less';
import chinaMap from './config/china.json'
Vue.prototype.$appName = 'ndata';
Vue.use(iView, {
  transfer: true,
  size: 'large'
});
Vue.use(AisComponents);
Vue.component('chart', ECharts);
ECharts.registerMap('china', chinaMap);
const routerApp = new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');

export default routerApp;

<template>
  <div>
    <DatePicker v-model="currentDate" class="margin-bottom-10" :type="type" />
    <ButtonGroup class="margin-bottom-10">
      <Button v-for="tab in tabs" :key="tab.key + tab.component" :type="tab.label=== currentTabName? 'primary': 'default'" @click="setCurrentComponent(tab.component, tab.key, tab.label)" class="margin-bottom-10">{{tab.label}}</Button>
    </ButtonGroup>
    <keep-alive>
      <component :is="currentComponent" v-bind="currentProps"></component>
    </keep-alive>
  </div>
</template>
<script>
import moment from 'moment';
import columns from '../../config/column';
import DatePicker from '../../components/DatePicker/DatePicker';
import BaseInfoReport from './report/BaseInfoReport';
import PerformanceReportChart from './report/PerformanceReportChart';
import PerformanceReportTable from './report/PerformanceReportTable';
import DomainReport from './report/DomainReport';
import DoudiReport from './report/DoudiReport';
import HourlyReport from './report/HourlyReport';
import IntentReport from './report/IntentReport';
import NaviCallFunnelReport from './report/NaviCallFunnelReport';
import HuashuReport from './report/HuashuReport'
import VidUsageReport from './report/VidUsageReport';
import CityReport from './report/CityReport';
import RetentionReport from './report/RetentionReport';
import DailyActiveNomi from './report/DailyActiveNomi';
import MostUsedQuery from './report/MostUsedQuery';
import QueryInterregional from './report/QueryInterregional';

import util from '../../util';
const EXTRA_REPORT = [
  'vidUsage',
  'client_version',
  'queryInterregional',
  'active_nomi_daily',
  'vehicle.driving'
]
export default {
  components: {
    DatePicker,
    BaseInfoReport,
    DomainReport,
    PerformanceReportChart,
    PerformanceReportTable,
    DoudiReport,
    HourlyReport,
    IntentReport,
    NaviCallFunnelReport,
    HuashuReport,
    VidUsageReport,
    CityReport,
    RetentionReport,
    DailyActiveNomi,
    MostUsedQuery,
    QueryInterregional
  },
  data() {
    return {
      type: '',
      currentDate: util.getTodayDate(),
      currentTab: 'info',
      currentTabName: '基本信息',
      currentComponent: 'BaseInfoReport'
    }
  },
  beforeMount() {
    this.type = this.$route.params.type;
    this.setDefaultDate();
  },
  watch: {
    $route() {
      this.type = this.$route.params.type
      // 这两个报表值在月和周中有,切换报表日子类型的时候，需要考虑这个情况
      if (EXTRA_REPORT.includes(this.currentTab)) {
        this.currentTab = 'info'
        this.currentComponent = 'BaseInfoReport'
      }
      this.setDefaultDate();
    }
  },
  computed: {
    tabs() {
      let tabs = [{
        label: '基本信息',
        key: 'info',
        component: 'BaseInfoReport'
      }, {
        label: 'Domain分布',
        key: 'domain',
        component: 'DomainReport'
      }, {
        label: '兜底分布',
        key: 'nlu_type',
        component: 'DoudiReport'
      }, {
        label: '小时Query',
        key: 'hourly',
        component: 'HourlyReport'
      }, {
        label: 'Intent分布',
        key: 'intents',
        component: 'IntentReport'
      }, {
        label: '导航意图',
        key: 'navigation_funnel',
        component: 'NaviCallFunnelReport'
      }, {
        label: '电话意图',
        key: 'call_funnel',
        component: 'NaviCallFunnelReport'
      }, {
        label: '用户留存',
        key: 'retention',
        component: 'RetentionReport'
      }, {
        label: '话术分类',
        key: 'huashu',
        component: 'HuashuReport'
      }, {
        label: '城市',
        key: 'city',
        component: 'CityReport'
      }, {
        label: '高频话术',
        key: 'query.frequency',
        component: 'MostUsedQuery'
      }]

      if (this.type === 'monthly') {
        tabs.push({
          label: 'vid.usage',
          key: 'vidUsage',
          component: 'VidUsageReport',
        }, {
          label: '日均query区间',
          key: 'queryInterregional',
          component: 'QueryInterregional'
        }, {
          label: '日活跃情况',
          key: 'active_nomi_daily',
          component: 'DailyActiveNomi'
        }
        )
      }
      return tabs
    },
    reportType() {
      if (this.type === 'monthly') {
        return 'm'
      } else if (this.type === 'daily') {
        return 'd'
      } else if (this.type === 'weekly') {
        return 'w'
      }
    },
    dateFormat() {
      if (this.type === 'monthly') {
        return 'YYYYMM';
      } else if (this.type === 'daily') {
        return 'YYYYMMDD';
      } else if (this.type === 'weekly') {
        return 'YYYYww';
      }
    },
    dateKey() {
      if (this.type === 'weekly') {
        //处理周日的情况，这周日算这周，不算下周
        if (new Date(this.currentDate).getDay() === 0) {
          return moment(this.currentDate).subtract(1, 'days').format(this.dateFormat);
        }
      }
      return moment(this.currentDate).format(this.dateFormat);
    },
    currentProps() {
      return {
        reportType: this.reportType,
        date: this.dateKey,
        report: this.currentTab
      };
    }
  },
  methods: {
    setDefaultDate(type) {
      if (this.type === 'daily' || this.type === 'weekly') {
        this.currentDate = util.getTodayDate();
      } else if (this.type === 'monthly') {
        this.currentDate = util.getCurrentMonth();
      }
    },
    setCurrentComponent(component, key, label) {
      if (label !== this.currentTabName) {
        this.currentTab = key;
        this.currentTabName = label;
        this.currentComponent = component;
      }
    }
  }
}

</script>

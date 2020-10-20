import aisTool from 'ais-components';

const REPORT = {
  label: '实车报表',
  children: [{
    label: 'Dashboard',
    to: '/report/dashboard',
    icon: 'md-speedometer',
    name: 'dashboard'
  }, {
    label: '整体数据',
    to: '/report/summary',
    icon: 'md-pie',
    name: 'summary'
  }, {
    label: 'Intent分布',
    to: '/report/intent_report',
    icon: 'ios-pie-outline',
    name: 'intent-report'
  },{
    label: 'Request Info',
    to: '/debug',
    icon: 'md-grid',
    name: 'face-data'
  },{
    label: 'Local Request Info',
    to: '/vos_debug',
    icon: 'md-bug',
    name: 'face-data'
  },{
    label: 'Asr Request Info',
    to: '/asr_debug',
    icon: 'md-mic',
    name: 'face-data'
  },{
    label: 'Wakeup',
    to: '/wakeup',
    icon: 'md-star',
    name: 'face-data'
  },{
    label: 'VosEvent',
    to: '/vos_event',
    icon: 'md-list',
    name: 'face-data'
  },{
    label: 'VehLog',
    to: '/veh_log',
    icon: 'md-cloud-download',
    name: 'veh_log'
  }]
}

const REPORT_GN = {
  label: '实车报表',
  children: [{
    label: 'Dashboard',
    to: '/report/dashboard',
    icon: 'md-speedometer',
    name: 'dashboard'
  }, {
    label: '整体数据',
    to: '/report/summary',
    icon: 'md-pie',
    name: 'summary'
  }, {
    label: 'Intent分布',
    to: '/report/intent_report',
    icon: 'ios-pie-outline',
    name: 'intent-report'
  }, {
    label: 'Request Info',
    to: '/debug',
    icon: 'md-grid',
    name: 'face-data'
  }, {
    label: '单日报表',
    to: '/report/daily',
    icon: 'md-analytics',
    name: 'daily-report'
  }, {
    label: '单周报表',
    to: '/report/weekly',
    icon: 'md-analytics',
    name: 'weekly-report'
  }, {
    label: '月度报表',
    to: '/report/monthly',
    icon: 'md-analytics',
    name: 'month-report'
  }]
}

var export_menu = REPORT
if( aisTool.Cookie.getData("ops-org") === "gn") {
  export_menu = REPORT_GN 
}

export default {
  base: [export_menu]
}

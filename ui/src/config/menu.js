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
  }, {
    label: '实车用户数据',
    to: '/fact_data',
    icon: 'md-grid',
    name: 'face-data'
  },{
    label: 'Debug',
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

export default {
  base: [REPORT]
}

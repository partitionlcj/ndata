<template>
  <div>
    <div class="flex-row">
      <InputNumber v-model="dailyMinNum"></InputNumber>
      <InputNumber v-model="dailyMinRate"></InputNumber>
    </div>
    <chart :options="activeOption" auto-resize theme="light" style="width: 100%;" class="margin-bottom-10"></chart>
    <div class="flex-row">
      <InputNumber v-model="dailyQueryMin"></InputNumber>
      <InputNumber v-model="dailyRateMin"></InputNumber>
    </div>
    <chart :options="activeRateOption" auto-resize theme="light" style="width: 100%" class="margin-bottom-10"></chart>
  </div>
</template>
<script>
import mixin from './mixin';
import util from '../../../util';
export default {
  mixins: [mixin],
  data() {
    return {
      dailyMinNum: 0,
      dailyMinRate: 0,
      dailyQueryMin: 0,
      dailyRateMin: 0,
      activeNomi: [],
      activeNomiRate: [],
      driveRate: [],
      userDriveRate: [],
      activeNomiDailyQuery: [],
      activeNomiDailyRate: []
    }
  },
  computed: {
    reportKey() {
      return `optimization.${this.report}.${this.reportType}.${this.date}`;
    },
    queryReportKey() {
      return `optimization.${this.report}_query.${this.reportType}.${this.date}`;
    },
    activeOption() {
      return {
        title: {
          text: 'nomi日活度'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['活跃nomi', 'nomi日活率', '行驶率', '行车用户日活率']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: true,
          axisTick: {
            alignWithLabel: true
          },
          data: util.getDaysArrayByMonth(this.date)
        },
        yAxis: [{
          type: 'value',
          min: this.dailyMinNum
        }, {
          type: 'value',
          min: this.dailyMinRate,
          max: 100,
          axisLabel: {
            formatter: '{value}%'
          }
        }],
        series: [{
          name: '活跃nomi',
          type: 'bar',
          yAxisIndex: 0,
          barWidth: '60%',
          data: this.activeNomi
        }, {
          name: 'nomi日活率',
          type: 'line',
          yAxisIndex: 1,
          data: this.activeNomiRate
        }, {
          name: '行驶率',
          type: 'line',
          yAxisIndex: 1,
          data: this.driveRate
        }, {
          name: '行车用户日活率',
          type: 'line',
          yAxisIndex: 1,
          data: this.userDriveRate
        }]
      };
    },
    activeRateOption() {
      return {
        title: {
          text: 'nomi日活率'
        },
        toolbox: {
          feature: {
            saveAsImage: { show: true }
          }
        },
        legend: {
          data: ['(活跃nomi)单车日均query', 'nomi日活率']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [{
          type: 'category',
          data: util.getDaysArrayByMonth(this.date)
        }],
        yAxis: [{
          type: 'value',
          min: this.dailyQueryMin,
          axisLabel: {
            formatter: '{value}'
          }
        }, {
          type: 'value',
          max: 100,
          min: this.dailyRateMin,
          axisLabel: {
            formatter: '{value}%'
          }
        }],
        series: [{
            name: '(活跃nomi)单车日均query',
            type: 'line',
            yAxisIndex: 0,
            markLine: {
              data: [
                { type: 'average', name: '平均值' }
              ]
            },
            data: this.activeNomiDailyQuery
          },
          {
            name: 'nomi日活率',
            type: 'line',
            yAxisIndex: 1,
            markLine: {
              data: [
                { type: 'average', name: '平均值' }
              ]
            },
            stack: '总量',
            data: this.activeNomiDailyRate
          }
        ]
      }

    }
  },
  beforeMount() {
    this.loadData();
  },
  methods: {
    async loadData() {
      let response = await this.getData([this.reportKey, this.queryReportKey].join(','));
      let activeData = response[this.reportKey];
      let queryData = response[this.queryReportKey];
      this.activeNomi = activeData && activeData.active_nomi;
      this.activeNomiRate = activeData && activeData.active_nomi_rate;
      this.driveRate = activeData && activeData.drive_rate;
      this.userDriveRate = activeData && activeData.user_drive_rate;
      this.activeNomiDailyQuery = queryData && queryData.active_nomi_daily_query;
      this.activeNomiDailyRate = queryData && queryData.active_nomi_daily_rate;
    }
  }
}

</script>

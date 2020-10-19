<template>
  <div>
    <div>
      <Button @click="setKeyPrefix('ds-mars-prod.100240130')">杰克豆</Button>
      <Button @click="setKeyPrefix('ds-mars-prod.100990130')">齐悟</Button>
      <Button @click="setKeyPrefix('ds-gn-prod.100240001')">广蔚</Button>
    </div>
    <div style="display: flex; justify-content: space-around; margin-bottom: '10px'">
      <Card v-for="(item, index) in nomiUseHoursData" :key="item.name" :style="{flex:1, margin:'0 8px', backgroundColor: colors[index]}" class="info-card">
        <div style="padding: 16px">
          <h2>{{item.value[item.value.length-1]}}</h2>
          <h5>{{item.name}}</h5>
          <p>{{(item.value.length-1) | fullHours}}-{{item.value.length | fullHours}}</p>
        </div>
        <chart auto-resize :options="getOption(item.value)" theme="light" style="width: 100%; height: 180px"></chart>
      </Card>
    </div>
    <Card class="margin-bottom-10 margin-top-10">
      <!-- <chart auto-resize :options="nomiUseHoursOption" theme="light" style="width: 100%;"></chart> -->
      <chart auto-resize :options="nomiUseHoursDomainOption" theme="light" style="width: 100%;"></chart>
    </Card>
    <Divider>截止到前一个小时的总体数据</Divider>
    <div style="display: flex; justify-content: space-around;">
      <Card v-for="(item, index) in baseSummaryData" :key="item.name" :style="{textAlign: 'center', flex:1, margin:'0 16px', backgroundColor: colors[index]}">
        <h2>{{item.value}}</h2>
        <h5>{{item.name}}</h5>
      </Card>
    </div>
  </div>
</template>
<script>
import moment from 'moment';
import api from '../../api/report';
import StackLine from '../../components/Line/StackLine';
export default {
  components: {
    StackLine
  },
  filters: {
    fullHours: function(value) {
      return String(value).padStart(2, '0') + ':00';
    }
  },
  data() {
    return {
      today: '',
      keyPrefix: 'ds-mars-prod.100240130',
      nomiUseSummary: null,
      nomiUseHoursInfo: null,
      colors: ['#00bebe', '#ffc107', '#f86c6b', '#20a8d8', '#63c2de', '#4dbd74', '#735973', '#96C5B0', '#E7AAB2']
    }
  },
  computed: {
    useNomiHoursKey() {
      return `${this.keyPrefix}.total.info.use_nomi_hours.d.${this.today}`;
    },
    useNomiSummaryKey() {
      return `ds-mars-prod.total.info.use_nomi.d.${this.today}`;
    },
    baseSummaryData() {
      if (this.nomiUseSummary) {
        return [{
          name: '唤醒次数',
          value: this.nomiUseSummary.wakeupCount,
        }, {
          name: 'ASR次数',
          value: this.nomiUseSummary.asrCount,
        }, {
          name: '设备数',
          value: this.nomiUseSummary.vidCount,
        }, {
          name: 'Query数',
          value: this.nomiUseSummary.queryCount,
        }]
      }
      return [];
    },
    top10Intent() {
      if (this.nomiUseSummary) {
        return this.nomiUseSummary.intent;
      }
      return {
        head: [],
        data: []
      };
    },
    topDomain() {
      if (this.nomiUseSummary) {
        return this.nomiUseSummary.domain;
      }
      return {
        head: [],
        data: []
      };
    },
    topUser() {
      if (this.nomiUseSummary) {
        return this.nomiUseSummary.activeUser;
      }
      return {
        head: [],
        data: []
      };
    },
    topMonthUser() {
      if (this.nomiUseSummary) {
        return this.nomiUseSummary.MonthActiveUser;
      }
      return {
        head: [],
        data: []
      };
    },
    nomiUseHoursData() {
      if (this.nomiUseHoursInfo) {
        return [{
          name: '唤醒次数',
          value: this.nomiUseHoursInfo.resultMap.wakeupCount
        }, {
          name: 'ASR次数',
          value: this.nomiUseHoursInfo.resultMap.asrCount
        }, {
          name: '设备数',
          value: this.nomiUseHoursInfo.resultMap.vidCount
        }, {
          name: 'Query数',
          value: this.nomiUseHoursInfo.resultMap.queryCount
        }]
      }
      return [];
    },
    nomiUseHoursDomainOption() {
      let series = [];
      let xAxisData = Array.from(Array(24).keys()).map(num => String(num).padStart(2, '0'));
      let legendData = [];
      if (this.nomiUseHoursInfo) {
        legendData = Object.keys(this.nomiUseHoursInfo.domainMap);
        legendData.forEach((domain, index) => {
          series.push({
            name: domain,
            type: 'line',
            lineStyle: {
              color: this.colors[index]
            },
            data: this.nomiUseHoursInfo.domainMap[domain]
          })
        })
      }
      return {
        tooltip: {
          trigger: 'axis'
        },
        color: this.colors,
        legend: {
          data: legendData,
          icon: 'pin'
        },
        grid: {
          left: '5%',
          right: '5%',
          bottom: '5%'
        },
        xAxis: {
          boundaryGap: false,
          data: xAxisData
        },
        yAxis: {
          type: 'value'
        },
        series: series
      };
    }
  },
  created() {
    this.today = moment().format('YYYYMMDD')
    this.loadData();
  },
  methods: {
    async loadData() {
      let response = await api.getData([this.useNomiHoursKey].join(','));
      if (response.state === 'success') {
        //this.nomiUseSummary = response.data[this.useNomiSummaryKey];
        this.nomiUseHoursInfo = response.data[this.useNomiHoursKey];
      }
    },
    setKeyPrefix(k){
      this.keyPrefix = k;
      console.log(this.keyPrefix)
      this.loadData()
    },
    getOption(data) {
      return {
        tooltip: {
          trigger: 'axis'
        },
        grid: {
          top: 0,
          left: 0,
          right: 0,
          bottom: 5
        },
        xAxis: {
          show: false,
          type: 'category',
          data: data.map((item, index) => String(index).padStart(2, '0'))
        },
        yAxis: {
          show: false,
          type: 'value',
        },
        series: [{
          data: data,
          type: 'line',
          lineStyle: {
            color: 'white',
            opacity: 0.8
          },
          itemStyle: {
            color: 'white'
          }
        }]
      }
    }
  }
}

</script>
<style scoped>
.info-card>>>.ivu-card-body {
  padding: 0;
}

</style>

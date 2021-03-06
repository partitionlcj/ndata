<template>
  <div>
    <div>
      <DatePicker :value="today" format="yyyyMMdd" type="date" placeholder="Select date" style="width: 200px" @on-change="dateChange"></DatePicker>
      <Button @click="setKeyPrefix('ds-mars-prod.100240130','杰克豆')">杰克豆</Button>
      <Button @click="setKeyPrefix('ds-gn-prod.100240001','广蔚')">广蔚</Button>
      <Button @click="setKeyPrefix('ds-mars-prod.100990130','齐悟')">齐悟</Button>
      当前APP: <b>{{title}}</b>
    </div>
    <div
      style="
        display: flex;
        justify-content: space-around;
        margin-bottom: '10px';
      "
    >
      <Card
        v-for="(item, index) in nomiUseHoursData"
        :key="item.name"
        :style="{ flex: 1, margin: '0 8px', backgroundColor: colors[index] }"
        class="info-card"
      >
        <div style="padding: 16px">
          <h2>{{ item.name }}</h2>
        </div>
        <chart
          auto-resize
          :options="getOption(item.value)"
          theme="light"
          style="width: 100%; height: 180px"
        ></chart>
      </Card>
    </div>
    <Card class="margin-bottom-10 margin-top-10">
      <!-- <chart auto-resize :options="nomiUseHoursOption" theme="light" style="width: 100%;"></chart> -->
      <chart
        auto-resize
        :options="hourlyUseHoursDomainOption"
        theme="light"
        style="width: 100%"
      ></chart>
    </Card>
    <Divider>截止到前一个小时的总体数据</Divider>
    <div style="display: flex; justify-content: space-around">
      <Card
        v-for="(item, index) in baseSummaryData"
        :key="item.name"
        :style="{
          textAlign: 'center',
          flex: 1,
          margin: '0 16px',
          backgroundColor: colors[index],
        }"
      >
        <h2>{{ item.value }}</h2>
        <h5>{{ item.name }}</h5>
      </Card>
    </div>
    <Divider>自定义查询</Divider>
      <DatePicker type="daterange" @on-change="chartDataChange" format="yyyyMMdd" placement="bottom-end" placeholder="选择时间范围" style="width: 200px"></DatePicker>
      当前APP: <b>{{title}}</b>
    <Card class="margin-bottom-10 margin-top-10">
      <chart
        auto-resize
        :options="keyMetricsOptions"
        theme="light"
        style="width: 100%"
      ></chart>
    </Card>
  </div>
</template>
<script>
import moment from "moment";

import api from "../../api/report";
import StackLine from "../../components/Line/StackLine";
export default {
  components: {
    StackLine,
  },
  filters: {
    fullHours: function (value) {
      return String(value).padStart(2, "0") + ":00";
    },
  },
  data() {
    return {
      today: "",
      title: "杰克豆",
      keyPrefix: "ds-mars-prod.100240130",
      nomiUseSummary: null,
      nomiUseHoursInfo: null,
      chartData: null,
      dateKeys: [],
      chartDateRange: [],
      colors: [
        "#00bebe",
        "#ffc107",
        "#f86c6b",
        "#20a8d8",
        "#63c2de",
        "#4dbd74",
        "#735973",
        "#96C5B0",
        "#E7AAB2",
      ],
    };
  },
  computed: {
    useNomiHoursKey() {
      return `${this.keyPrefix}.total.info.use_nomi_hours.d.${this.today}`;
    },
    useNomiSummaryKey() {
      return `${this.keyPrefix}.total.info.use_nomi.d.${this.today}`;
    },
    baseSummaryData() {
      if (this.nomiUseSummary) {
        return [
          {
            name: "主唤醒次数",
            value: this.nomiUseSummary.wakeup0Count,
          },
          {
            name: "自定义唤醒次数",
            value: this.nomiUseSummary.wakeup4Count,
          },
          {
            name: "ASR次数",
            value: this.nomiUseSummary.asrCount,
          },
          {
            name: "设备数",
            value: this.nomiUseSummary.vidCount,
          },
          {
            name: "Query数",
            value: this.nomiUseSummary.queryCount,
          },
        ];
      }
      return [];
    },
    top10Intent() {
      if (this.nomiUseSummary) {
        return this.nomiUseSummary.intent;
      }
      return {
        head: [],
        data: [],
      };
    },
    topDomain() {
      if (this.nomiUseSummary) {
        return this.nomiUseSummary.domain;
      }
      return {
        head: [],
        data: [],
      };
    },
    topUser() {
      if (this.nomiUseSummary) {
        return this.nomiUseSummary.activeUser;
      }
      return {
        head: [],
        data: [],
      };
    },
    topMonthUser() {
      if (this.nomiUseSummary) {
        return this.nomiUseSummary.MonthActiveUser;
      }
      return {
        head: [],
        data: [],
      };
    },
    nomiUseHoursData() {
      if (this.nomiUseHoursInfo) {
        return [
          {
            name: "唤醒次数",
            value: this.nomiUseHoursInfo.resultMap.wakeupCount,
          },
          {
            name: "ASR次数",
            value: this.nomiUseHoursInfo.resultMap.asrCount,
          },
          {
            name: "设备数",
            value: this.nomiUseHoursInfo.resultMap.vidCount,
          },
          {
            name: "Query数",
            value: this.nomiUseHoursInfo.resultMap.queryCount,
          },
        ];
      }
      return [];
    },
    hourlyUseHoursDomainOption() {
      let series = [];
      let xAxisData = Array.from(Array(24).keys()).map((num) =>
        String(num).padStart(2, "0")
      );
      let legendData = [];
      if (this.nomiUseHoursInfo) {
        legendData = Object.keys(this.nomiUseHoursInfo.domainMap);
        legendData.forEach((domain, index) => {
          series.push({
            name: domain,
            type: "line",
            lineStyle: {
              color: this.colors[index],
            },
            data: this.nomiUseHoursInfo.domainMap[domain],
          });
        });
      }
      return {
        tooltip: {
          trigger: "axis",
        },
        color: this.colors,
        legend: {
          data: legendData,
          icon: "pin",
        },
        grid: {
          left: "5%",
          right: "5%",
          bottom: "5%",
        },
        xAxis: {
          boundaryGap: false,
          data: xAxisData,
        },
        yAxis: {
          type: "value",
        },
        series: series,
      };
    },
    keyMetricsOptions() {
      if (this.chartData) {
        let series = [];
        let xAxisData = Array.from(this.dateKeys).map((k) =>
          k.substring(k.length - 4, k.length-2) + "/" + k.substring(k.length - 2, k.length)
        );

        let legendData = [{k:'wakeup0Count',n:'主唤醒次数'},{k:'wakeup4Count',n:"自定义唤醒次数"},{k:'asrCount',n:'ASR次数'},{k:'vidCount',n:'设备数'},{k:'queryCount',n:'Query数'}]
        let that = this
        legendData.forEach((k, index) => {
          series.push({
            name: k['n'],
            type: "line",
            lineStyle: {
              color: this.colors[index],
            },
            data: that.getMetricsData(k['k'])
          });
        });
      
        return {
          tooltip: {
            trigger: "axis",
          },
          color: this.colors,
          legend: {
            data: ['主唤醒次数','自定义唤醒次数','ASR次数','设备数','Query数'],
            icon: "pin",
          },
          grid: {
            left: "5%",
            right: "5%",
            bottom: "5%",
          },
          xAxis: {
            boundaryGap: false,
            data: xAxisData,
          },
          yAxis: {
            type: "value",
          },
          series: series,
        };
      }
    },
  },
  created() {
    this.today = moment().format("YYYYMMDD");
    this.chartDateRange = [moment().subtract(14,'d').format('YYYYMMDD'),this.today]
    this.loadData();
    this.loadChartData();
  },
  methods: {
    chartDataChange(val){
      console.log(val)
      this.chartDateRange = val
      this.loadChartData()
    },
    getMetricsData(k){
      let data = []
      this.dateKeys.forEach((v,idx)=>{
        if (this.chartData[v]){
          data.push(this.chartData[v][k])
        }
      })
      return data
    },
    async loadChartData(){
      this.dateKeys = []
      let startDate = moment(this.chartDateRange[0], "YYYYMMDD")
      let endDate   = moment(this.chartDateRange[1], "YYYYMMDD")
      let dateRange = moment().range(startDate, endDate);

      const days = Array.from(dateRange.by('day'));
      days.map(m => {
        let dt = m.format('YYYYMMDD');
        this.dateKeys.push(`${this.keyPrefix}.total.info.use_nomi.d.${dt}`)
      }) 

      let response = await api.getData(
        this.dateKeys.join(",")
      );
      if (response.state === "success") {
        this.chartData = response.data
      }
    },
    async loadData() {
      let response = await api.getData(
        [this.useNomiHoursKey, this.useNomiSummaryKey].join(",")
      );
      if (response.state === "success") {
        this.nomiUseSummary = response.data[this.useNomiSummaryKey];
        this.nomiUseHoursInfo = response.data[this.useNomiHoursKey];
      }
    },
    dateChange (date) {
      this.today = date;
      this.loadData();
    },
    setKeyPrefix(k,title) {
      this.keyPrefix = k;
      this.title = title;
      this.loadData();
      this.loadChartData();
    },
    getOption(data) {
      return {
        tooltip: {
          trigger: "axis",
        },
        grid: {
          top: 0,
          left: 0,
          right: 0,
          bottom: 5,
        },
        xAxis: {
          show: false,
          type: "category",
          data: data.map((item, index) => String(index).padStart(2, "0")),
        },
        yAxis: {
          show: false,
          type: "value",
        },
        series: [
          {
            data: data,
            type: "line",
            lineStyle: {
              color: "white",
              opacity: 0.8,
            },
            itemStyle: {
              color: "white",
            },
          },
        ],
      };
    },
  },
};
</script>
<style scoped>
.info-card >>> .ivu-card-body {
  padding: 0;
}
</style>

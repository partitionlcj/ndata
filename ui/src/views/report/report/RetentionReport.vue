<template>
  <div>
    <AisObjCol :data="data" class="margin-bottom-10" />
    <template v-if="reportType === 'm'">
      <ButtonGroup class="margin-bottom-20">
        <Button :type="currentTab === 'a'?'primary':'default'" @click="currentTab='a'">不同提车时期用户月度留存率变化</Button>
        <Button :type="currentTab === 'b'?'primary':'default'" @click="currentTab='b'">当月提车用户激活率变化</Button>
      </ButtonGroup>
      <template v-if="currentTab==='a'">
        <AisTable :show-page="false" :columns="detailColumns" :data="detailData" class="margin-bottom-10" />
        <InputNumber v-model="ymin" palceholder="y洲最小值调整"></InputNumber>
        <CheckboxGroup v-model="picOptions" class="margin-top-20 margin-bottom-10">
          <Checkbox label="留存率"></Checkbox>
          <Checkbox label="行驶率"></Checkbox>
          <Checkbox label="日活率"></Checkbox>
        </CheckboxGroup>
        <StackLine :legend="compareLegend" :xAxisData="xAxisData" :series="series" :title="date + '留存率对比'" :ymin="ymin" legend-orient="vertical" style="width: 100%" />
        <AisTable :show-page="false" :columns="driveRateColumns" :data="driveRateData" table-title="每日行驶率" class="margin-bottom-20" />
        <AisTable :show-page="false" :columns="userDriveRateColumns" :data="userDriveRateData" table-title="每日行车用户的留存率" />
      </template>
      <template v-if="currentTab==='b'">
        <AisTable :show-page="false" :columns="optColumns" :data="optData" table-title="提车天次变化表" class="margin-bottom-10" />
        <!-- 当月新提车用户行驶率变化 -->
        <AisTable :show-page="false" :columns="activeDriveRateColumns" :data="activeDriveRateData" table-title="当月新提车用户行驶率变化" class="margin-bottom-10" />
        <!-- 当月新提车用户日行驶用户激活率变化 -->
        <AisTable :show-page="false" :columns="activeUserDriveRateColumns" :data="activeUserDriveRateData" table-title="当月新提车用户日行驶用户激活率变化" class="margin-bottom-10" />
      </template>
    </template>
  </div>
</template>
<script>
import mixin from './mixin';
import StackLine from '../../../components/Line/StackLine';
import util from '../../../util';
export default {
  components: {
    StackLine
  },
  mixins: [mixin],
  data() {
    return {
      data: {},
      ymin: 0,
      detailColumns: [{
        title: '',
        key: 'date',
        align: 'center'
      }, {
        title: '当月提车用户留存率',
        key: 'curMonth',
        align: 'center'
      }, {
        title: '上月提车用户月留存率',
        key: 'lastMonth',
        align: 'center'
      }, {
        title: '上上月提车用户月留存率',
        key: 'lastlastMonth',
        align: 'center'
      }, {
        title: '历史老用户',
        key: 'history',
        align: 'center'
      }],
      detailData: [],
      optColumns: [],
      optData: [],
      legend: [],
      compareData: [],
      driveRateData: [],
      driveRateColumns: [],
      userDriveRateColumns: [],
      userDriveRateData: [],
      activeDriveRateColumns: [],
      activeDriveRateData: [],
      activeUserDriveRateColumns: [],
      activeUserDriveRateData: [],
      currentTab: 'a',
      picOptions: ['留存率', '行驶率', '日活率']
    }
  },
  computed: {
    reportKey() {
      return `${this.report}.${this.reportType}.${this.date}`;
    },
    detailReportKey() {
      return `${this.report}.detail.${this.reportType}.${this.date}`;
    },
    optmizedReportKey() {
      return `optimization.active.user_rate.${this.reportType}.${this.date}`;
    },
    graphKey() {
      return `optimization.${this.report}_graph.${this.reportType}.${this.date}`;
    },
    xAxisData() {
      return util.getDaysArrayByMonth(this.date);
    },
    compareLegend() {
      return this.legend.filter(item => {
        for (let option of this.picOptions) {
          if (this.$aisUtil.hasStr(item, option)) {
            return true;
          }
        }
        return false;
      })
    },
    series() {
      return this.compareData.filter(item => {
        for (let option of this.picOptions) {
          if (this.$aisUtil.hasStr(Object.keys(item)[0], option)) {
            return true;
          }
        }
        return false
      }).map(item => {
        let borderType = 'solid';
        let key = Object.keys(item)[0];
        if (this.$aisUtil.hasStr(key, '行驶率')) {
          borderType = 'dashed';
        } else if (this.$aisUtil.hasStr(key, '日活率')) {
          borderType = 'dotted';
        }
        return {
          name: key,
          type: 'line',
          data: Object.values(item)[0],
          lineStyle: {
            normal: {
              type: borderType
            }
          }
        }
      })
    },
    driveRateKey() {
      return `optimization.retention.drive_rate.${this.reportType}.${this.date}`;
    },
    userDriveRateKey() {
      return `optimization.retention.user_drive_rate.${this.reportType}.${this.date}`;
    },
    activeDriveRateKey() {
      return `optimization.active.drive_rate.${this.reportType}.${this.date}`;
    },
    activeUserDriveRateKey() {
      return `optimization.active.user_drive_rate.${this.reportType}.${this.date}`;
    }
  },
  beforeMount() {
    this.loadData();
  },
  methods: {
    async loadData() {
      this.data = await this.getData(this.reportKey);
      if (this.reportType === 'm') {
        let response = await this.getData([this.detailReportKey, this.optmizedReportKey, this.graphKey, this.driveRateKey, this.userDriveRateKey, this.activeDriveRateKey, this.activeUserDriveRateKey].join(','))
        if (response) {
          this.detailData = this.getDetailData(response[this.detailReportKey]);

          this.optColumns = response[this.optmizedReportKey].head;
          this.optData = response[this.optmizedReportKey].data;

          this.legend = response[this.graphKey].legend;
          this.compareData = response[this.graphKey].data;

          this.driveRateColumns = response[this.driveRateKey].head;
          this.driveRateData = response[this.driveRateKey].data;

          this.userDriveRateColumns = response[this.userDriveRateKey].head;
          this.userDriveRateData = response[this.userDriveRateKey].data;

          this.activeDriveRateColumns = response[this.activeDriveRateKey].head;
          this.activeDriveRateData = response[this.activeDriveRateKey].data;

          this.activeUserDriveRateColumns = response[this.activeUserDriveRateKey].head;
          this.activeUserDriveRateData = response[this.activeUserDriveRateKey].data;

        }
      }
    },
    getDetailData(data) {
      let res = [];
      for (let key in data) {
        if (data.hasOwnProperty(key)) {
          let temp = {
            date: key,
            curMonth: data[key][0],
            lastMonth: data[key][1],
            lastlastMonth: data[key][2],
            history: data[key][3]
          };
          res.push(temp)
        }
      }
      return res;
    }
  }
}

</script>

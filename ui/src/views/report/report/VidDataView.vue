<template>
  <div>
    <Input v-model="vid" @on-enter="loadData" placeholder="请输入vid"></Input>
    <AisTable :columns="columns" :data="tableData" :show-page="false" />
  </div>
</template>
<script>
import util from '../../../util';
import mixin from './mixin';
export default {
  mixins: [mixin],
  data() {
    return {
      data: [],
      vid: ''
    };
  },
  computed: {
    columns() {
      return [{
        title: '每日交互次数',
        key: 'queryCount'
      }, {
        title: '每日唤醒次数',
        key: 'sessionCount'
      }, {
        title: '每日行车时间',
        key: 'drivingTime'
      }, {
        title: '日期',
        key: 'date'
      }];
    },
    reportKey() {
      return `${this.report}.${this.vid}.${this.reportType}.${this.date}`;
    },
    tableData() {
      if (this.data) {
        return this.data.map(item => {
          item.drivingTime = `${util.generateReadableTime(item.drivingTime)}(${item.drivingTime})`;
          return item;
        });
      } else {
        return []
      }
    }
  }

}

</script>

<template>
  <div>
    <ChinaMap :data="mapData" :max="max" style="width: 100%; min-height: 600px" title="车辆城市分布" />
    <AisTable :columns="columns" :data="data" :file-name="reportKey" download-xls />
  </div>
</template>
<script>
import util from '../../../util';
import mixin from './mixin';
import ChinaMap from '../../../components/Map/ChinaMap';
export default {
  components: {
    ChinaMap
  },
  mixins: [mixin],
  data() {
    return {
      data: []
    }
  },
  computed: {
    reportKey() {
      return `base.${this.report}.${this.reportType}.${this.date}`;
    },
    columns() {
      let column = util.getTableHeader(this.data && this.data[0]);
      column.forEach(item => {
        if (item.title === '总query') {
          item.sortable = true;
          item.sortType = 'number';
        }
        if (item.title === '到达车辆') {
          item.sortable = true;
          item.sortType = 'number';
        }
      });
      return column;
    },
    mapData() {
      if (this.data) {
        return this.data.map(item => ({ name: item.city, value: item['到达车辆'] }));
      } else {
        return [];
      }
    },
    max() {
      let max = 0;
      this.mapData.forEach(item => {
        if (item.value > max) {
          max = item.value;
        }
      });
      return max;
    }
  },
  beforeMount() {
    this.loadData();
  }
}

</script>

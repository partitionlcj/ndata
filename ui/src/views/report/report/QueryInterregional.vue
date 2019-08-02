<template>
  <div>
    <AisTable :columns="columns" :data="data" :file-name="reportKey" :table-title="reportKey" download-xls />
    <AisTable :columns="drivingColumn" :data="drivingData" :file-name="drivingQueryKey" :table-title="drivingQueryKey" download-xls />
  </div>
</template>
<script>
import util from '../../../util';
import columns from '../../../config/column';
import mixin from './mixin';
export default {
  mixins: [mixin],
  data() {
    return {
      data: [],
      columns: [],
      drivingData: [],
      drivingColumn: []
    }
  },
  computed: {
    reportKey() {
      return `optimization.${this.report}.${this.reportType}.${this.date}`;
    },
    drivingQueryKey() {
      return `optimization.driveQueryInterregional.${this.reportType}.${this.date}`;
    }
  },
  beforeMount() {
    this.loadData();
    this.loadDrivingQuery();
  },
  watch: {
    drivingQueryKey() {
      this.loadDrivingQuery();
    }
  },
  methods: {
    async loadData() {
      try {
        const data = await this.getData(`${this.reportKey}`);
        this.data = data.data;
        this.columns = data.head;
      } catch (e) {
        this.data = [];
        this.columns = [];
      }
    },
    async loadDrivingQuery() {
      try {
        const data = await this.getData(this.drivingQueryKey);
        this.drivingData = data.data;
        this.drivingColumn = data.head;
      } catch (e) {
        this.drivingData = [];
        this.drivingColumn = [];
      }
    }
  }
}

</script>

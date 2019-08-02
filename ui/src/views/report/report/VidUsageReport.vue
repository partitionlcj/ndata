<template>
  <AisTable :columns="columns" :data="data" :file-name="reportKey" download-xls />
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
      columns: []
    }
  },
  computed: {
    reportKey() {
      return `optimization.${this.report}.${this.reportType}.${this.date}`;
    }
  },
  beforeMount() {
    this.loadData();
  },
  methods: {
    async loadData() {
      try {
        const data = await this.getData(`${this.reportKey}`);
        this.data = data.data;
        this.columns = data.head.map(item => {
          item.width = 80;
          return item;
        });
      } catch (e) {
        this.data = [];
        this.columns = [];
      }
    }
  }
}

</script>

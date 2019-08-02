<template>
  <AisTable :columns="columns" :data="tableData" :show-page="false" :file-name="reportKey" download-xls />
</template>
<script>
import mixin from './mixin';
export default {
  mixins: [mixin],
  data() {
    return {
      data: {}
    };
  },
  computed: {
    title() {
      if (this.reportType === 'm') {
        return '当月';
      } else if (this.reportType === 'd') {
        return '当天';
      } else if (this.reportType === 'w') {
        return '本周';
      }
    },
    columns() {
      return [{
        title: '名称',
        key: 'label'
      }, {
        title: this.title,
        key: 'num'
      }];
    },
    tableData() {
      let res = []
      for (let key in this.data) {
        if (this.data.hasOwnProperty(key)) {
          res.push({
            label: key,
            num: this.data[key]
          })
        }
      }
      return res;
    },
    reportKey() {
      return `optimization.base.${this.report}.${this.reportType}.${this.date}`;
    }
  },
  beforeMount() {
    this.loadData();
  }
}

</script>

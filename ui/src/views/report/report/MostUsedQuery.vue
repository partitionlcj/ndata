<template>
  <AisTable :columns="columns" :data="data" />
</template>
<script>
import mixin from './mixin';
export default {
  mixins: [mixin],
  data() {
    return {
      data: [],
      columns: [{
        title: '话术',
        key: 'query'
      }, {
        title: '词频',
        key: 'count'
      }]
    };
  },
  computed: {
    reportKey() {
      return `ds-mars-prod.${this.report}.${this.reportType}.${this.date}`;
    }
  },
  beforeMount() {
    this.loadData();
  }
}

</script>

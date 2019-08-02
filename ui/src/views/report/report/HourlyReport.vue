<template>
  <LineChart :data="lineData" style="width: 100%" />
</template>
<script>
import LineChart from '../../../components/Line/Line';
import mixin from './mixin';
export default {
  mixins: [mixin],
  components: {
    LineChart
  },
  data() {
    return {
      data: {}
    }
  },
  computed: {
    reportKey() {
      return `base.${this.report}.${this.reportType}.${this.date}`;
    },
    lineData() {
      return this.data || {};
    },
  },
  beforeMount() {
    this.loadData();
  }
}

</script>

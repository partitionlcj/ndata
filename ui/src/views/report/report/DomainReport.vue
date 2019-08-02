<template>
  <div>
    <PieChart :data="data" />
    <AisObjCol :data="data" download-xls :file-name="reportKey" />
  </div>
</template>
<script>
import PieChart from '../../../components/Pie/Pie';
import mixin from './mixin';
export default {
  mixins: [mixin],
  components: {
    PieChart
  },
  data() {
    return {
      data: {}
    }
  },
  computed: {
    reportKey() {
      return `base.${this.report}.${this.reportType}.${this.date}`;
    }
  },
  beforeMount() {
    this.loadData();
  }
}

</script>

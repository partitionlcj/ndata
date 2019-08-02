<template>
  <AisObjCol :data="data" :file-name="reportKey" download-xls />
</template>
<script>
import mixin from './mixin';
export default {
  mixins: [mixin],
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

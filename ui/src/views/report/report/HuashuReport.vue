<template>
  <AisObjCol :data="data" />
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
    reportKey() {
      return `ds-mars-prod.base.${this.report}.${this.reportType}.${this.date}`;
    }
  },
  beforeMount() {
    this.loadData();
  },
  methods: {
    async loadData() {
      let data = await this.getData(`${this.reportKey}`);
      this.data = data ? data : {};
    }
  }
}

</script>

import util from '../../../util';
import api from '../../../api/report';
export default {
  props: {
    reportType: {
      type: String,
      validator: function(val) {
        return util.oneOf(val, ['d', 'w', 'm']);
      }
    },
    report: {
      type: String,
      required: true
    },
    date: {
      type: String,
      required: true
    }
  },
  watch: {
    reportKey() {
      this.loadData();
    }
  },
  methods: {
    goToBadcase(key, label) {
      window.open(this.$aisUtil.getUrl(`/report/badcase?key=${key}&label=${label}`))
    },
    async getData(key) {
      let response = await api.getData(key);
      if (this.$aisUtil.hasStr(key, ',')) {
        return response.data;
      }
      return response.data[key];
    },
    async loadData() {
      this.data = await this.getData(this.reportKey);
    }
  }
}

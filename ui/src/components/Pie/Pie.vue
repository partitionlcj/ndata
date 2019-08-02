<template>
  <div>
    <chart :options="option" auto-resize theme="light" :style="pieStyle"></chart>
    <AisObjCol :data="data" v-if="showTable" :download-xls="downloadXls" :file-name="fileName" />
  </div>
</template>
<script>
import util from '../../util';
export default {
  props: {
    data: Object,
    showTable: {
      type: Boolean,
      default: false
    },
    showTitle: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: ''
    },
    limit: {
      type: Number
    },
    pieStyle: Object,
    fileName: String,
    downloadXls: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      pieData: []
    }
  },
  mounted() {
    let temp = util.getPieContentFromObj(this.data, this.limit);
    this.pieData = temp.data;
  },
  watch: {
    data() {
      let temp = util.getPieContentFromObj(this.data, this.limit);
      this.pieData = temp.data;
    }
  },
  computed: {
    option() {
      var opt = {
        tooltip: {
          trigger: 'item',
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          data: Object.keys(this.data)
        },
        series: [{
          name: 'domain',
          type: 'pie',
          radius: '55%',
          center: ['50%', '60%'],
          data: this.pieData,
          itemStyle: {
            emphasis: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }]
      };
      if (this.showTitle) {
        opt.title = {
          text: this.title,
          x: 'center'
        }
      }
      return opt;
    }
  }
}

</script>

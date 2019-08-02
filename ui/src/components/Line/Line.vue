<template>
  <chart :options="option" auto-resize theme="light"></chart>
</template>
<script>
export default {
  props: {
    data: Object
  },
  computed: {
    lineData() {
      return this.legend.map(item => this.data[item]);
    },
    legend() {
      let res = [];
      for (let i = 0; i < 24; i++) {
        res.push(i);
      }
      return res;
    },
    option() {
      return {
        tooltip: {
          trigger: 'item',
          formatter: "{c}"
        },
        xAxis: {
          type: 'category',
          data: this.legend
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: this.lineData,
          type: 'line',
          label: {
            show: true
          }
        }]
      };
    }

  }
}

</script>

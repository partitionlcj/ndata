<template>
  <chart :options="option" auto-resize theme="light"></chart>
</template>
<script>
export default {
  props: {
    data: [Object, Array],
    legendData: Array
  },
  computed: {
    barData() {
      return this.legendData ? this.data : this.legend.map(item => this.data[item]);
    },
    legend() {
      return this.legendData || Object.keys(this.data);
    },
    option() {
      var opt = {
        tooltip: {
          trigger: 'item',
          formatter: "{c}"
        },
        xAxis: {
          type: 'category',
          data: this.legend,
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: this.barData,
          type: 'bar'
        }]
      };
      return opt;
    }
  }
}

</script>

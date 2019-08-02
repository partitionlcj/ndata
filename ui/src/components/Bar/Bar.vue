<template>
  <chart :options="option" auto-resize theme="light"></chart>
</template>
<script>
export default {
  props: {
    data: Object
  },
  computed: {
    barData() {
      return this.legend.map(item => this.data[item]);
    },
    legend() {
      return Object.keys(this.data);
    },
    option() {
      var opt = {
        xAxis: {
          type: 'value'
        },
        yAxis: {
          type: 'category',
          data: this.legend
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

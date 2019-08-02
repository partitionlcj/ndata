<template>
  <chart :options="option" auto-resize theme="light" style="width: 100%"></chart>
</template>
<script>
export default {
  props: {
    title: String,
    legend: Array,
    xAxisData: Array,
    series: Array,
    ymin: {
      type: Number,
      default: 0
    },
    yFormatter: {
      type: String,
      default: '{value}%'
    },
    legendOrient: {
      type: String,
      default: 'horizontal',
      validator: function(value) {
        return ['horizontal', 'vertical'].indexOf(value) !== -1
      }
    }
  },
  computed: {
    option() {
      return {
        title: {
          text: this.title,
        },
        tooltip: {
          trigger: 'axis',
        },
        legend: {
          data: this.legend,
          orient: this.legendOrient,
          right: this.legendOrient === 'vertical' ? 'right' : undefined,
          top: this.legendOrient === 'vertical' ? 'center' : undefined
        },
        grid: {
          left: '4%',
          right: this.legendOrient === 'vertical' ? '15%' : '4%',
          bottom: 0,
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: this.xAxisData
        },
        yAxis: {
          type: 'value',
          min: this.ymin,
          axisLabel: {
            formatter: this.yFormatter
          }
        },
        series: this.series
      };
    }
  }
}

</script>

<template>
  <chart :options="option" auto-resize theme="light"></chart>
</template>
<script>
export default {
  props: {
    data: Array,
    legendData: Array
  },
  computed: {
    option() {
      var opt = {
        tooltip: {
          trigger: 'item',
          formatter: "{a} <br/>{b} : {c}"
        },
        toolbox: {
          feature: {
            dataView: { readOnly: false },
            restore: {},
            saveAsImage: {}
          }
        },
        legend: {
          data: this.legend
        },
        calculable: true,
        series: [{
          name: '漏斗图',
          type: 'funnel',
          left: '10%',
          top: 60,
          //x2: 80,
          bottom: 60,
          width: '80%',
          // height: {totalHeight} - y - y2,
          min: 0,
          max: 100,
          minSize: '0%',
          maxSize: '100%',
          sort: 'descending',
          gap: 2,
          label: {
            normal: {
              show: true,
              position: 'inside'
            },
            emphasis: {
              textStyle: {
                fontSize: 20
              }
            }
          },
          labelLine: {
            normal: {
              length: 10,
              lineStyle: {
                width: 1,
                type: 'solid'
              }
            }
          },
          itemStyle: {
            normal: {
              borderColor: '#fff',
              borderWidth: 1
            }
          },
          data: this.data
        }]
      };
      return opt;
    }

  }
}

</script>

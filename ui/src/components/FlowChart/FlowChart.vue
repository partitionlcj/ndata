<template>
  <chart :options="option" auto-resize theme="light"></chart>
</template>
<script>
import echarts from 'echarts';
export default {
  props: {
    data: {
      type: Array,
      default: () => []
    },
    unit: {
      type: String,
      default: ''
    },
    title: String,
  },
  computed: {
    option() {
      return {
        tooltip: {
          formatter: (params) => {
            return params.marker + params.data.name + ': ' + params.value[3].toLocaleString() + this.unit;
          }
        },
        title: {
          text: this.title,
          left: 'center'
        },
        dataZoom: [{
          type: 'slider',
          filterMode: 'weakFilter',
          showDataShadow: false,
          top: 400,
          height: 10,
          borderColor: 'transparent',
          backgroundColor: '#e2e2e2',
          handleIcon: 'M10.7,11.9H9.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4h1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7v-1.2h6.6z M13.3,22H6.7v-1.2h6.6z M13.3,19.6H6.7v-1.2h6.6z', // jshint ignore:line
          handleSize: 20,
          handleStyle: {
            shadowBlur: 6,
            shadowOffsetX: 1,
            shadowOffsetY: 2,
            shadowColor: '#aaa'
          },
          labelFormatter: ''
        }, {
          type: 'inside',
          filterMode: 'weakFilter'
        }],
        grid: {
          height: 300
        },
        xAxis: {
          min: 0,
          scale: true,
          axisLabel: {
            formatter: (val) => {
              return val + ' ms';
            }
          }
        },
        yAxis: {
          data: ['前端性能报表']
        },
        series: [{
          type: 'custom',
          renderItem: this.renderItem,
          encode: {
            x: [1, 2],
            y: 0
          },
          label: {
            normal: {
              show: true,
              color: 'black',
              fontSize: 10,
              formatter: (params) => {
                return params.data.name + '\n' + params.value[3].toLocaleString() + this.unit
              }
            }
          },
          data: this.data
        }]
      };
    }
  },
  methods: {
    renderItem(params, api) {
      var categoryIndex = api.value(0);
      var start = api.coord([api.value(1), categoryIndex]);
      var end = api.coord([api.value(2), categoryIndex]);
      var type = api.value(4);
      var height = api.size([0, 1])[1] * 0.6;
      var y = start[1] - height / 2;
      if (type === 'local_nlu') {
        y = start[1];
      }
      if (type === 'local_nlu' || type === 'cloud_nlu') {
        height = height / 2;
      }

      var rectShape = echarts.graphic.clipRectByRect({
        x: start[0],
        y: y,
        width: end[0] - start[0],
        height: height
      }, {
        x: params.coordSys.x,
        y: params.coordSys.y,
        width: params.coordSys.width,
        height: params.coordSys.height
      });

      return rectShape && {
        type: 'rect',
        shape: rectShape,
        style: api.style()
      };
    }
  }
}

</script>

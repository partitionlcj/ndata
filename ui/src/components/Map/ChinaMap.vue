<template>
  <chart :options="options" auto-resize theme="light"></chart>
</template>
<script>
import GEO_COORD_MAP from '../../config/cityChina.json';

export default {
  props: {
    data: Array,
    title: String,
    max: Number
  },
  computed: {
    options() {
      return {
        backgroundColor: '#404a59',
        title: {
          text: this.title,
          x: 'center',
          textStyle: {
            color: '#fff'
          },
          padding: 25
        },
        toolbox: {
          feature: {
            restore: {},
            saveAsImage: {}
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: function(params) {
            return params.name + ' : ' + params.value[2];
          }
        },
        visualMap: {
          min: 0,
          max: this.max,
          left: 200,
          calculable: true,
          inRange: {
            color: ['#50a3ba', 'yellow']
          },
          textStyle: {
            color: '#fff'
          }
        },
        geo: {
          map: 'china',
          label: {
            emphasis: {
              show: false
            }
          },
          itemStyle: {
            normal: {
              areaColor: '#323c48',
              borderColor: '#111'
            },
            emphasis: {
              areaColor: '#2a333d'
            }
          }
        },
        series: [{
          name: this.title,
          type: 'scatter',
          coordinateSystem: 'geo',
          data: this.convertData(this.data),
          symbolSize: 10,
          label: {
            normal: {
              show: false
            },
            emphasis: {
              show: false
            }
          },
          itemStyle: {
            emphasis: {
              borderColor: '#fff',
              borderWidth: 1
            }
          }
        }, {
          name: 'Top 5',
          type: 'scatter',
          coordinateSystem: 'geo',
          data: this.convertData(this.data.sort(function(a, b) {
            return b.value - a.value;
          }).slice(0, 6)),
          symbolSize: function(val) {
            return val[2] / 100;
          },
          showEffectOn: 'render',
          rippleEffect: {
            brushType: 'stroke'
          },
          hoverAnimation: true,
          label: {
            normal: {
              formatter: '{b}',
              position: 'right',
              show: true
            }
          },
          itemStyle: {
            normal: {
              color: 'red',
              shadowBlur: 10,
              shadowColor: '#333'
            }
          },
          zlevel: 1
        }]
      }
    }
  },
  methods: {
    findCord(map, city) {
      if (this.$aisUtil.hasStr(map.name, city)) {
        return map.center;
      } else if (map.children) {
        for (let i = 0; i < map.children.length; i++) {
          let currentMap = map.children[i];
          let res = this.findCord(currentMap, city);
          if (res) return res;
        }
      }
    },
    convertData(data) {
      let res = [];
      for (let i = 0; i < data.length; i++) {
        let geoCoord = this.findCord(GEO_COORD_MAP, data[i].name);
        if (geoCoord) {
          res.push({
            name: data[i].name,
            value: geoCoord.concat(data[i].value)
          });
        } else {
          console.log(data[i].name);
        }
      }
      return res;
    }
  }
}

</script>

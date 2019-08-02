<template>
  <div>
    <AisTable :columns="columns" :data="data" :show-page="false" class="margin-bottom-10" />
    <AisTable :columns="badCaseColumn" :data="badCaseData" :show-page="false" class="margin-bottom-10" />
    <chart v-if="reportType==='m'" :options="option" auto-resize theme="light" style="width: 100%; min-height: 600px"></chart>
    <div class="text-align-center">
      <Tag type="dot" v-for="tag in tags" :color="tag.color" :key="tag.name">{{tag.name}}</Tag>
    </div>
  </div>
</template>
<script>
import util from '../../../util';
import { NAVI_FUNNEL_TYPE, CALL_FUNNEL_TYPE } from '../../../config/const';
import columns from '../../../config/column';
import mixin from './mixin';
import echarts from 'echarts';
export default {
  mixins: [mixin],
  data() {
    return {
      colors: ['#7b9ce1', '#bd6d6c', '#75d874', '#e0bc78', '#dc77dc', '#72b362', ''],
      data: [],
      badCaseColumn: [],
      badCaseData: [],
      funnelCategory: [],
      funnelData: []
    }
  },
  beforeMount() {
    this.processBadcaseColumn();
  },
  watch: {
    badCaseColumn() {
      this.processBadcaseColumn();
    }
  },
  computed: {
    columns() {
      return columns[this.report];
    },
    reportKey() {
      return `optimization.${this.report}.${this.reportType}.${this.date}`;
    },
    graphTitle() {
      return `${this.reportKey}意图流转`;
    },
    badcaseKey() {
      return `optimization.${this.report}_fail.${this.reportType}.${this.date}`;
    },
    badcaseDetailKey() {
      let key = this.reportKey.split(/[._]/).slice(1);
      if (this.report === 'navigation_funnel') {
        key[0] = 'nav';
      }
      return key.join('.');
    },
    graphKey() {
      return `optimization.${this.report}_graph.${this.reportType}.${this.date}`;
    },
    tags() {
      return this.funnelData.map((item, index) => ({ color: this.colors[index], name: item.name }));
    },
    funnelGraphData() {
      let seriesData = [];
      let gap = 0;
      this.funnelData.forEach((item, index) => {
        for (let i = 0; i < item.data.length; i++) {
          let seriesItem = {
            name: item.name,
            itemStyle: {
              "normal": {
                color: this.colors[index]
              }
            }
          }
          let data = [];
          data.push(item.data.length - i - 1);
          let start;
          if (index === 0) {
            start = gap * (i + 1);
          } else {
            start = seriesData[seriesData.length - item.data.length].value[2];
          }
          data.push(start);
          data.push(start + item.data[i]);
          data.push(item.data[i]);
          if (i === 0) {
            data.push(undefined);
          } else {
            data.push(Number((item.data[i] / item.data[0]) * 100).toFixed(2));
          }
          seriesItem.value = data;
          seriesData.push(seriesItem);
        }
      });
      return seriesData;
    },
    graphCategory() {
      let total = 0;
      return this.funnelCategory.map((item, index) => {
        let sum = 0;
        this.funnelData.forEach(data => {
          sum += data.data[index];
        });
        let rate = 100;
        if (index > 0) {
          rate = Number((sum / total) * 100).toFixed(2);
        } else {
          total = sum;
        }
        return `${item}\n（${sum}）(${rate}%)`;
      }).reverse();
      return this.funnelCategory.reverse();
    },
    option() {
      return {
        tooltip: {
          formatter: function(params) {
            if (params.value[4]) {
              return `${params.marker}${params.data.name}:${params.value[3]}(${params.value[4]}%)`;
            } else {
              return `${params.marker}${params.data.name}:${params.value[3]}`;
            }
          }
        },
        title: {
          text: this.graphTitle,
        },
        xAxis: {
          show: false,
        },
        yAxis: {
          data: this.graphCategory,
          axisLine: {
            show: false
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            inside: false
          }
        },
        legend: {
          data: this.legendData
        },
        series: [{
          type: 'custom',
          renderItem: this.renderItem,
          label: {
            normal: {
              show: true,
              formatter: function(params) {
                return params.value[3];
              },
              position: 'top'
            }
          },
          encode: {
            x: [1, 2],
            y: 0
          },
          data: this.funnelGraphData
        }]
      };
    }
  },
  beforeMount() {
    this.loadData();
  },
  methods: {
    async loadData() {
      let data = await this.getData(this.reportKey);
      this.data = data ? data.data : [];
      let badData = await this.getData(this.badcaseKey);
      if (badData) {
        this.badCaseColumn = badData.head;
        this.badCaseData = badData.data;
      }
      if (this.reportType === 'm') {
        let graphData = await this.getData(this.graphKey);
        if (graphData) {
          this.funnelCategory = graphData.category;
          this.funnelData = graphData.data;
        }
      }
    },
    processBadcaseColumn() {
      if (this.badCaseColumn && this.reportType === 'd') {
        this.badCaseColumn.forEach((item, index) => {
          if (index > 0) {
            item.align = 'center';
            item.render = (h, params) => {
              return h('Button', {
                props: {
                  size: 'small'
                },
                on: {
                  click: () => {
                    let processKey = item.key.match(/\d+/)[0];
                    processKey = this.$aisUtil.hasStr(this.badcaseKey, 'nav') ? +processKey + 1 : processKey;
                    let intent = params.row.intent === '总计' ? '' : `${params.row.intent}.`;
                    this.goToBadcase(`${this.badcaseDetailKey}.${intent}${processKey}`, `${this.badcaseKey}.${params.row.intent}`);
                  }
                }
              }, params.row[item.key]);
            }
          }
        })
      }
    },
    renderItem(params, api) {
      let categoryIndex = api.value(0);
      let start = api.coord([api.value(1), categoryIndex]);
      let end = api.coord([api.value(2), categoryIndex]);
      let height = api.size([0, 1])[1] * 0.6;
      let rectShape = echarts.graphic.clipRectByRect({
        x: start[0],
        y: start[1] - height / 2,
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

<!-- 前端性能报表 -->
<template>
  <div>
    <Select v-model="env" class="width-200" placeholder="请选择环境">
      <Option v-for="item in envs" :key="item" :value="item">{{item}}</Option>
    </Select>
    <Select v-model="option" class="width-200" placeholder="请选择查看选项">
      <Option v-for="item in options" :key="item" :value="item">{{item}}</Option>
    </Select>
    <Select v-model="dimension" class="width-200" placeholder="请选择查看维度">
      <Option v-for="item in dimensions" :key="item" :value="item">{{item}}</Option>
    </Select>
    <Select v-model="version" class="width-400" placeholder="请选择查看的版本">
      <Option v-for="item in versions" :key="item" :value="item">{{item}}</Option>
    </Select>
    <AisObjCol :data="count" class="margin-top-10 margin-bottom-10" v-if="Object.keys(count).length" />
    <FlowChart :data="chartData" class="performance-chart" :unit="unit" title="详细信息" />
    <FlowChart :data="summaryChatData" class="performance-chart" :unit="unit" title="汇总信息" />
    <AisTable :data="descData" :columns="descHeader" :show-page="false" />
  </div>
</template>
<script type="text/javascript">
import { PERFORMANCE_LABEL, SUMMARY_PERFORMANCE_LABEL } from '../../../config/const';
import mixin from './mixin';
import FlowChart from '../../../components/FlowChart/FlowChart';
export default {
  mixins: [mixin],
  components: {
    FlowChart
  },
  data() {
    return {
      count: {},
      data: {},
      env: 'stag',
      dimension: '',
      version: '',
      option: 'count',
      options: ['avg', 'count', 'tp50', 'tp90', 'tp99'],
      descHeader: [{
        title: '',
        key: 'name',
        width: 250,
        render: (h, params) => {
          return h('Tag', {
            props: {
              color: params.row.color
            }
          }, params.row.name);
        }
      }, {
        title: '说明',
        key: 'comments'
      }]
    }
  },
  computed: {
    envs() {
      if (this.reportType === 'd') {
        return ['prod', 'stag'];
      } else {
        return ['stag'];
      }
    },
    reportKey() {
      return `${this.report}.${this.env}.${this.reportType}.${this.date}`;
    },
    unit() {
      if (this.option === 'count') {
        return '';
      }
      return 'ms';
    },
    dimensions() {
      return Object.keys(this.data);
    },
    versions() {
      try {
        return this.dimension ? Object.keys(this.data[this.dimension]) : [];
      } catch (e) {
        return [];
      }
    },
    chartData() {
      try {
        return this.getChartData(this.data, PERFORMANCE_LABEL.filter(label => !label.env || label.env === this.env));
      } catch (e) {
        return [];
      }
    },
    summaryChatData() {
      try {
        return this.getChartData(this.data, SUMMARY_PERFORMANCE_LABEL);
      } catch (e) {
        return [];
      }
    },
    descData() {
      return PERFORMANCE_LABEL.filter(label => !label.env || label.env === this.env).concat(SUMMARY_PERFORMANCE_LABEL)
    }
  },
  watch: {
    dimension() {
      this.version = this.versions[0];
    },
    data(newVal) {
      if (Object.keys(newVal).length > 0) {
        this.dimension = 'total';
      }
    }
  },
  beforeMount() {
    this.loadData();
  },
  methods: {
    getChartData(data, labelData) {
      if (Object.keys(data).length > 0) {
        let sum = 0;
        return labelData.map((item, index) => {
          const data = this.data[this.dimension][this.version];
          let start = sum;
          let duration = data[item.key][this.option];
          let end = start + duration;
          if (item.key !== 'local_nlu') {
            sum = end;
          }
          let tmp = { name: item.name, itemStyle: { normal: { color: item.color } }, value: [0, start, end, duration, item.key] };
          return tmp;
        });
      }
    },
    async loadData() {
      let data = await this.getData(`${this.reportKey}`);
      if (this.env === 'stag') {
        this.data = data ? data.data : {};
        this.count = data ? data.count : {};
        if (this.count && this.count.failRate) {
          this.count.failRate += '%';
        }
      } else {
        this.data = data ? data : {};
        this.count = {};
      }
    }
  }
}

</script>
<style scoped>
.performance-chart {
  width: 100%;
  height: 600px;
}

</style>

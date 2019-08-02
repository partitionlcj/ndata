<template>
  <div>
    <Select v-model="env" class="width-200" placeholder="请选择环境">
      <Option v-for="item in envs" :key="item" :value="item">{{item}}</Option>
    </Select>
    <Select v-model="dimension" class="width-200" placeholder="请选择查看维度">
      <Option v-for="item in dimensions" :key="item" :value="item">{{item}}</Option>
    </Select>
    <AisATable :columns="tableColumn" :data="tableData" class="margin-top-10"></AisATable>
  </div>
</template>
<script>
import mixin from './mixin';
import { PERFORMANCE_LABEL, SUMMARY_PERFORMANCE_LABEL } from '../../../config/const';

export default {
  mixins: [mixin],
  data() {
    return {
      env: 'stag',
      dimension: '',
      dimensions: [],
      tableColumn: [],
      tableData: [],
      data: null,
      types: ['avg', 'count', 'tp50', 'tp90', 'tp99']
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
    currentData() {
      try {
        if (this.env === 'stag') {
          return this.data.data[this.dimension];
        } else {
          return this.data[this.dimension];
        }
      } catch (e) {
        return null;
      }
    },
    processes() {
      return PERFORMANCE_LABEL.filter(label => !label.env || label.env === this.env).concat(SUMMARY_PERFORMANCE_LABEL)
    }
  },
  watch: {
    data() {
      this.getDimensions();
    },
    currentData(newVal) {
      if (newVal) {
        this.getColumns();
        this.processData();
      }
    }
  },
  beforeMount() {
    this.loadData()
  },
  methods: {
    getDimensions() {
      if (this.data) {
        if (this.env === 'stag') {
          this.dimensions = Object.keys(this.data.data);
        } else {
          this.dimensions = Object.keys(this.data);
        }
      } else {
        this.dimensions = [];
      }
    },
    getColumns() {
      let column = [{
        type: 'rowspan',
        title: '',
        key: 'process'
      }, {
        title: '',
        key: 'type'
      }];
      this.tableColumn = column.concat(Object.keys(this.currentData).map(key => ({ title: key, key: key })));
    },
    processData() {
      let data;
      let versions = Object.keys(this.currentData);
      data = this.processes.map(process => ({
        process: {
          title: process.name,
          key: process.key
        }
      }));
      data.forEach(item => {
        item.process.children = [];
        this.types.forEach(type => {
          let tmp = { type };
          versions.forEach(version => {
            let value = '-';
            try {
              value = this.currentData[version][item.process.key][type];
              tmp[version] = (value).toFixed(2);
            } catch (e) {
              tmp[version] = value;
            }
          });
          item.process.children.push(tmp);
        });
      });
      this.tableData = data;
    }
  }
}

</script>

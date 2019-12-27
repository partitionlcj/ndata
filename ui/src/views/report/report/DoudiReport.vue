<template>
  <AisTable :columns="columns" :data="tableData" :show-page="false" />
</template>
<script>
import { DAILY_NLU_TYPE } from '../../../config/const';
import mixin from './mixin';
export default {
  mixins: [mixin],
  data() {
    return {
      data: {},
    }
  },
  computed: {
    columns() {
      let column = [{
          title: '标签',
          key: 'label'
        },
        {
          title: '数量',
          key: 'num'
        },
        {
          title: '完成百分比',
          key: 'rate'
        }
      ];
      if (this.reportType === 'd') {
        column.push({
          title: 'badcase',
          align: 'center',
          render: (h, params) => {
            if (params.row.label !== '正常') {
              return h('Button', {
                props: {
                  size: 'small',
                  type: 'error'
                },
                on: {
                  click: () => {
                    this.goToBadcase(`${this.reportKey}.${params.row.key}`, params.row.label)
                  }
                }
              }, params.row.num)
            }
          }
        })
      }
      return column;
    },
    tableData() {
      let dict = this.getTypeDict(DAILY_NLU_TYPE)
      let data = {}
      let total = 0
      for (let key in this.data) {
        if (this.data.hasOwnProperty(key)) {
          data[dict[key]] = this.data[key]
          total += this.data[key]
        }
      }
      return this.getCTableData(dict, this.data, total);
    },
    reportKey() {
      return `ds-mars-prod.base.${this.report}.${this.reportType}.${this.date}`;
    }
  },
  beforeMount() {
    this.loadData();
  },
  methods: {
    getCTableData(dict, data, total) {
      let res = []
      for (let key in data) {
        if (data.hasOwnProperty(key)) {
          res.push({
            label: dict[key],
            num: data[key],
            rate: ((data[key] / total) * 100).toFixed(2) + '%',
            key: key
          })
        }
      }
      return res
    },
    getTypeDict(type) {
      let dict = {}
      Object.keys(type).forEach(item => {
        dict[type[item]] = item
      })
      return dict
    }
  }
}

</script>

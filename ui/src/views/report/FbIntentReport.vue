<!-- 实车用户intent分布 -->
<template>
  <div>
    <ButtonGroup>
      <Button v-for="dom in domains" :key="dom" @click="chooseDomain(dom)" :type="dom === domain?'primary':'default'">{{dom}}</Button>
    </ButtonGroup>
    <chart :options="option" auto-resize theme="light" class="pie-chart"></chart>
    <Table :columns="columns" :data="data" :loading="loading"></Table>
  </div>
</template>
<script>
import api from '../../api/report';
import util from '../../util';
export default {
  data() {
    return {
      option: {},
      loading: false,
      domain: 'CALL',
      domains: [
        'CALL',
        'COMMON',
        'DEVICE_CONTROL',
        'MEDIA',
        'NAVI',
        'OTHERS',
        'ROBOT',
        'WEATHER'
      ],
      columns: [{
        title: 'Intent',
        key: 'intent',
        align: 'center'
      }, {
        title: '记录数',
        key: 'num',
        align: 'center'
      }],
      data: []
    }
  },
  beforeMount() {
    this.getIntentData();
  },
  computed: {
    key() {
      return `ds-mars-prod.total.intents.${this.domain.toLowerCase()}`;
    }
  },
  watch: {
    domain() {
      this.getIntentData();
    }
  },
  methods: {
    chooseDomain(domain) {
      this.domain = domain;
    },
    async getIntentData() {
      this.loading = true;
      this.data = [];
      this.options = {};
      let intents = [];
      let intentData = [];
      let response = await api.getData(this.key);
      const data = response.data[this.key];
      for (let key in data) {
        if (data.hasOwnProperty(key)) {
          this.data.push({
            intent: key,
            num: data[key]
          })
        }
      }
      this.data.sort((a, b) => b.num - a.num);
      this.data.forEach((item, index) => {
        if (index < 12) {
          intents.push(item.intent);
          intentData.push({
            value: item.num,
            name: item.intent
          });
        }
      })
      this.option = this.getOption(this.domain, intents, intentData);
      this.loading = false;
    },
    getOption(domain, intents, intentData) {
      return {
        title: {
          text: `实车用户${domain} Intent分布`,
          x: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          data: intents
        },
        series: [{
          name: 'intent',
          type: 'pie',
          radius: '55%',
          center: ['50%', '60%'],
          data: intentData,
          itemStyle: {
            emphasis: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }]
      };
    },
    viewQueryDetail(domain, intent) {
      var targetUrl = this.$aisUtil.getUrl(`/report/query_detail/${domain}/${intent}`);
      window.open(targetUrl, '_blank');
    }
  }
}

</script>
<style scoped>
.pie-chart {
  margin: 20px auto;
  width: 90%;
  height: 600px;
}

</style>

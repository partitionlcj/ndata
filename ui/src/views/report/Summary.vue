<!-- 实车用户domain分布 -->
<template>
  <div>
    <ButtonGroup>
      <Button v-for="type in types" :key="type.key" @click="currentType=type.key" :type="currentType === type.key?'primary':'default'">{{type.title}}</Button>
    </ButtonGroup>
    <Pie :data="this.data" :title="pieTitle" :limit="limit" :pie-style="pieStyle" showTable></Pie>
  </div>
</template>
<script>
import api from '../../api/report';
import util from '../../util';
import Pie from '../../components/Pie/Pie'
export default {
  components: {
    Pie
  },
  data() {
    return {
      data: {},
      currentType: 'domain',
      types: [{
        title: 'Domain',
        key: 'domain'
      }, {
        title: 'Intent',
        key: 'intents'
      }, {
        title: '话术分类',
        key: 'huashu'
      }],
      pieStyle: {
        width: '80%',
        margin: '10px auto',
        height: '600px'
      }
    }
  },
  beforeMount() {
    this.getPieChartData();
  },
  computed: {
    key() {
      return `ds-mars-prod.total.${this.currentType}`;
    },
    pieTitle() {
      return `实车 ${this.currentType} 分布`
    },
    limit() {
      if (this.currentType === 'intents') {
        return 12;
      }
    }
  },
  watch: {
    currentType() {
      this.getPieChartData();
    }
  },
  methods: {
    async getPieChartData() {
      let response = await api.getData(this.key);
      this.data = response.data[this.key];
    }
  }
}

</script>

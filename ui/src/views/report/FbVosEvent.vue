<template>
  <div>
    <InfoModal v-model="showModal" :data="sysResult"></InfoModal>
    <Row class="margin-bottom-20" :gutter="16">
      <Col span="4" class="margin-bottom-10">
        <DatePicker :value="filter.date" format="yyyy-MM-dd" type="daterange" placement="bottom-end" placeholder="Select date" @on-change="dateChange" style="width: 100%"></DatePicker>
      </Col>
      <template>
        <Col span="5" class="margin-bottom-10">
          <Input placeholder="vehicle_id" v-model="filter.vid" @on-enter="pageChange(1)"></Input>
        </Col>
        <Col span="2" class="margin-bottom-10">
        <Input placeholder="env" v-model="filter.env" @on-enter="pageChange(1)"></Input>
        </Col>
      </template>
      <Col span="3" class="margin-bottom-10">
      <Input placeholder="app_id" v-model="filter.app_id" @on-enter="pageChange(1)"></Input>
      </Col>
      <Col span="4" class="margin-bottom-10">
        <Input placeholder="event_type" v-model="filter.event_type" @on-enter="pageChange(1)"></Input>
      </Col>
    </Row>
    <Table :columns="columns" :data="data" :loading="loading" :row-class-name="currentViewRowCls" class="detail-table"></Table>
    <div class="page">
      <Page :current="pagination.page" :total="pagination.total" :page-size="pagination.pageSize" @on-change="pageChange" show-elevator show-total></Page>
    </div>
  </div>
</template>
<script>
import api from '../../api';
import real from '../../api/real';
import InfoModal from '../../components/Modal/InfoModal';
import util from '../../util';
export default {
  components: {
    InfoModal
  },
  data() {
    return {
      currentSessionId: '',
      reportName: '',
      loading: false,
      showModal: false,
      sysResult: '',
      pagination: {
        page: 1,
        pageSize: 30,
        total: 0
      },
      filter: {
        date: [],
        event_type: '',
        env: '',
        vid: '',
        app_id: ''
      },
      data: [],
      currentViewRow: -1
    }
  },
  watch: {
    showModal(newVal) {
      if (!newVal) {
        this.sysResult = '';
      }
    }
  },
  computed: {
    columns() {
      let columns = []
    
      columns.push({
        title: 'vid',
        key: 'vid',
        width: 80,
        render: (h, params) => {
          return h('Tooltip', {
            props: {
              content: params.row.vid
            }
          }, params.row.vid.slice(params.row.vid.length - 5));
        }
      });

      columns.push( {
          title: 'env',
          key: 'env',
          minWidth: 110,
          maxWidth: 110,
        })
      
      columns.push({
        title: 'app_id',
        key: 'app_id',
        minWidth: 110,
        maxWidth: 110
      });
      columns.push({
        title: 'date',
        key: 'date',
        minWidth: 190,
        maxWidth: 190
      });
      columns.push({
        title: 'event_type',
        minWidth: 230,
        maxWidth: 230,
        key: 'event_type',
      });

      columns.push( {
          title: 'event_data',
          key: 'event_data',
          minWidth: 300
        }
      )
      return columns;
    }
  },
  beforeMount() {
    this.reportName = 'vos-event';
    
    this.domain = this.$route.params.domain;
    this.intent = this.$route.params.intent === 'null' ? '' : this.$route.params.intent;

    let now = util.getTodayDate();
    this.filter.date = [now, now];
    this.getVosEvent();
  },
  methods: {
    async getVosEvent(exportCsv) {
      this.currentViewRow = -1; // 只要重新获取数据就重置当前查看的行
      
      let begin_date = undefined;
      let end_date = undefined;
      let { event_type, env, vid, app_id } = this.filter;

      if (this.filter.date.length > 0) {
        begin_date = this.filter.date[0] ? `${this.filter.date[0]} 00:00:00` : undefined;
        end_date = this.filter.date[1] ? `${this.filter.date[1]} 23:59:59` : undefined;
      }
      this.loading = true;
      let response;
      response = await api.getVosEventData(new Date(begin_date).getTime(), new Date(end_date).getTime(), app_id.toLowerCase(), event_type.toLowerCase(), vid.toLowerCase(), env.toLowerCase(), this.pagination.page, this.pagination.pageSize);
      
      this.loading = false;
      let data = response.data;
      this.data = data.data.map((item) => ({
        vid: item[0],
        date: new Date(item[1]).toLocaleString("zh-CN"),
        app_id: item[2],
        event_type: item[3],
        event_data: item[4],
        env: item[5]
      }));
      this.pagination.total = data.total;
    },
    pageChange(page) {
      document.querySelector('.content').scrollTop = 0; //翻页回到页面顶部
      this.pagination.page = page;
      this.getVosEvent();
    },
    dateChange(val) {
      this.filter.date = val;
      this.pagination.page = 1;
    },
    exportCsv() {
      this.getVosEvent(true);
    },
    currentViewRowCls(row, index) {
      if (index === this.currentViewRow) {
        return 'viewing-row';
      }
      if (row.hasSubmited) {
        return 'submited-row';
      }
      return '';
    }
  }
}

</script>
<style scoped>
.detail-table>>>.viewing-row td {
  background-color: #00bebe;
}

.detail-table>>>.submited-row td {
  background-color: #c5c8ce;
}

</style>

<template>
  <div>
    <InfoModal v-model="showModal" :data="sysResult"></InfoModal>
    <Row class="margin-bottom-20" :gutter="16">
      <Col span="4" class="margin-bottom-10">
        <DatePicker :value="filter.date" format="yyyy-MM-dd" type="daterange" placement="bottom-end" placeholder="Select date" @on-change="dateChange" style="width: 100%"></DatePicker>
      </Col>
      <template>
        <Col span="4" class="margin-bottom-10">
          <Input placeholder="request_id" v-model="filter.requestId" @on-enter="pageChange(1)"></Input>
        </Col>
        <Col span="2" class="margin-bottom-10">
        <Input placeholder="env" v-model="filter.env" @on-enter="pageChange(1)"></Input>
        </Col>
      </template>
      <Col span="6" class="margin-bottom-10">
      <Input placeholder="query" v-model="filter.query" @on-enter="pageChange(1)"></Input>
      </Col>
      <template v-if="reportName=='fact-data'">
        <Col span="4" class="margin-bottom-10">
        <Input placeholder="vid" v-model="filter.vid" @on-enter="pageChange(1)"></Input>
        </Col>
        <Col span="4" class="margin-bottom-10">
        <Input placeholder="appId" v-model="filter.appId" @on-enter="pageChange(1)"></Input>
        </Col>
      </template>
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
        query: '',
        env: '',
        vid: '',
        appId: '',
        requestId: ''
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
      let columns = [
        {
        title: 'reqId',
        key: 'request_id',
        width: 80,
        render: (h, params) => {
          return h('Tooltip', {
            props: {
              content: params.row.request_id
            }
          }, params.row.request_id.slice(params.row.request_id.length - 5));
        }
      }]
      
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
      
      columns.push({
        title: 'appId',
        key: 'app_id',
        minWidth: 150,
      });
      columns.push({
        title: 'query',
        key: 'query',
        minWidth: 150,
      })
      columns.push({
          title: 'env',
          key: 'env',
          minWidth: 80
        }, {
          title: '音频',
          width: 70,
          render: (h, params) => {
            return h('AisAudio', {
              props: {
                url: `/api/audio/download_wav?requestId=${params.row.request_id}`,
                size: 14
              }
            })
          }
        }
        )
      //}
      columns.push({
        title: '更新时间',
        key: 'timestamp',
        minWidth: 100,
      });
      columns.push({
        title: '云端日志',
        width: 100,
        align: 'center',
        key: 'detail',
        render: (h, params) => {
          return h('Button', {
            props: {
              type: 'primary',
              size: 'small'
            },
            on: {
              click: () => {
                this.currentViewRow = params.row._index;
                window.open("/api/debug/getReqInfo?rid="+params.row.request_id, "_blank")
              }
            }
          }, 'ReqInfo');
        }
      })
      columns.push({
        title: 'vos日志',
        width: 100,
        align: 'center',
        key: 'detail',
        render: (h, params) => {
          return h('Button', {
            props: {
              type: 'primary',
              size: 'small'
            },
            on: {
              click: () => {
                this.currentViewRow = params.row._index;
                window.open("/api/debug/getVosReqInfo?rid="+params.row.request_id, "_blank")
              }
            }
          }, 'ReqInfo');
        }
      })

      return columns;
    }
  },
  beforeMount() {
    this.reportName = 'fact-data';
    this.domain = this.$route.params.domain;
    this.intent = this.$route.params.intent === 'null' ? '' : this.$route.params.intent;
    let now = util.getTodayDate();
    //let now = '2019-06-01';
    this.filter.date = [now, now];
    this.getDomainIntentQueryDetail();
  },
  methods: {
    async getDomainIntentQueryDetail(exportCsv) {
      this.currentViewRow = -1; // 只要重新获取数据就重置当前查看的行
      if (!!this.filter.vin) {
        let vidRes = await real.getVid(this.filter.vin)
        if (vidRes.state !== 'success' || vidRes.data.total === 0) {
          this.$Message.error('没有该vid的数据');
          return;
        } else {
          this.filter.vid = vidRes.data.data[0][0];
        }
      }

      let begin_date = undefined;
      let end_date = undefined;
      let { requestId, sessionId, query, domain, operation, intent, vid, appId, env, wakeup_asr_text } = this.filter;

      operation = operation

      if (this.filter.date.length > 0) {
        begin_date = this.filter.date[0] ? `${this.filter.date[0]} 00:00:00` : undefined;
        end_date = this.filter.date[1] ? `${this.filter.date[1]} 23:59:59` : undefined;
      }
      this.loading = true;
      let response;
      
      response = await api.getAsrDebugData(new Date(begin_date).getTime(), new Date(end_date).getTime(), requestId.toLowerCase().trim(),  query.toLowerCase().trim(),vid.toLowerCase().trim(), env.toLowerCase().trim(), appId.trim(), this.pagination.page, this.pagination.pageSize);
    
      this.loading = false;
      let data = response.data;
      this.data = data.data.map((item) => ({
        query: item[0],
        vid: item[2],
        timestamp: new Date(item[1]).toLocaleString("zh-CN"),
        request_id: item[3],
        env: item[4],
        app_id:item[5],
        hasSubmited: false
      }));
      this.pagination.total = data.total;
    },
    pageChange(page) {
      document.querySelector('.content').scrollTop = 0; //翻页回到页面顶部
      this.pagination.page = page;
      this.getDomainIntentQueryDetail();
    },
    async viewDetail(sessionId,requestId) {
      this.currentSessionId = sessionId;
      let response = await api.getRequestInfo(requestId);
      if (response.state === 'success') {
        this.sysResult = response.data;
        console.log(this.sysResult)
        this.showModal = true;
      }
    },
    dateChange(val) {
      this.filter.date = val;
      this.pagination.page = 1;
    },
    exportCsv() {
      this.getDomainIntentQueryDetail(true);
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

<template>
  <div>
    <InfoModal v-model="showModal" :data="sysResult"></InfoModal>
    <Row class="margin-bottom-20" :gutter="16">
      <Col span="4" class="margin-bottom-10">
        <DatePicker :value="filter.date" format="yyyy-MM-dd" type="daterange" placement="bottom-end" placeholder="Select date" @on-change="dateChange" style="width: 100%"></DatePicker>
      </Col>
      <Col span="3" class="margin-bottom-10">
        <Input placeholder="request_id" v-model="filter.requestId" @on-enter="pageChange(1)"></Input>
      </Col>
      <Col span="2" class="margin-bottom-10">
        <Input placeholder="session_id" v-model="filter.sessionId" @on-enter="pageChange(1)"></Input>
      </Col>
      <Col span="3" class="margin-bottom-10">
        <Input placeholder="vossdk_ver" v-model="filter.vossdk_ver" @on-enter="pageChange(1)"></Input>
      </Col>
      <Col span="2" class="margin-bottom-10">
      <Input placeholder="env" v-model="filter.env" @on-enter="pageChange(1)"></Input>
      </Col>
      <Col span="6" class="margin-bottom-10">
      <Input placeholder="query" v-model="filter.query" @on-enter="pageChange(1)"></Input>
      </Col>
      
      <Col span="4" class="margin-bottom-10">
      <Input placeholder="vid" v-model="filter.vid" @on-enter="pageChange(1)"></Input>
      </Col>
      <Col span="2" class="margin-bottom-10">
      <Input placeholder="appId" v-model="filter.appId" @on-enter="pageChange(1)"></Input>
      </Col>
      <Col span="2" class="margin-bottom-10">
      <Input placeholder="domain" v-model="filter.domain" @on-enter="pageChange(1)"></Input>
      </Col>
      <Col span="2" class="margin-bottom-10">
      <Input placeholder="operation;搜空请输入null" v-model="filter.operation" @on-enter="pageChange(1)"></Input>
      </Col>
      <Col span="2" class="margin-bottom-10">
        <Input placeholder="intent" v-model="filter.intent" @on-enter="pageChange(1)"></Input>
      </Col>
        <Col span="2" class="margin-bottom-10">
        <Input placeholder="唤醒词" v-model="filter.wakeup_asr_text" @on-enter="pageChange(1)"></Input>
      </Col>
      <Col span="14" class="margin-bottom-10">
          <Input placeholder="自定义查询，会覆盖其他条件, 示例: app_id='100240001' and env !='ds-gn-stg'" v-model="filter.customQuery" @on-enter="pageChange(1)"></Input>
        </Col>
      </Col>
    </Row>
    <Table :columns="columns" :data="data" :loading="loading" :row-class-name="currentViewRowCls" class="detail-table"></Table>
    <div class="page">
      <Page :current="pagination.page" :total="pagination.total" :page-size="pagination.pageSize" @on-change="pageChange" show-elevator show-total></Page>
    </div>
  </div>
</template>
<script>
import aisTool from 'mars-common';
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
      domain: '',
      intent: '',
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
        domain: '',
        vid: '',
        appId: '',
        operation: '',
        intent: '',
        sessionId: '',
        requestId: '',
        vossdk_ver: '',
        wakeup_asr_text: '',
        customQuery: ''
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
      },{
        title: 'sesId',
        key: 'session_id',
        width: 80,
        render: (h, params) => {
          return h('Tooltip', {
            props: {
              content: params.row.session_id
            }
          }, params.row.session_id.slice(params.row.session_id.length - 5));
        }
      }
      ]
      if (this.reportName === 'fact-data') {
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
        }, {
          title: 'domain',
          key: 'domain',
          minWidth: 70
        });
      }
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
        title: 'tts',
        minWidth: 200,
        render: (h, params) => {
          let tts = JSON.parse(params.row.tts);
          return h('ul', tts.map(item => h('li', item.content)));
        }
      });
      //if (this.reportName === 'fact-data') {
        columns.push({
          title: 'intent',
          key: 'intent',
          minWidth: 100
        }, 
        {
          title: 'vossdk_ver',
          key: 'vossdk_ver',
          minWidth: 100
        },{
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
        },
        {
          title: '唤醒',
          width: 90,
          render: (h, params) => {
            console.log(params.row)
            if( params.row.wakeup === 1){
              return h('AisAudio', {
                props: {
                  url: `/api/audio/wakeup_wav?requestId=${params.row.request_id}`,
                  size: 14
                }
              })
            }
            else{
              return h('div', "N/A")
            }
            
          }
        },
        {
          title: '唤醒词',
          key: 'wakeup_asr_text',
          minWidth: 100,
        }
        )
      //}
      columns.push({
        title: '更新时间',
        key: 'updated_at',
        minWidth: 100,
      }, {
        title: '详情',
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
                this.viewDetail(params.row.session_id,params.row.request_id);
              }
            }
          }, '详情');
        }
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
    this.filter.customQuery = aisTool.Cookie.getData("vos_debug_query.custom") + ""
    if( this.filter.customQuery == "undefined" ){
      this.filter.customQuery = ""
    }

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
      let { requestId, sessionId, query, domain, operation, intent, vid, appId, env, vossdk_ver, wakeup_asr_text, customQuery } = this.filter;

      operation = operation

      if (this.filter.date.length > 0) {
        begin_date = this.filter.date[0] ? `${this.filter.date[0]} 00:00:00` : undefined;
        end_date = this.filter.date[1] ? `${this.filter.date[1]} 23:59:59` : undefined;
      }
      this.loading = true;
      let response;
      
      response = await api.getVosDebugData(begin_date, end_date, requestId.toLowerCase().trim(), sessionId.toLowerCase().trim(), query.toLowerCase().trim(), domain.toLowerCase().trim(), vid.toLowerCase().trim(), operation.toLowerCase().trim(), intent.toLowerCase().trim(), env.toLowerCase().trim(), wakeup_asr_text.toUpperCase().trim(), appId.trim(), vossdk_ver.toLowerCase().trim(), customQuery, this.pagination.page, this.pagination.pageSize);
      aisTool.Cookie.setData("vos_debug_query.custom",customQuery)
      this.loading = false;
      let data = response.data;
      this.data = data.data.map((item) => ({
        session_id: item[4],
        query: item[0],
        vid: item[5],
        domain: item[6],
        intent: item[7],
        operation: item[8],
        updated_at: new Date(item[1]).toLocaleString("zh-CN"),
        tts: item[2],
        request_id: item[9],
        env: item[10],
        wakeup: item[11],
        wakeup_asr_text: item[12],
        app_id:item[13],
        vossdk_ver:item[14],
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

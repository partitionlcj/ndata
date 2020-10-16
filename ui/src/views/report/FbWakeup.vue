<template>
  <div>
    <InfoModal v-model="showModal" :data="sysResult"></InfoModal>
    <Row class="margin-bottom-20" :gutter="16">
      <Col span="4" class="margin-bottom-10">
        <DatePicker :value="filter.date" format="yyyy-MM-dd" type="daterange" placement="bottom-end" placeholder="Select date" @on-change="dateChange" style="width: 100%"></DatePicker>
      </Col>
      <template>
        <Col span="3" class="margin-bottom-10">
          <Input placeholder="vehicle_id" v-model="filter.vid" @on-enter="pageChange(1)"></Input>
        </Col>
        <Col span="2" class="margin-bottom-10">
        <Input placeholder="env" v-model="filter.env" @on-enter="pageChange(1)"></Input>
        </Col>
      </template>
      <Col span="2" class="margin-bottom-10">
      <Input placeholder="app_id" v-model="filter.app_id" @on-enter="pageChange(1)"></Input>
      </Col>
      <Col span="4" class="margin-bottom-10">
        <Input placeholder="request_id" v-model="filter.rid" @on-enter="pageChange(1)"></Input>
      </Col>
      <Col span="2" class="margin-bottom-10">
        <Input placeholder="platform_type" v-model="filter.platform_type" @on-enter="pageChange(1)"></Input>
      </Col>
      <Col span="4" class="margin-bottom-10">
        <Input placeholder="vossdk version" v-model="filter.ver" @on-enter="pageChange(1)"></Input>
      </Col>
      <Col span="3" class="margin-bottom-10">
        <Input placeholder="asr text" v-model="filter.asr_text" @on-enter="pageChange(1)"></Input>
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
        rid: '',
        env: '',
        vid: '',
        app_id: '',
        ver: '',
        asr_text: '',
        platform_type: ''
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
        title: 'request_id',
        minWidth: 340,
        maxWidth: 340,
        key: 'request_id',
      });
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
          title: '唤醒词',
          key: 'asr_text',
          width: 150
        }
      )
      columns.push( {
          title: '平台类型',
          key: 'platform_type',
          width: 150
        }
      )
      columns.push( {
          title: 'env',
          key: 'env',
          minWidth: 150,
          maxWidth: 150,
        })
      
      columns.push({
        title: 'app_id',
        key: 'app_id',
        minWidth: 110,
        maxWidth: 110
      });

      columns.push( {
          title: 'ver',
          key: 'ver',
          minWidth: 410,
          maxWidth: 410,
        }
      )

      columns.push({
          title: '音频',
          width: 70,
          render: (h, params) => {
            return h('AisAudio', {
              props: {
                url: `/api/audio/wakeup_wav?requestId=${params.row.request_id}`,
                size: 14
              }
            })
          }
        })
      columns.push({
        title: 'date',
        key: 'date',
        minWidth: 190,
        maxWidth: 500
      });
      
      return columns;
    }
  },
  beforeMount() {
    this.reportName = 'wakeup';
    let now = util.getTodayDate();
    this.filter.date = [now, now];
    this.getWakeup();
  },
  methods: {
    async getWakeup() {
      this.currentViewRow = -1; // 只要重新获取数据就重置当前查看的行
      
      let begin_date = undefined;
      let end_date = undefined;
      let { rid, env, vid, app_id, ver, asr_text, platform_type } = this.filter;

      if (this.filter.date.length > 0) {
        begin_date = this.filter.date[0] ? `${this.filter.date[0]} 00:00:00` : undefined;
        end_date = this.filter.date[1] ? `${this.filter.date[1]} 23:59:59` : undefined;
      }
      this.loading = true;
      let response;
      response = await api.getWakeupData(new Date(begin_date).getTime(), new Date(end_date).getTime(), app_id.toLowerCase().trim(), rid.toLowerCase().trim(), 
                  vid.toLowerCase().trim(), ver.toLowerCase().trim(), env.toLowerCase().trim(),asr_text.toLowerCase().trim(),platform_type.toLowerCase().trim(), this.pagination.page, this.pagination.pageSize);
      
      this.loading = false;
      let data = response.data;
      this.data = data.data.map((item) => ({
        asr_text: item[0],
        vid: item[2],
        request_id: item[3],
        date: new Date(item[1]).toLocaleString("zh-CN"),
        app_id: item[5],
        platform_type: item[7],
        ver: item[6],
        env: item[4]
      }));
      this.pagination.total = data.total;
    },
    pageChange(page) {
      document.querySelector('.content').scrollTop = 0; //翻页回到页面顶部
      this.pagination.page = page;
      this.getWakeup();
    },
    dateChange(val) {
      this.filter.date = val;
      this.pagination.page = 1;
    },
    exportCsv() {
      this.getWakeup(true);
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

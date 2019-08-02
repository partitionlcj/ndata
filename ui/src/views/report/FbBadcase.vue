<template>
  <div class="badcase-page">
    <InfoModal :data="sysResult" v-model="showModal" :sessionId="currentSessionId" @refresh="loadBadcase"></InfoModal>
    <Card>
      <p slot="title">
        {{$route.query.label}}-badcase
      </p>
      <Table :columns="columns" :data="data" :loading="loading" stripe></Table>
      <div class="page">
        <Page :current="pagination.page" :total="pagination.total" :page-size="pagination.pageSize" show-total @on-change="pageChange"></Page>
      </div>
    </Card>
  </div>
</template>
<script>
import api from '../../api/index';
import InfoModal from '../../components/Modal/InfoModal';
import util from '../../util';
export default {
  components: {
    InfoModal
  },
  data() {
    return {
      loading: false,
      showModal: false,
      data: [],
      sysResult: [],
      currentSessionId: '',
      pagination: {
        total: 0,
        pageSize: 10,
        page: 1
      },
      columns: [{
        title: '上下文',
        render: (h, params) => {
          return h('div', {
            style: {
              padding: '20px'
            }
          }, params.row.context && params.row.context.map(item => {
            let currentSession = item.session_id === params.row.session_id;
            return h('div', {
              class: [currentSession ? 'current-session' : '']
            }, [h('div', {
              style: {
                fontWeight: currentSession ? 'bold' : ''
              }
            }, item.session_id), h('Card', {
              props: {
                disHover: true
              },
              class: ['margin-bottom-10', currentSession ? 'current-session' : '']
            }, item.queries.map((query, index) => {
              let tts = JSON.parse(query.finalTts).map(item => item.content).join('|');
              let viewText = JSON.parse(query.finalViewText).map(item => item.content).join('|');
              let time = util.getTextFromTime(query.ts);
              return h('div', [h('div', [h('label', 'query:' + query.query),
                time && h('Tag', { props: { color: 'warning' } }, time),
                h('AisAudio', {
                  props: {
                    url: `/api/audio/download_wav?requestId=${query.requestId}`
                  }
                })
              ]), h('div', 'TTS:' + tts), h('div', 'ViewText:' + viewText), index === item.queries.length - 1 ? null : h('Divider')]);
            }))])
          }))
        }
      }, {
        title: '操作',
        width: 80,
        align: 'center',
        render: (h, params) => {
          return h('Button', {
            props: {
              type: 'primary',
              size: 'small',
              disabled: params.row.submit_raphael === 'true'
            },
            on: {
              click: () => {
                this.loadInfo(params.row.session_id);
              }
            }
          }, '查看')
        },
      }]
    }
  },
  watch: {
    showModal(newVal) {
      if (!newVal) {
        this.sysResult = [];
      }
    }
  },
  beforeMount() {
    this.loadBadcase();
  },
  methods: {
    async loadBadcase() {
      this.loading = true;
      let key = this.$route.query.key;
      let response = await api.readSsdb(key, this.pagination.page, this.pagination.pageSize);
      const data = response.data;
      this.pagination.total = data.total;
      this.data = data.data;
      this.loading = false;
    },
    async loadInfo(sessionId, index) {
      this.currentSessionId = sessionId;
      let response = await api.getRequestInfo(sessionId);
      if (response.state === 'success') {
        this.sysResult = response.data;
        this.showModal = true;
      }
    },
    pageChange(page) {
      document.querySelector('.content').scrollTop = 0; //翻页回到页面顶部
      this.pagination.page = page;
      this.loadBadcase();
    }
  }
}

</script>
<style scoped>
.badcase-page>>>.current-session {
  background-color: #2db7f5 !important;
}

</style>

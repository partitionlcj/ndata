<template>
  <div>
    <div>
    <Label>起始时间</Label>
    <DatePicker type="date" placeholder="Select date" style="width: 200px" :value="startDate" @on-change="dateChange"></DatePicker>
    <TimePicker format="HH:mm" placeholder="Select time" style="width: 112px" :value="startTime" @on-change="timeChange"></TimePicker>
    <Label>小时数</Label>
    <InputNumber :max="1000" :min="1" v-model="hourCount"></InputNumber>
    设备VehicleId
    <AutoComplete
        v-model="vid"
        :data="vids"
        placeholder="Vehicle ID"
        style="width:200px">
    </AutoComplete>
    <Button type="primary" @click="requestLog()">发送日志回传请求</Button>
    </div>
    <br>
    <div>
      <AutoComplete
        v-model="searchVid"
        :data="vids"
        placeholder="Vehicle ID"
        style="width:200px">
    </AutoComplete>
    <Button type="primary" @click="searchLog()">查看日志</Button>
        <Table :columns="columns" :data="logs" :loading="loading" class="detail-table"></Table>
    </div>
  </div>
</template>

<script>
import api from '../../api';

export default {
  data () {
    return {
      startDate: '',
      startTime: '',
      hourCount: 0,
      vid:'',
      searchVid:'',
      vids:[],
      loading: false,
      columns: [{
        title: '日志回传时间',
        key: 'uploadedAt'
      },
      {
        title: '日志生成时间',
        key: 'createdAt'
      },
      {
        title: '日志文件',
        key: 'files',
        render: (h, params) => {
          return h('ul', params.row.files.map(f => h('li', [h('a',{on: {
                'click': ()=>{
                    this.handleLink(f.link)
                }
          }},f.name)])));
        }
      }
      ],
      logs: [
      ]
    }
  },
  mounted () {
    this.getVids()
  },
  methods: {
    async getVids(){
      let response = await api.getVehVids()
      this.vids = response.data
    },
    async requestLog () {
      let response
      this.loading = true
      response = await api.requestVehLog(this.vid, this.startDate + ' ' + this.startTime, this.hourCount)
      this.loading = false;
      if( response.state == 'success' ){
        this.$Message.success('回传日志请求推送成功！');
      }
      else{
        this.$Message.error('回传日志请求推送失败！');
      }

    },
    async searchLog () {
      let response = await api.searchVehLog(this.searchVid)
      this.logs = response.data
      console.log(response)
    },
    dateChange (date) {
      this.startDate = date
    },
    timeChange (time) {
      this.startTime = time
    },
    handleLink (link) {
      window.open(link)
    }
  }
}
</script>
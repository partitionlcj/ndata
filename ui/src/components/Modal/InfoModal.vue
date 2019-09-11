<template>
  <div>
    <Modal title="Output" :value="value" :closable="false" @on-visible-change="visibleChange" width="600px">
      <div>
        <pre>{{ json_txt }}</pre>
      </div>
    </Modal>
  </div>
</template>
<script>
import { PROBLEM_TYPE } from '../../config/const';
import api from '../../api/fb';
export default {
  props: {
    value: Boolean,
    data: {
      type: String
    }
  },
  data() {
    return {
      problemTypes: PROBLEM_TYPE,
      fbInfo: {
        reason: [],
        comment: ''
      }
    }
  },
  computed: {
    json_txt() { 
      if( this.data != null && this.data.length > 2){
        return JSON.stringify(JSON.parse(this.data), null, 4)
      }
      else{ 
        return '';
      }
    }
  },
  methods: {
    visibleChange(status) {
      this.$emit('input', status);
    },
    async submitToFb() {
      if (this.fbInfo.comment === '') {
        this.$Message.error('请填写备注!');
        return;
      }

      let response = await api.submitToFb({ session_id: this.sessionId, reason: this.fbInfo.reason.join(','), comment: this.fbInfo.comment });
      if (response.state === 'success') {
        this.$Message.success('提交成功');
        api.addComment(this.sessionId, this.fbInfo.comment);
        this.$emit('refresh');
        this.$emit('input', false);
      } else {
        this.$Message.error(response.data);
      }
    }
  }
}

</script>
<style scoped>
.tts {
  padding-left: 20px;
}

.query {
  color: blue;
  font-weight: bold;
}

</style>

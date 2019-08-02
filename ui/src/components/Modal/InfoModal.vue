<template>
  <div>
    <Modal :value="value" title="viewText & TTS" :closable="false" @on-visible-change="visibleChange">
      <div v-for="(i, index) in data" :key="'query'+index" class="margin-bottom-20">
        <p class="query">【{{i.query}}】</p>
        <div class="label-text">TTS</div>
        <ul class="tts margin-bottom-20">
          <li v-for="(item, index) in i.final_tts" :key="'tts'+index">{{item}}</li>
        </ul>
        <span class="label-text">ViewText</span>
        <ul class="tts">
          <li v-for="(item, index) in i.final_view_text" :key="'view'+index">{{item}}</li>
        </ul>
      </div>
      <div v-if="showSubmitToFb">
        <fieldset style="padding: 10px">
          <legend>反馈信息</legend>
          <CheckboxGroup v-model="fbInfo.reason" class="margin-bottom-20">
            <Checkbox v-for="type in problemTypes" :key="type" :label="type"></Checkbox>
          </CheckboxGroup>
          <Input type="textarea" placeholder="请输入你的备注" v-model.trim="fbInfo.comment"></Input>
        </fieldset>
      </div>
      <div slot="footer">
        <Button type="error" long @click="submitToFb">提交到反馈系统</Button>
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
      type: Array,
      default: () => []
    },
    sessionId: String,
    showSubmitToFb: {
      type: Boolean,
      default: true
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
  watch: {
    value() {
      this.fbInfo.reason = [];
      this.fbInfo.comment = '';
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

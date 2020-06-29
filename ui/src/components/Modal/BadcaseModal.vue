<template>
  <div>
    <Modal title="提交Badcase" @on-ok="addBadcase" :value="value" :closable="false" @on-visible-change="visibleChange" width="600px">
      <Form :label-width="80" :model="p">
      <FormItem label="request_id">
        <Input v-model="p.request_id" disabled></Input>
      </FormItem>
      <FormItem label="asr识别文本">
        <Input v-model="p.asr_text" readonly></Input>
      </FormItem>
      <FormItem label="正确文本">
        <Input placeholder="请输入正确文本" v-model="p.text"></Input>
      </FormItem>
      <FormItem label="类型">
        <Select v-model="p.type">
          <Option v-for="t in types" :value="t.id" :key="t.id">{{ t.label }}</Option>
        </Select>
      </FormItem>
      <FormItem label="权重">
        <InputNumber :min="1" :max="100" v-model="p.weight" placeholder="请输入权重"></InputNumber>
      </FormItem>
      </Form>
    </Modal>
  </div>
</template>
<script>
import api from '../../api/fb';

export default {
  props: {
    value: Boolean,
    data:  Object
  },
  data() {
    return {
      p:{
        request_id: '',
        asr_text: '',
        text: '',
        type: 0,
        weight: 1
      },
      types: [
        {id: 1001, label:'噪音'},
        {id: 1002, label:'口音'},
        {id: 1003, label:'外语'},
        {id: 1004, label:'语速快'},
        {id: 1005, label:'语速慢'},
        {id: 1006, label:'其他'},
        {id: 2001, label:'poi纠错'},
        {id: 2002, label:'新发音'},
        {id: 2003, label:'新词'},
        {id: 9999, label:'其他'}
      ]
    }
  },
  watch: {
    data(newVal){
      this.p.request_id = newVal.request_id
      this.p.asr_text = newVal.query
      this.p.weight = 1
      this.p.text = ''
      this.p.type = 0
    }
  },
  computed: {
    
  },
  methods: {
    visibleChange(status) {
      this.$emit('input', status);
    },
    async addBadcase() {
      if (this.p.text === '') {
        this.$Message.error('请填写正确文本!');
        return false;
      }
      if (this.p.type === 0 ) {
        this.$Message.error('请选择问题类型!');
        return false;
      }

      let response = await api.submitBadcase(this.p);
      if (response.state === 'success') {
        //this.$Message.success('提交成功');
        this.$emit('updateBadcase');
        //this.$emit('input', false);
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

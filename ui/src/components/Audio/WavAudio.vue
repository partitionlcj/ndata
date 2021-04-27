<template>
  <div class="display-inline-block">
      <Icon :type="icon" @click.native="controlAudio" :size="size" class="play" />
      <Icon type="ios-download" @click.native="downloadAudio" :size="size" class="download" />
  </div>
</template>
<script>
export default {
    name: 'WavAudio',
    props: {
        url: {
            type: String,
            required: true
        },
        size: {
            type: Number,
            default: 28
        }
    },
    data() {
        return {
            icon: 'ios-play',
            audioObj: null
        }
    },
    methods: {
        async controlAudio() {
            // 如果当前音频为空,则发送请求拿到音频数据
            
                this.$Loading.start({ color: 'yellow' });
                let response = await fetch(this.url);
                // let type = response.headers.get("content-type");
                // // 判断拿到的数据的数据类型
                // if (this.$aisUtil.hasStr(type, 'text')) {
                //     this.$Loading.error();
                //     this.$Message.error({
                //         duration: 5,
                //         content: await response.text(),
                //     });
                //     return;
                // } else {
                    this.$Loading.finish();
                    this.audioObj = new Audio(URL.createObjectURL(await response.blob()));
                    this.audioObj.onended = () => {
                        this.icon = 'ios-play';
                    }
                    this.audioObj.onerror = () => {
                        this.audioObj = null;
                        this.$Message.error('音频内容有问题!请联系管理员');
                        this.$Loading.error();
                        this.icon = 'ios-play';
                    }
                // }
            
            // 如果音频不为空就开始播放
            if (this.icon === 'ios-play') {
                this.icon = 'ios-pause';
                this.audioObj.play();
            } else if (this.icon === 'ios-pause') {
                this.icon = 'ios-play';
                this.audioObj.pause();
            }
        },
        downloadURI(uri, name) {
            const link = document.createElement("a");
            link.download = name;
            link.href = uri;
            link.click();
        },
        downloadAudio() {
          this.downloadURI(this.url);
        }
    }
}
</script>
<style scoped>
.play,
.download {
    cursor: pointer;
}
</style>
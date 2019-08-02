<template>
  <div class="date-picker">
    <ButtonGroup class="margin-bottom-10">
      <Button type="primary" icon="ios-skip-backward" @click="year--"></Button>
      <Button size="large">{{year}}</Button>
      <Button type="primary" icon="ios-skip-forward" @click="year++"></Button>
    </ButtonGroup>
    <br />
    <!-- <div class="margin-bottom-10 month-text">Month</div> -->
    <ButtonGroup class="margin-bottom-10">
      <div v-for="(row, index) in months">
        <Button v-for="m in row" :key="m" :type="m == month ? 'primary':'default'" @click="month=m" class="width-60" :style="{'border-top': index > 0 ?'none':''}">{{m + '月'}}</Button>
      </div>
    </ButtonGroup>
    <br />
    <!-- <div class="margin-bottom-10 day-text">Day</div> -->
    <template v-if="showDayPanel">
      <ButtonGroup class="margin-bottom-10">
        <Button v-for="week in weeks" :key="week" type="text" class="width-60">{{week}}</Button>
      </ButtonGroup>
      <br />
      <ButtonGroup>
        <div v-for="(row, index) in days">
          <Button v-for="d in row" :key="d.day" :disabled="d.disabled" :type="d.day== day ? 'primary':'default'" @click="day=d.day" class="width-60" :style="{'border-top': index > 0 ?'none':''}">{{d.day}}
          </Button>
        </div>
      </ButtonGroup>
    </template>
  </div>
</template>
<script>
const ROW_COUNT = 7;
export default {
  props: {
    value: String,
    type: String
  },
  data() {
    return {
      year: '',
      month: '',
      day: '',
      weeks: ['一', '二', '三', '四', '五', '六', '日']
    }
  },
  beforeMount() {
    this.setInitDate();
  },
  computed: {
    showDayPanel() {
      return this.type === 'daily' || this.type === 'weekly';
    },
    months() {
      let res = this.calRows(12, ROW_COUNT);
      return res;
    },
    days() {
      return this.getDaysPanel(this.year, this.month, 0);
    }
  },
  watch: {
    year() {
      this.emitFunc()
    },
    month() {
      this.emitFunc()
    },
    day() {
      this.emitFunc()
    },
    value() {
      this.setInitDate();
    }
  },
  methods: {
    setInitDate() {
      let temp = this.value.split('-');
      this.year = +temp[0];
      this.month = +temp[1];
      this.day = +temp[2] || '';
    },
    calRows(num, count, type) {
      let n = Math.floor(num / count);
      let res = [];
      for (let i = 0; i < n; i++) {
        res.push([i * count + 1, i * count + 2, i * count + 3, i * count + 4, i * count + 5, i * count + 6, i * count + 7]);
      }
      let modes = [];
      for (let i = n * count + 1; i < 12 + 1; i++) {
        modes.push(i);
      }
      res.push(modes);
      return res;
    },
    emitFunc() {
      if (this.type === 'daily' || this.type === 'weekly') {
        this.$emit('input', this.year + '-' + this.month + '-' + this.day);
      } else if (this.type === 'monthly') {
        this.$emit('input', this.year + '-' + this.month);
      }
    },
    getDaysPanel(year, month, day) {
      // 返回这个月一共有几天
      let days = new Date(year, month, day).getDate();
      // 返回这个月的第一天
      let firstDay = new Date(year, month - 1, 1);
      let res = [];
      let d = [];
      for (let i = 1; i < days + 1; i++) {
        let week = this.getWeekDay(year + '-' + month + '-' + i);
        // 如果第一天不是周一, 那么就用上一个月的最后几天来补全
        if (i === 1 && week > 0) {
          let j = 0;
          while (j < week) {
            let temp = new Date(firstDay.getTime());
            temp.setDate(firstDay.getDate() - (week - j));
            d[j] = {
              day: temp.getDate(),
              disabled: true
            };
            j++;
          }
        }

        // 如果当前行还不够七天,则继续在当前行加入日期; 否则另起一行
        if (d.length < 7) {
          d[week] = {
            day: i,
            disabled: false
          };
        } else {
          res.push(d);
          d = [];
          d[week] = {
            day: i,
            disabled: false
          };
        }
      }
      res.push(d);
      return res;
    },
    getWeekDay(dateStr) {
      // 获取日期为dateStr在一周中的天数, 并返回其在数组中的下标
      // 注意周日为0, 但是周日显示在最后一行
      let week = new Date(dateStr).getDay()
      if (week === 0) {
        return 6;
      }
      return week - 1;
    }
  }
}

</script>
<style scoped>
.date-picker {
  width: 500px;
}

.width-60 {
  width: 60px;
}

</style>

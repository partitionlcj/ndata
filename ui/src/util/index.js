import moment from 'moment';

let getTableHeader = function(data) {
  // 获取表头的信息,传入的数据可以是数组也可以是对象
  let temp;
  if (Array.isArray(data)) {
    temp = data[0];
  } else {
    temp = data;
  }
  let column = [];
  for (let key in temp) {
    if (temp.hasOwnProperty(key)) {
      column.push({
        title: key,
        key: key,
        align: 'center'
      })
    }
  }
  return column;
}

let objToArr = function(data, name, value) {
  let res = [];
  for (let key in data) {
    if (data.hasOwnProperty(key)) {
      res.push({
        [name]: key,
        [value]: data[key]
      })
    }
  }
  return res;
}

let getPieContentFromObj = function(data, limit) {
  let temp = objToArr(data, 'name', 'value');
  if (limit === undefined) {
    return {
      legend: Object.keys(data),
      data: temp
    }
  } else {
    let res = [];
    let legend = [];
    temp.sort((a, b) => b.value - a.value);
    temp.forEach((item, index) => {
      if (index < limit) {
        legend.push(item.name);
      }
    });
    return {
      legend: legend,
      data: temp.slice(0, limit)
    }
  }
}

let getLabelTextFromObj = function(obj) {
  let labelText = '';
  for (let key in obj) {
    if (obj.hasOwnProperty(key)) {
      labelText += `${key.toUpperCase()}:${obj[key]} &nbsp;&nbsp; `
    }
  }
  return labelText;
}

let genNAVICALLTableHeader = function(obj, goToBadCase, dateType, type) {
  // 生成导航意图和电话意图的报表表头
  let header = [{
    title: '',
    align: 'center',
    key: 'intent'
  }];
  for (let key in obj) {
    if (obj.hasOwnProperty(key)) {
      header.push({
        title: key,
        align: 'center',
        render: (h, params) => {
          let temp = params.row[obj[key]];
          let badcase = null;
          if (dateType === 'daily' && temp && temp.badcase > 0) {
            badcase = h('Button', {
              props: { size: 'small', type: 'error', disabled: params.row.intent === '总计' },
              on: {
                click: () => {
                  let badcaseKey = type === 'nav' ? `${params.row.intent}.${obj[key]}` : `${params.row.intent}.${obj[key]-1}`
                  goToBadCase(`${badcaseKey}`, `${params.row.intent}-${key}`);
                }
              },
              class: {
                'display-block': true
              },
              style: {
                'margin': '10px auto'
              }
            }, temp.badcase)
          }
          return h('div', [temp && h('Button', {
              props: { size: 'small' },
              class: {
                'display-block': true
              },
              style: {
                'margin': '10px auto'
              }
            }, temp.value),
            temp && temp.rate && h('Button', {
              props: { size: 'small', type: 'success' },
              class: {
                'display-block': true
              },
              style: {
                'margin': '10px auto'
              }
            }, temp.rate), badcase
          ]);
        }
      })
    }
  }
  return header;
}

let oneOf = function(value, arr) {
  return arr.includes(value);
}

let getTodayDate = function() {
  return moment().format('YYYY-MM-DD');
}

let getYesterdayDate = function() {
  return moment().subtract(1, 'days').format('YYYY-MM-DD');
}

let getCurrentMonth = function() {
  return moment().format('YYYY-M');
}

let getTextFromTime = function(time) {
  // 传入的参数是秒级的时间
  // 输出显示大概的距离时间文本
  if (time === 0) return '';
  let type = '';
  if (time > 0) {
    type = '后';
  } else if (time < 0) {
    type = '前';
  }
  time = Math.abs(time);
  if (time < 60) {
    return time + 's' + type;
  } else {
    let min = Math.floor(time / 60);
    if (min < 60) {
      return min + 'min' + type;
    } else {
      let hour = Math.floor(min / 60);
      if (hour < 24) {
        return hour + 'hr' + type;
      } else {
        let day = Math.floor(hour / 24);
        return day + 'day' + type;
      }
    }
  }
}

let getDaysArrayByMonth = function(month) {
  let daysInMonth = moment(`${month}01`).daysInMonth();
  let arrDays = [];
  while (daysInMonth) {
    let current = moment(`${month}01`).date(daysInMonth).format('YYYY-MM-DD');
    arrDays.unshift(current);
    daysInMonth--;
  }

  return arrDays;
}

// 根据秒数来生成更易读的字符串
let generateReadableTime = function(time) {
  let arr = [];
  if (time < 60) {
    return time + '秒';
  } else {
    let second = time % 60;
    second && arr.unshift(time % 60 + '秒');
    let min = Math.floor(time / 60);
    if (min < 60) {
      arr.unshift(min + '分钟');
      return arr.join(' ');
    } else {
      let hr = Math.floor(min / 60);
      min = min % 60;
      min && arr.unshift(min + '分钟');
      if (hr < 24) {
        arr.unshift(hr + '小时');
        return arr.join(' ');
      } else {
        let day = Math.floor(hr / 24);
        hr = hr % 24;
        hr && arr.unshift(hr + '小时');
        day && arr.unshift(day + '天');
      }
    }
  }
  return arr.join(' ');
}

const API = {
  getTableHeader,
  objToArr,
  getPieContentFromObj,
  getLabelTextFromObj,
  genNAVICALLTableHeader,
  getTodayDate,
  getYesterdayDate,
  getCurrentMonth,
  oneOf,
  getTextFromTime,
  getDaysArrayByMonth,
  generateReadableTime
}


export default API;

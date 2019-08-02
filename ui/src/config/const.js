export const DAILY_NLU_TYPE = {
  '正常': 0,
  '正常走兜底': 1,
  'NLU部分理解走兜底': 2,
  'NLU完全不理解': 3
}

export const NAVI_FUNNEL_TYPE = {
  '有导航意图': 1,
  '成功反馈结果': 2,
  '成功确定了POI': 3,
  '开始导航': 4
}

export const CALL_FUNNEL_TYPE = {
  '有电话意图': 1,
  '成功确定号码': 2,
  '执行拨打': 3
}

export const PROBLEM_TYPE = ['tts', 'nlu', 'bug', 'search', 'asr', 'design', 'chat', 'front end', 'nomi没听懂', '进入task', '进入其他topic', '反向回复', '偏离语境'];

export const NAVI_INTENT = ['navi_poi', 'poi_lookup', 'navi_favorite', 'navi_history_go', 'navi_history_lookup', 'navi_favorite_list', 'navi_favorite_list_go'];

export const CALL_INTENT = ['call_with_name', 'call_with_org', 'call_with_num', 'call_history'];

export const PERFORMANCE_LABEL = [{
    "name": "唤醒事件在Nomi App与语音服务之间的本地通讯时间",
    "key": "wakeup_interface",
    "color": "#7b9ce1",
    "comments": "从SpeechService发出唤醒事件的时刻到Nomi接收到唤醒事件的时刻 "
  },
  {
    "name": "Nomi App界面启动时间",
    "key": "nomi_launch",
    "color": "#bd6d6c",
    "comments": "从Nomi接收到唤醒事件的时刻到Nomi界面完成启动的时刻  "
  },
  {
    "name": "Nomi App界面启动到向DS发出唤醒通知",
    "key": "block1",
    "color": "#77ACA2",
    "comments": "从Nomi界面完成启动的时刻到Nomi模块开始向DS发唤醒通知"
  },
  {
    "name": "DS接收NomiApp发出的唤醒通知 成功",
    "key": "user_awaken",
    "color": "#e0bc78",
    "comments": "从Nomi模块向DS发出唤醒通知到DS成功接收到NomiApp发出的通知"
  },
  {
    "name": "DS接收到Nomi App发出的唤醒通知到用户开始语音输入",
    "key": "block2",
    "color": "#dc77dc",
    "comments": "从Nomi模块完成唤醒的时刻到Nomi模块调用SpeechService接口开启识别"
  },
  {
    "name": "开启识别到用户开始说话的时间差",
    "key": "Speech_Recognize",
    "color": "cyan",
    "env": "stag",
    "comments": "Nomi模块调用SpeechService接口开启识别到SpeechService模块接收到用户开始语音输入的时刻"
  },
  {
    "name": "用户开始语音输入的事件在NomiApp和语音服务之间的本地通讯时间",
    "key": "speech_start_interval",
    "color": "#72b362",
    "comments": "从SpeechService模块接收到用户开始语音输入的时刻到Nomi模块得知用户已开始语音输入的时刻"
  },
  {
    "name": "用户说话",
    "key": "block3",
    "color": "lightblue",
    "comments": "从Nomi模块得知用户已开始语音输入的时刻到SpeechService模块得知到用户语音输入已结束的时刻"
  },
  {
    "name": "用户结束语音输入的事件在Nomi App与语音服务之间的本地通讯时间",
    "key": "speech_end_interval",
    "color": "#75d874",
    "comments": "SpeechService模块得知到用户语音输入已结束的时刻到Nomi模块得知用户已结束语音输入的时刻"
  },
  {
    "name": "语音输入结束到完成asr识别",
    "key": "block4",
    "color": "pink",
    "comments": "从Nomi模块得知用户已结束语音输入的时刻到SpeechService模块得到ASR识别结果的时刻"
  },
  {
    "name": "Asr识别结果在Nomi App与语音服务之间的本地通讯时间",
    "key": "asr_event",
    "color": "#508a88",
    "comments": "从SpeechService模块得到ASR识别结果的时刻到Nomi模块接收到Asr识别结果的时刻"
  },
  {
    "name": "语音服务上报的识别耗时",
    "key": "Test asr time",
    "color": "#C65D46",
    "env": "stag",
    "comments": "直接读取这个埋点中的tracking_event_time_interval字段值"
  },
  {
    "name": "TTSPlayer 的start事件在本地通讯的时间",
    "key": "tts_start_to_onstart",
    "color": "#5ADBFF",
    "env": "stag",
    "comments": "直接读取这个埋点中的tracking_event_timestamp字段值"
  },
  {
    "name": "TTSPlayer合成时长",
    "key": "tts_start_to_onsynend",
    "color": "#584850",
    "env": "stag",
    "comments": "直接读取这个埋点中的tracking_event_timestamp字段值"
  },
  {
    "name": "离线nlu",
    "key": "local_nlu",
    "color": "#b7ba6b",
    "comments": "从Nomi模块开始离线nlu的时刻到Nomi模块完成离线nlu的时刻"
  },
  {
    "name": "在线nlu",
    "key": "cloud_nlu",
    "color": "#f15b6c",
    "comments": "从Nomi模块开始在线nlu的时刻到Nomi模块完成在线nlu的时刻"
  }
]

export const SUMMARY_PERFORMANCE_LABEL = [{
    "name": "唤醒时长",
    "key": "wakeup",
    "color": "purple",
    "comments": "从SpeechService发出唤醒事件的时刻到Nomi界面完成启动的时刻"
  },
  {
    "name": "识别时长",
    "key": "asr_cost",
    "color": "yellow",
    "comments": "从SpeechService模块得知到用户语音输入已结束的时刻到Nomi模块接收到Asr事件的时刻"
  },
  {
    "name": "理解时长",
    "key": "recognize_nlu",
    "color": "orange",
    "comments": "如果在线nlu在2.5秒内有结果，则使用在线nlu时间，如果在线nlu时间超过2.5秒，则看离线和在线nlu谁快就用谁"
  }
]

import base from './root';
const ASSIGN = {
  requestInfo: '/api/sp/wa/com/page_query',
}

const COMMON = {
  config: '/api/config/multiget',
  configSingleGet: '/api/config/get',
  meta: '/api/common/meta',
  report: '/api/common/report',
  getUserInfo: '/api/common/user_role',
  query: '/api/common/query',
  readSsdb: '/api/common/read_page_ssdb',
  getComments: '/api/sp/com/batch_comment'
};

export default {
  getUserInfo() {
    return base('get', COMMON.getUserInfo);
  },
  getMeta() {
    return base('get', COMMON.meta);
  },
  config(keys) {
    return base('get', COMMON.config, {
      params: {
        keys
      }
    });
  },
  getCommonReport(reportName, domain) {
    return base('post', COMMON.report, {
      report_name: reportName,
      domain
    });
  },
  getDomainIntentQueryDetail(domain, intent, begin_date, end_date, query, pageIndex, pageSize) {
    // intent报表中获取每个intent下面具体的query信息
    return base('post', COMMON.report, {
      report_name: "实车用户明细_ch",
      pageIndex,
      pageSize,
      domain,
      intent,
      begin_date,
      end_date,
      query
    });
  },
  getFactData(begin_date, end_date, sessionId, query, domain, vid, operation, intent, pageIndex, pageSize) {
    return base('post', COMMON.report, {
      report_name: "实车用户明细_no_intent_ch",
      pageIndex,
      pageSize,
      begin_date,
      end_date,
      query: `%${query}%`,
      session_id: `%${sessionId}%`,
      domain: `%${domain}%`,
      vid: `%${vid}%`,
      intents: `%${intent}%`,
      operations: operation.toUpperCase() === 'NULL' ? '' : `%${operation}%`
    });
  },
  getDebugData(begin_date, end_date, requestId, sessionId, query, domain, vid, operation, intent, env, wakeup_asr_text, pageIndex, pageSize) {
    return base('post', COMMON.report, {
      report_name: "debug1",
      pageIndex,
      pageSize,
      begin_date,
      end_date,
      request_id: `%${requestId}%`,
      query: `%${query}%`,
      session_id: `%${sessionId}%`,
      domain: `%${domain}%`,
      vid: `%${vid}%`,
      intents: `%${intent}%`,
      env: `%${env}%`,
      wakeup_asr_text: `%${wakeup_asr_text}%`,
      operations: operation.toUpperCase() === 'NULL' ? '' : `%${operation}%`
    });
  },
  getVosDebugData(begin_date, end_date, requestId, sessionId, query, vid, env, pageIndex, pageSize) {
    return base('post', COMMON.report, {
      report_name: "vos_debug_query",
      pageIndex,
      pageSize,
      begin_date,
      end_date,
      request_id: `%${requestId}%`,
      query: `%${query}%`,
      session_id: `%${sessionId}%`,
      vid: `%${vid}%`,
      env: `%${env}%`
    });
  },
  getRequestInfo(requestId) {
    return base('get', '/api/debug/output?rid='+requestId)
  },
  searchVehLog(vid) {
    return base('get', '/api/vehlog/searchLog?vid='+vid)
  },
  requestVehLog(vid,startTs,hourCount, appId, env){
    return base('post','/api/vehlog/requestLog',{
      vid,
      startTs,
      hourCount,
      appId,
      env
    })
  },
  getVehVids(){
    return base('get','/api/vehlog/vids')
  },
  readSsdb(key, page, pageSize) {
    return base('post', COMMON.readSsdb, {
      key,
      page_index: page,
      page_size: pageSize
    });
  },
  getComments(keys) {
    //return base('post', COMMON.getComments, keys.map(key => `sariel_${key}_to_feedback_comment`));
  }
};

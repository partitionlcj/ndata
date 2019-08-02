import base from './root';

const REAL = {
  query: '/api/common/report',
  submitToFb: '/api/fb/report_user_feedback'
}

export default {
  getVid(vin) {
    let params = { report_name: "get_vid_by_vin", pageIndex: 1, pageSize: 1, vin }
    return base('post', REAL.query, params);
  },
  submitToFb(param) {
    return base('post', REAL.submitToFb, param);
  }
}

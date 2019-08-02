import base from './root';

const DAILY = {
  query: '/api/ssdb/get'
}

export default {
  getData(keys) {
    return base('get', DAILY.query, {
      params: {
        keys
      }
    });
  }
}

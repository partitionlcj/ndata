import base from './root';
import Moment from 'moment';
import { extendMoment } from 'moment-range';

const moment = extendMoment(Moment);

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

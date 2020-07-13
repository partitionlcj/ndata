import base from './root';

export default {
  submitBadcase(param) {
    return base('post', '/api/common/badcase', param, true);
  },
  submitLowQualityWav(param,type) {
    param['type'] = type
    return base('post', '/api/common/lowQuality', param, true);
  }
}

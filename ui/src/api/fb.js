import base from './root';

export default {
  submitBadcase(param) {
    return base('post', '/api/common/badcase', param, true);
  }
}

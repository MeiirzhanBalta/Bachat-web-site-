import ApiService from './ApiService';

export default {
  getUsers() {
    return ApiService.get('/users');
  },
  addUser(userData) {
    return ApiService.post('/users', userData);
  }
};
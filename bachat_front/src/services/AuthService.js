import ApiService from '../services/ApiService';
import store from '@/store';

const AuthService = {
  login(credentials) {
    return ApiService.post('/login', credentials)
      .then(response => {
        store.dispatch('login'); 
        return Promise.resolve(response);
      })
      .catch(error => {
        console.error("Login Error:", error);
        return Promise.reject(error);
      });
  },
  logout() {
    return new Promise((resolve) => {
      store.dispatch('logout');
      resolve();
    });
  },
  loadUserInfo() {
    return ApiService.loadUserInfo();
  }
};

export default AuthService;


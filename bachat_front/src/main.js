import { createApp } from 'vue';
import App from './App.vue';
import router from './router/router';
import store from './store';
import './assets/css/style.css';
import ApiService from './services/ApiService';

ApiService.init(); 

createApp(App).use(router).use(store).mount('#app');


document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('authToken');
    if (token) {
      store.dispatch('login', token);
    }
  });
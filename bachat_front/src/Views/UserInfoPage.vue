<template>
    <div class="user-info-page">
      <h1>Персональная информация</h1>
      <p>First Name: {{ user.firstName }}</p>
      <p>Last Name: {{ user.lastName }}</p>
      <p>Email: {{ user.email }}</p>
    </div>
  </template>
  
  <script>
  import AuthService from '../services/AuthService';
  
  export default {
    name: 'UserInfoPage',
    data() {
      return {
        user: {
          firstName: '',
          lastName: '',
          email: ''
        }
      };
    },
    methods: {
      loadUserInfo() {
        console.log("Loading user info...");
        return AuthService.loadUserInfo().then(response => {
          this.user.firstName = response.data.firstName;
          this.user.lastName = response.data.lastName;
          this.user.email = response.data.email;
          console.log("User info loaded:", this.user);
        }).catch(error => {
          console.error('Load user info error:', error);
        });
      }
    },
    mounted() {
      this.loadUserInfo();
    }
  };
  </script>
  
  <style>
  .user-info-page {
    padding: 20px;
    text-align: center;
  }
  
  .user-info-page h1 {
    margin-bottom: 20px;
  }
  
  .user-info-page p {
    font-size: 18px;
  }
  </style>
  
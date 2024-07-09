<template>
  <div class="page-container">
    <div class="logo-enter">
      <img src="../assets/logo.svg" alt="Logo">
    </div>
    <div v-if="!isLoggedIn" class="Header_enter">
      Welcome!
    </div>
    <div v-else class="Header_enter">
      Welcome, {{ user.firstName }} {{ user.lastName }}!
    </div>
    <div v-if="!isLoggedIn" class="form-container">
      <form @submit.prevent="login" class="login-form">
        <div class="fontFamily-form">
          <div class="form-group">
            <input type="email" v-model="loginData.email" required placeholder="Email">
          </div>
          <div class="form-group">
            <input type="password" v-model="loginData.password" required placeholder="Password">
          </div>
          <div class="buttons">
            <button type="submit">Log In</button>
            <button type="submit"><router-link to="/registr">Register</router-link></button>
          </div>
        </div>
      </form>
    </div>
    <div v-else class="user-info">
      <!-- Персональная информация пользователя -->
      <h2>User Information</h2>
      <p>First Name: {{ user.firstName }}</p>
      <p>Last Name: {{ user.lastName }}</p>
      <p>Email: {{ user.email }}</p>
    </div>
  </div>
</template>

<script>
import AuthService from '../services/AuthService';

export default {
  name: 'LoginPage',
  data() {
    return {
      loginData: {
        email: '',
        password: ''
      },
      user: {
        firstName: '',
        lastName: '',
        email: ''
      }
    };
  },
  computed: {
    isLoggedIn() {
      return this.$store.state.isLoggedIn;
    }
  },
  methods: {
    login() {
      console.log("Attempting login...");
      this.$store.dispatch('login', this.loginData)
        .then(() => {
          console.log("Login successful, loading user info...");
          return this.loadUserInfo();
        })
        .then(() => {
          console.log("User info loaded, redirecting...");
          this.$router.push('/userInfo'); 
        })
        .catch(error => {
          console.error('Login error:', error);
        });
    },
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
    document.body.style.backgroundColor = "#f0f0f0";
    if (this.isLoggedIn) {
      this.loadUserInfo();
    }
  }
};
</script>


<style scoped>
.Header_enter {
  font-family: "PT Sans", sans-serif;
  font-weight: 700;
  color: #000000;
  font-size: 50px;
}

.page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 55rem;
  font-family: "PT Sans", sans-serif;
}

.logo-enter img {
  width: 500px;
  height: auto;
  margin-bottom: 2rem;
}

.form-container {
  width: 100%;
  max-width: 700px;
  background-color: #f0f0f0;
  padding: 20px;
  font-size: 20px;
  margin-top: 2%;
}

.login-form {
  border-radius: 20px;
}

.remember-forgot-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.styled-checkbox {
  visibility: hidden;
  position: absolute;
  width: 0;
  height: 0;
}

.remember-me label {
  position: relative;
  cursor: pointer;
  padding-left: 35px;
  line-height: 25px;
  user-select: none;
}

.remember-me label::before {
  content: '';
  position: absolute;
  left: 0%;
  top: 0;
  width: 25px;
  height: 25px;
  border: 2px solid #555;
  border-radius: 50%;
  background-color: white;
  transition: background-color 0.2s ease;
}

.remember-me label::after {
  content: '';
  position: absolute;
  top: 6px;
  left: 6px;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background-color: #007bff;
  transform: scale(0);
  transition: transform 0.2s ease;
}

.styled-checkbox:checked+label::before {
  background-color: #ffffff;
}

.styled-checkbox:checked+label::after {
  transform: scale(1.5);
}

.forgot-password {
  text-decoration: underline;
}
</style>
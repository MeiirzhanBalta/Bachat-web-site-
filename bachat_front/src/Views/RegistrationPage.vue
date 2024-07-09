<!-- RegistrationPage.vue -->
<template>
  <div class="page-container">
    <div class="logo-enter">
      <img src="../assets/logo.svg" alt="Logo">
    </div>
    <div class="Header_enter">
      Welcome!
    </div>
    <div class="form-container">
      <form @submit.prevent="registerUser" class="login-form">
        <div class="fontFamily-form">
          <div class="form-group">
            <input type="text" v-model="user.firstName" required placeholder="First Name">
          </div>
          <div class="form-group">
            <input type="text" v-model="user.lastName" required placeholder="Last Name">
          </div>
          <div class="form-group">
            <input type="email" v-model="user.email" required placeholder="Email">
          </div>
          <div class="form-group">
            <input type="password" v-model="user.password" required placeholder="Password">
          </div>
          <div class="form-group">
            <input type="password" v-model="user.confirmPassword" required placeholder="Confirm Password">
          </div>
          <div class="remember-forgot-wrapper">
            <div class="remember-me">
              <input type="checkbox" id="remember-me" class="styled-checkbox">
              <label for="remember-me">Remember me</label>
            </div>
            <router-link to="/forgot" class="forgot-password">Forgot Password?</router-link>
          </div>
          <div class="buttons">
            <button type="submit">Register</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import UserService from '@/services/UserService';
import AuthService from '@/services/AuthService';

export default {
  name: 'EnterPage',
  data() {
    return {
      user: {
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: ''
      }
    };
  },
  methods: {
    registerUser() {
      if (this.user.password !== this.user.confirmPassword) {
        alert("Passwords do not match!");
        return;
      }
      UserService.addUser({
        firstName: this.user.firstName,
        lastName: this.user.lastName,
        email: this.user.email,
        password: this.user.password
      }).then(() => {
        alert("Registration successful!");
        this.$router.push('/home');
      }).catch(error => {
        console.error("Error during registration: ", error);
        alert("Registration error!");
      });
    },
    loginUser() {
      AuthService.login(this.loginData)
        .then(response => {
          localStorage.setItem('authToken', response.data.token);
          this.$router.push('/home');
        })
        .catch(error => {
          console.error("Authentication error: ", error);
          alert("Authentication error!");
        });
    }
  },
  mounted() {
    this.$emit('toggle-footer', false);
    document.body.style.backgroundColor = "#f0f0f0";
  },
  beforeUnmount() {
    this.$emit('toggle-footer', true);
    document.body.style.backgroundColor = "";
  }
};
</script>


<style scoped>
.Header_enter{
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
  margin: 2rem; 
}

.form-container {
  width: 100%;
  max-width: 700px;
  background-color: #f0f0f0; 
  padding: 20px;
  font-size: 20px;
  margin-top: 2%;
}
.login-form{
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
  margin-left: 0.4rem;
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
  top: 7px;
  left: 7px;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background-color: #007bff; 
  transform: scale(0);
  transition: transform 0.2s ease;
}

.styled-checkbox:checked + label::before {
  background-color: #ffffff;
}

.styled-checkbox:checked + label::after {
  transform: scale(1.2); 
}
.forgot-password {
  text-decoration: underline; 
}
</style>

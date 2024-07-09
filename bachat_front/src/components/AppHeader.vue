<template>
  <div class="header-wrapper">
    <div class="header-container">
      <header class="header">
        <div class="left">
          <div class="logo-wrapper">
            <router-link to="/">
              <div class="left-item logo"> <img src="../assets/logo.svg" alt="logo"> </div>
            </router-link>
          </div>
          <div class="links">
            <div class="left-item"><router-link to="/statistic-page">Statistics</router-link> </div>
            <div class="left-item"><router-link to="/chat-bot">Chat Bot</router-link> </div>
            <div class="left-item"><router-link to="/doc">Documents</router-link> </div>
            <!-- <div class="left-item"><router-link to="/list">Directory</router-link></div> -->
          </div>
        </div>
        <div class="right">
          <div class="right-item" v-if="!$store.state.isLoggedIn">
            <router-link to="/enter">Login</router-link> / <router-link to="/registr">Register</router-link>
          </div>
          <div class="right-item" v-else>
            <div @click="toggleDropdown" class="user-dropdown">
              User
              <img class="dropdown-arrow" :class="{ open: showDropdown }" src="../assets/arrowDrop.png" alt="Dropdown arrow">
            </div>
            <div v-if="showDropdown" class="dropdown-content">
              <router-link to="/user-info">User</router-link>
              <button @click="$store.dispatch('logout')">Logout</button>
            </div>
          </div>
        </div>
      </header>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppHeader',
  data() {
    return {
      showDropdown: false
    };
  },
  methods: {
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    }
  }
}
</script>

<style scoped>
.header-wrapper {
  display: flex;
  justify-content: center;
}

.header-container {
  width: 100%;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 10px 20px;
  background-color: #fff;
  border-bottom: 1px solid #ddd;
}

.left, .right {
  display: flex;
  align-items: center;
}

.links {
  display: flex;
  gap: 20px;
}

.user-dropdown {
  cursor: pointer;
  position: relative;
}

.dropdown-arrow {
  width: 16px; /* фиксированный размер ширины */
  height: 16px; /* фиксированный размер высоты */
  transition: transform 0.3s;
}

.dropdown-arrow.open {
  transform: rotate(180deg);
}

.dropdown-content {
  position: absolute;
  top: 40px; /* adjust this value as needed */
  right: 0;
  background-color: white;
  border: 1px solid #ddd;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  width: 150px;
  text-align: left;
  display: flex;
  flex-direction: column;
}

.dropdown-content button, .dropdown-content a {
  display: block;
  width: 100%;
  padding: 10px;
  text-align: left;
  border: none;
  background: none;
  cursor: pointer;
  text-decoration: none;
  color: #000;
}

.dropdown-content button:hover, .dropdown-content a:hover {
  background-color: #f0f0f0;
}

/* Адаптивные стили для малых экранов */
@media (max-width: 1140px) {
  .header {
    flex-direction: column;
    padding: 10px;
    height: auto;
  }

  .left, .links {
    flex-direction: column;
    align-items: start;
  }

  .logo {
    margin-right: 0;
  }

  .links {
    gap: 10px;
  }

  .right {
    margin-top: 40px;
  }

  .button {
    justify-content: center;
    align-items: center;
  }
}
</style>

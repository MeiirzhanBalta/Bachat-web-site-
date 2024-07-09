<template>
  <div id="app">
    <header-component></header-component>
    <router-view @toggle-footer="handleToggleFooter"></router-view>
    <footer-component v-if="showFooter"></footer-component>
  </div>
</template>

<script>
import HeaderComponent from './components/AppHeader.vue'
import FooterComponent from './components/AppFooter.vue'


export default {
  name: 'App',
  components: {
    HeaderComponent,
    FooterComponent
  },
  data() {
    return {
      showFooter: true
    };
  },
  methods: {
    handleToggleFooter(show) {
      this.showFooter = show;
    }
  }
};
</script>

<style>
</style>

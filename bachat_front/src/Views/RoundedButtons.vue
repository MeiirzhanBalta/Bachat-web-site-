<!-- RoundedButtons -->
<template>
    <div class="button-container">
      <button class="rounded-button" v-for="button in buttons" :key="button.id">
        {{ button.text }}
      </button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'RoundedButtons',
    props: {
      buttons: Array
    }
  };
  </script>
  

  
<template>
    <div v-if="show" class="popup">
    <div class="popup-content">
      <h2>Test</h2>
      <p>this is a test</p>
      <button @click="closePopup">Close</button>
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';

export default {
  data() {
    return {
      msg: 'this is a test',
    };
  },
  methods: {
    closePopup() {
      this.show = false;
    }
  }
};
</script>

<!--ref: https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/-->
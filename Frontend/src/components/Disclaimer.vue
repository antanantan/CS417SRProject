<template>
    <div>
      <p>{{ msg }}</p>
    </div>
</template>
  
<script>
import axios from 'axios';

export default {
  name: 'Disclaimer',
  data() {
    return {
      msg: 'this is a test',
    };
  },
  methods: {
    getMessage() {
      const path = 'SeniorProj/backend/app.py';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>

<!--ref: https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/-->
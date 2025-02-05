<script setup>
import axios from 'axios';

</script>

<template>

<div v-if="username">
Username: {{ username }}
</div>

<button @click="logout" style="border-width: 10px; color: red;">Test Logout</button>

</template>


<script>
export default {
  data() {
    return {
      username: null,
    };
  },
  created() {
    this.profile();
  },
  methods: {
    async logout() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/logout', {});
        if (response.data.message === "you have been logged out.") {
            localStorage.removeItem('access_token');
            console.log("logout successful");
            this.$router.push("/");
        }
    }
    catch (error) {
        console.error('error:', error);
    }
    },
    async profile() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/profile', {withCredentials: true});
        if (response.data && response.data.username) {
          this.username = response.data.username;
        } else {
          console.error('no username', response.data);
          this.username = null;
        }
      }
      catch (error) {
        console.error('error:', error);
        this.username = null;
      }
    },
  },
};
</script>

<style>

</style>

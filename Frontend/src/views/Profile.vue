<script setup>
import axios from 'axios';

</script>

<template>

<div v-if="username">
  Username: {{ username }}
</div>

<div v-else>
  <p>You are not logged in.</p>
</div>

<button @click="logout" style="border-width: 10px; color: red;">Test Logout</button>

</template>


<script>
export default {
  data() {
    return {
      username: '',
    };
  },
  created() {
    this.profile();
  },
  methods: {
  async profile() {
    try {
      const response = await axios.get('http://127.0.0.1:5000/profile', { withCredentials: true });
      
      console.log("Response from backend:", response);
      
      if (response.data.username) {
        this.username = response.data.username;
      } else {
        console.error('No username returned:', response.data);
        this.username = null;
      }
    } catch (error) {
      console.error('Error fetching profile:', error);
      this.username = null;
    }
  },
    async logout() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/logout', {});
        if (response.data.message === "you have been logged out.") {
          this.username = '';
          console.log("logout successful");
          this.$router.push("/");
        }
      }
      catch (error) {
        console.error('error:', error);
      }
    },
  },
};
</script>

<style>

</style>

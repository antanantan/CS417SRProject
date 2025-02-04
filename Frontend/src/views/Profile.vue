<script setup>
import axios from 'axios';

</script>

<template>


<br>

<button @click="logout" style="border-width: 10px; color: red;">Test Logout</button>

</template>

<!--TODO: allow for session to grab user data from the session and display it on the profile.-->

<script>
export default {
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
    }
  },
};
</script>

<style>

</style>

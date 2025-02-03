<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();

const goToForgotPassword = () => {
  router.push('/forgot-password');
};

const continueAsGuest = () => {
  router.push('/allergy_list'); 
};
</script>

<!--ref: https://medium.com/@karthikreddy17/building-a-secure-login-system-with-flask-and-vue-js-a-step-by-step-guide-5cc1e4fd7a15-->

<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-8">
      <div class="text-center mb-6">
        <b>Log Into Your Account</b>
      </div>
      Or <a href="/create" style="color:palevioletred">Create a New Account</a>
      <br>

<!--marks beginning of login implementation-->

      <form @submit.prevent="login">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
            Username
          </label>
          <input v-model="username" type="text" id="username" placeholder="Enter your username" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500" required/>
        </div>

        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
            Password
          </label>
          <input v-model="password" type="password" id="password" placeholder="Enter your password" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500" required/>
        </div>

        <button type="submit" class="w-full bg-green-500 text-white font-bold py-2 rounded-lg hover:bg-green-600 focus:outline-none focus:bg-green-700">
          Sign In
        </button>
      </form>

      <div class="text-center mt-4">
        <RouterLink
          to="/forgot-password"
          class="text-blue-500 hover:underline"
          @click.prevent="goToForgotPassword">
          Forgot password?
        </RouterLink>
        <span class="text-gray-500 mx-2">or</span>
        <RouterLink
          to="/"
          class="text-blue-500 hover:underline"
          @click.prevent="continueAsGuest">
          Continue as Guest
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { errorMessages } from 'vue/compiler-sfc';

export default {
  data() {
    return {
      username_current: '',
      password_current: '',
      errorMessage: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/login', {username: username_current, password: password_current});
        localStorage.setItem('access_token', response.data.access_token);
        console.log('logging in with', username.value, password.value);
        this.$router.push({ name: 'Profile' }); 
      } catch (error) {
        this.errorMessage = error.response ? error.response.data.message : 'an error occurred.';
      }
    }
  }
};
</script>

<style></style>

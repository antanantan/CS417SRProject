<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const username = ref('');
const email = ref('');
const password = ref('');
const router = useRouter();

const continueAsGuest = () => {
  router.push('/allergy_list'); 
};

</script>

<template>
<h1>Create Your Account to Get Started.</h1>

<div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-8">
      <div class="text-center mb-6">
      </div>
      <form @submit.prevent="register">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="username" required>
            Username
          </label>
          <input
            v-model="new_username"
            type="text"
            id="username"
            placeholder="Enter a username"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
          />
        </div>

        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="email" required>
            Email
          </label>
          <input
            v-model="new_email"
            type="text"
            id="email"
            placeholder="Enter your email"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
          />
        </div>

        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="password" required>
            Password
          </label>
          <input v-model="new_password" type="password" id="password" placeholder="Enter a password" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"/>
        </div>

        <button
          type="submit"
          class="w-full bg-green-500 text-white font-bold py-2 rounded-lg hover:bg-green-600 focus:outline-none focus:bg-green-700"
        >
          Create Account
        </button>
      </form>

      <div class="text-center mt-4">
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
export default {
  data() {
    return {
      new_username: '',
      new_email: '',
      new_password: '',
      errorMessage: '',
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/register', {username: this.new_username, email: this.new_email, password: this.new_password,});

        if (response.data.message === 'account created successfully.') {
          this.$router.push('/profile');  
        }
      } 
      catch (error) {
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.message || 'something went wrong';
        }
      }
    },
  },
};

</script>


<style>

</style>


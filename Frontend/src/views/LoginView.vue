<script setup>
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ref } from 'vue';

const router = useRouter();
const current_username = ref('');
const current_password = ref('');
const errorMessage = ref('');

const goToForgotPassword = () => {
  router.push('/forgot-password');
};

const continueAsGuest = () => {
  router.push('/allergy_list'); 
};


const login = async () => {
  try {
    const response = await axios.post('http://localhost:5000/login', {
      username: current_username.value,
      password: current_password.value,
    }, { withCredentials: true }
  );

  if (response.data.token) {
    const token = response.data.token;
    console.log("Logged in as", current_username.value);

    localStorage.setItem('token', token);
    router.push('/profile');

  }else{
    errorMessage.value = "Login failed. Please try again."
  }
} catch (error) {
  errorMessage.value = error.response ? error.response.data.message : 'Something went wrong.';
}
};

</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-8">
      <div class="text-center mb-6">
        <b>Log Into Your Account</b>
      </div>
      Or <a href="/create" style="color:palevioletred">Create a New Account</a>
      <br>



      <form @submit.prevent="login">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
            Username
          </label>
          <input v-model="current_username" type="text" id="username" placeholder="Enter your username" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500" required/>
        </div>

        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
            Password
          </label>
          <input v-model="current_password" type="password" id="password" placeholder="Enter your password" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500" required/>
        </div>

        <button type="submit" class="w-full bg-green-500 text-white font-bold py-2 rounded-lg hover:bg-green-600 focus:outline-none focus:bg-green-700">
          Sign In
        </button>

        <br>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

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

<style scoped>
.error-message {
  color: red;
  font-weight: bold;
  display:flex;
  text-align: center;
}
</style>

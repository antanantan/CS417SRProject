<script setup>
import { ref} from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api/auth.js';
import axios from 'axios';

const router = useRouter();

const new_username = ref('');
const new_password = ref('');
const new_email = ref('');
const errorMessage = ref(''); 

const continueAsGuest = () => {
  router.push('/allergy_list'); 
};

const GoToLogin = () => {
  router.push('/login');
};  

const register= async () =>{
  if(!new_username.value || !new_email.value || !new_password.value){
    errorMessage.value = 'Please fill out all fields';
    return;
  }
  try{
    const response = await api.post('/auth/register',{
      username: new_username.value,
      email: new_email.value,
      password: new_password.value,  
  }
);
  if (response.status === 201) {
    console.log("Account created: ,", new_username.value);
    localStorage.setItem('token', response.data.token);
    router.push('/profile');
  }
} catch(error){
  if (error.response){  
    const status = error.response.status;
    if (status === 422) {
      errorMessage.value = 'Username or email already in use. Please choose another.';
    } else if(status === 400){
      errorMessage.value = 'Invalid input.';
    } else {
      errorMessage.value = error.response.data.message;
    }
  }
  }
};
</script>

<template>
<h1>Create Your Account to Get Started.</h1>

<div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-8">
      <div class="text-center mb-6">
        <b>Create Your Account</b>
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
            required
          />
        </div>

        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="email" >
            Email
          </label>
          <input
            v-model="new_email"
            type="text"
            id="email"
            placeholder="Enter your email"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
            required
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

      <br>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

        <div class="text-center mt-4">
        <RouterLink
          to="/login"
          class="text-blue-500 hover:underline"
          @click.prevent="GoToLogin">
          Log In
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


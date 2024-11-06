<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const router = useRouter();

const handleLogin = () => {
  // Replace with actual login logic
  console.log('Logging in with', email.value, password.value);
  // Navigate to a different route if needed
};

const goToForgotPassword = () => {
  router.push('/forgot-password');
};

const continueAsGuest = () => {
  router.push('/allergy_list'); 
};
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-8">
      <div class="text-center mb-6">
      </div>
      <br>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="email">
            Email/Username
          </label>
          <input
            v-model="email"
            type="text"
            id="email"
            placeholder="Enter your email or username"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
          />
        </div>

        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
            Password
          </label>
          <input
            v-model="password"
            type="password"
            id="password"
            placeholder="Enter your password"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
          />
        </div>

        <button
          type="submit"
          class="w-full bg-green-500 text-white font-bold py-2 rounded-lg hover:bg-green-600 focus:outline-none focus:bg-green-700"
        >
          Sign In
        </button>
      </form>
<!--reference: https://www.shecodes.io/athena/53677-how-to-create-a-login-page-with-form-validation-using-html-css-and-javascript-->
      <!--script type="text/javascript">
        const form = document.querySelector('form');
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // prevent default form submission behavior

            // validate username and password
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            if (username === 'myusername' && password === 'mypassword') {
                alert('Login successful!');
            } else {
                alert('Username or password incorrect. Please try again.');
            }
        });
    </script-->
<!--maybe we have to implement some js to confirm or deny the user access-->

      <div class="text-center mt-4">
        <RouterLink
          to="/forgot-password"
          class="text-blue-500 hover:underline"
          @click.prevent="goToForgotPassword"
        >
          Forgot password?
        </RouterLink>
        <span class="text-gray-500 mx-2">or</span>
        <RouterLink
          to="/home"
          class="text-blue-500 hover:underline"
          @click.prevent="continueAsGuest"
        >
          Continue as Guest
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Add any custom styles here */
</style>

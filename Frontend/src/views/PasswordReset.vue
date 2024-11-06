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

const continueAsGuest = () => {
  router.push('/allergy_list'); 
};
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-8">
      <div class="text-center mb-6">
      </div>
      <form>
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="email">
            Let's get you back into your account.
          </label>
          <input
            v-model="email"
            type="text"
            id="email"
            placeholder="Enter your email or username"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
          />
        </div>

        <button
          type="submit"
          class="w-full bg-green-500 text-white font-bold py-2 rounded-lg hover:bg-green-600 focus:outline-none focus:bg-green-700"
        >
          Submit
        </button>
      </form>
    <!--this would be a good test to see if we can actually send things to an email address-->
    </div>
  </div>
</template>

<style scoped>
/* Add any custom styles here */
</style>

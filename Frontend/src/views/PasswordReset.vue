<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const email = ref('');
const errorMessage = ref('');

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
            placeholder="Enter the email associated with your account."
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

      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <!--this would be a good test to see if we can actually send things to an email address-->
    </div>
  </div>
</template>

<script>
const email = ref('');
const errorMessage = ref('');
const newPassword = ref('');  
const resetMessage = ref('');  
const resetSuccess = ref(false); 

const resetPassword = async () => {
  try {
    const response = await fetch('/auth/password_reset', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email.value, 
        new_password: newPassword.value,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      resetMessage.value = data.message;
      resetSuccess.value = true;
    } else {
      resetMessage.value = data.message;
      resetSuccess.value = false;
    }
  } catch (error) {
    resetMessage.value = 'An error occurred. Please try again.';
    resetSuccess.value = false;
  }
};
</script>

<style scoped>
</style>

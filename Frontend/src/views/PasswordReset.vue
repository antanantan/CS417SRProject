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
export default {
  data() {
    return {
      new_email: '',
      errorMessage: '',
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/register', {username: this.new_username, email: this.new_email, password: this.new_password,});

        if (response.data.message === 'account created successfully.') {
          this.$router.push('/login');  
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

<style scoped>
</style>

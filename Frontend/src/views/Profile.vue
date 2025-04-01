<script setup>
import axios from 'axios';
import {ref, onMounted} from 'vue';
import { api, authApi } from '@/api/auth.js';
import { useRouter } from 'vue-router';
import Card from '@/components/Steps_Bottom.vue';

const username = ref('');
const email = ref('');
const allergies = ref([]);
const router = useRouter(); 
const errorMessage = ref('');
const newPassword = ref('');  
const resetMessage = ref('');  
const resetSuccess = ref(false);  

// function to grab profile information from backend based on token
const fetchProfile = async () => {
  try {
    const response = await authApi.get('/user/profile');
    if (response.data.username) {
        username.value = response.data.username;
        email.value = response.data.email;
        allergies.value = response.data.allergies || [];
    } else {
      console.warn('No username returned:', response.data);
      username.value = null;
    }
  } catch (error) {
    if (error.response?.status === 401) {
      localStorage.removeItem('token'); 
      errorMessage.value = 'Your session has expired. Please log in again.';
      await router.push('/login');
    } else {
      errorMessage.value = 'Failed to load profile'
      console.error(error);
    ;}
    username.value = null;
  }
}; 

const deleteAccount = async () => {
  if (!confirm('Are you sure you want to delete your account?')) return;

  try {
    const response = await authApi.delete('/user/delete');

    if (response.status === 200) {
      alert(response.data.message);
      localStorage.removeItem('token');
      await router.push('/login');

    } else {
      alert('Failed to delete account. Please try again');
      await router.push('/profile');
    }
  } catch (error) {
    console.error('Error deleting the account:', error);
    alert('An error occurred. Please try again.');
    await router.push('/profile');
  }
};


const resetPassword = async () => {
  try {
    const response = await authApi.post('/auth/password_reset', {
      email: email.value,
      new_password: newPassword.value,
    });

    resetMessage.value = response.data.message;
    resetSuccess.value = true;
  } catch (error) {
    console.error('Error resetting password:', error);
    resetMessage.value = error.response?.data?.message || 'An error occurred. Please try again.';
    resetSuccess.value = false;
  }
};

const logout = () => {
  localStorage.removeItem('token');
  username.value = '';
  console.log('Logged out');
  router.push('/login');
}

onMounted(fetchProfile);

const allergyPage = () => {
  router.push('/allergy_list'); 
};
</script>



<template>
  <br>
  <div v-if="username" class="profile_container">
    <h1>Welcome, {{ username }}</h1>
    <h2>email: {{ email }}</h2>
    <br>
    <div class="allergy_section">
      <h2 v-if="allergies"> {{ username }}'s allergies...</h2>
      <h2 v-else>User has no listed allergies</h2>
        <ul>
          <li v-for="(allergy, index) in allergies" :key="index">{{ allergy }}</li>
        </ul>
    </div>

    <button @click="logout">Logout</button>
    <button @click="allergyPage">Go To Order</button>
    <button @click="deleteAccount" class="delete-button">Delete Account</button>


    <div class="password-reset-section">
      <h3>Reset Your Password</h3>
      <form @submit.prevent="resetPassword">
        <input
          v-model="newPassword"
          type="password"
          placeholder="Enter new password"
          required
          class="password-input"
        />
        <button type="submit" class="reset-btn">Reset Password</button>
      </form>
      <div v-if="resetMessage" :class="{'success': resetSuccess, 'error': !resetSuccess}">
        {{ resetMessage }}
      </div>
    </div>
  </div>



  <div v-else>
    <h1>You are not logged in. Please log in or create an account to continue.</h1>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>

  
 <Card />
</template>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  display: flex;
  justify-content: center;
}
.allergy-section h2 {
  font-size: 1.5rem;
  color: #555;
  margin-bottom: 10px;
  display: flex;
  justify-content: center;
}
.error-message {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
button {
  background:green;
  font-weight: bold;
  margin: 10px;
  color: white;
  padding: 12px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
button:hover {
  background: darkgreen;
}
ul {
  margin-left: 10%;
  margin-right: 80%;
  font-size: medium;
  list-style-type: none;
  padding: 0;
}
ul li {
  font-size: 1rem;
  padding: 8px;
  background-color: #fee1ee;
  margin-bottom: 5px;
  border-radius: 4px;
}
</style>
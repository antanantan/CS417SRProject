<script setup>
import axios from 'axios';
import {ref, onMounted} from 'vue';
import { useRouter } from 'vue-router';

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
  const token = localStorage.getItem('token');
    if (!token) {
      errorMessage.value = 'You are not logged in.';
      await router.push('/login');
      return;
    } 
    try {
    const response = await axios.get('http://localhost:5000/profile', {
      headers: { Authorization: `Bearer ${token}` }, 
  });

  if (response.data.username) {
      username.value = response.data.username;
      email.value = response.data.email;
      if (response.data.allergies) {
        allergies.value = response.data.allergies;
      }
      else {
        console.warn('User has no listed allergies.', response.data);
      }
    } else {
      console.warn('No username returned:', response.data);
      username.value = null;
    }
} catch (error) {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token'); 
      errorMessage.value = 'Your session has expired. Please log in again.';
      await router.push('/login');
    } else {errorMessage.value = 'Failed to load profile';}
    username.value = null;}
}; 

const resetPassword = async () => {
  try {
    const response = await fetch('http://localhost:5000/password_reset', {
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
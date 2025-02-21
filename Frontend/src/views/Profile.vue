<script setup>
import axios from 'axios';
import {ref, onMounted} from 'vue';
import { useRouter } from 'vue-router';

const username = ref('');
const allergies = ref([]);
const router = useRouter(); 
const errorMessage = ref('');

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
  <div v-if="username">
    <h1>Welcome, {{ username }}</h1>
    <button @click="logout">Logout</button>
  </div>
  <div v-else>
    <h1>You are not logged in</h1>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>

  <button @click="allergyPage">Go To Order</button>

  <ul>
    <li v-for="(allergy, index) in allergies" :key="index">{{ allergy }}</li>
  </ul>

</template>

<style scoped>
.error-message {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
</style>
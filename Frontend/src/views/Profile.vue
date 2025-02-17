<script setup>
import axios from 'axios';
import {ref, onMounted} from 'vue';
import { useRouter } from 'vue-router';

const username = ref('');
const router = useRouter(); 
const errorMessage = ref('');

const fetchProfile = async () => {

  const token = localStorage.getItem('token'); //retrieves token from the local storage

    if (!token) {
      errorMessage.value = 'You are not logged in';
      await router.push('/login');
      return;
    } 
    try{
    const response = await axios.get('http://localhost:5000/profile', {
      headers: { Authorization: `Bearer ${token}` }, //sends token in header.
  });

  if (response.data.username) {
      username.value = response.data.username;
    } else {
      console.error('No username returned:', response.data);
      username.value = null;
    }
  } catch (error) {
    console.error('Error fetching profile:', error);
    username.value = null;
  }
};
if (errorMessage.response.status === 401) {
  localStorage.removeItem('token'); //expired token
  errorMessage.value = 'Your session has expired. Please log in again.';
  await router.push('/login');
} else {
  errorMessage.value = "Failed to load profile";
}
  username.value = null;
};
 

const logout = () => {
  localStorage.removeItem('token');
  username.value = '';
  console.log('Logged out');
  router.push('/login');
}

onMounted(fetchProfile);
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
</template>
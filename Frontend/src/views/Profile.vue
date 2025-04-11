<script setup>
import axios from 'axios';
import {ref, onMounted} from 'vue';
import { api, authApi } from '@/api/auth.js';
import { useRouter } from 'vue-router';
import { userAllergies, fetchUserAllergies } from '@/composables/useUserAllergies.js';

const username = ref('');
const email = ref('');
// const allergies = ref([]);
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
        // allergies.value = response.data.allergies || [];
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
    <h1 style="text-align: center; font-weight: bolder; font-size: xx-large;">welcome, {{ username }}</h1>
    <h2 style="text-align: center; font-size: large; padding-top: 1%;">email address: {{ email }}</h2>
    <br>

    <div class="button-line">
      <button @click="logout">Logout</button>
      <button @click="allergyPage">Go To Order</button>
      <button @click="deleteAccount" class="delete-button">Delete Account</button>
    </div>

    <div class="allergy-section">
      <h2 class="allergy-header" v-if="userAllergies">{{ username }}'s allergies...</h2>
      <h2 class="allergy-header" v-else>User has no listed allergies</h2>
      <ul class="allergy-list">
        <li v-for="(allergy, index) in userAllergies" :key="index">{{ allergy.name }}</li>
      </ul>
    </div>

    <br>

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
    <h1 style="font-size: xx-large; text-align: center; padding-top: 2%;">You are not logged in. Please <a href ="/login" style="color: #f55d8b;">log in</a> or <a href ="/create" style="color: #f55d8b;">create an account</a> to continue.</h1>
    <div v-if="errorMessage" class="error-message" style="text-align: center; font-size: large;">{{ errorMessage }}</div>
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
.allergy-section {
  border: 3px solid #f55d8b; 
  border-radius: 8px;        
  width: max-content;
  max-width: 90%;          
  margin: 20px auto;         
  padding: 20px;           
  background-color: #f9f9f9;
}
.allergy-header {
  padding: 10px 20px;      
  font-size: x-large;
  font-weight: bold;
  color: #6c6c6c;  
  margin-bottom: 15px;     
  text-align: center;        
  border-radius: 5px;        
}
.allergy-list {
  list-style-type: none;  
  padding: 0;
  margin: 0;
}

.allergy-list li {
  padding: 10px;
  background-color: #fff;    
  border: 1px solid #ddd; 
  margin-bottom: 10px;        
  border-radius: 5px;    
  transition: background-color 0.3s, transform 0.3s;
}

.allergy-list li:hover {
  background-color: #2d9f48; 
  color: white;           
  transform: translateX(5px); 
}

.allergy-list li:last-child {
  margin-bottom: 0;    
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
.button-line {
  display: flex;
  justify-content: center;
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
  width:max-content;
  margin-bottom: 5px;
  border-radius: 4px;
}

.password-reset-section {
  background-color: #f7f7f7;    
  padding: 20px;                 
  border-radius: 8px;            
  max-width: 400px;              
  margin: 20px auto;
}

.password-reset-section h3 {
  font-size: 1.25rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;            
  text-align: center;
}

.password-input {
  width: 100%;            
  padding: 12px;                 
  margin-bottom: 15px;           
  border: 1px solid #ddd;      
  border-radius: 5px;            
  font-size: 1rem;             
  background-color: #fff;       
}

.password-input:focus {
  outline: none;                
  border-color: #f55d8b;         
}

.reset-btn {
  width: 100%;                   
  padding: 12px;                
  font-size: 1rem;               
  background-color: #f55d8b;
  color: white;                  
  border: none;                 
  border-radius: 5px;            
  cursor: pointer;               
  transition: background-color 0.3s; 
}

.reset-btn:hover {
  background-color: #f85c9e;  
}

.password-reset-section .success,
.password-reset-section .error {
  padding: 10px;
  margin-top: 15px;
  text-align: center;
  font-size: 1rem;
  border-radius: 5px;
  color: white;
}

.password-reset-section .success {
  color: #28a745;
  font-weight: bolder;
}

.password-reset-section .error {
  background-color: #dc3545; 
  font-weight: bolder;
}

</style>
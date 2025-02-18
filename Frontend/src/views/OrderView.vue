<script setup>
import Card from '@/components/Steps_Bottom.vue';
import axios from 'axios';
const continueAsGuest = () => {
  router.push('/allergy_list'); 
};
const createAccount = () => {
  router.push('/create'); 
};
</script>

<template>
    <h1>Step 4: Place your Order</h1>
    <h2>Order Recap</h2>
   
   <RouterLink
          to="/create"
          class="text-blue-500 hover:underline"
          @click.prevent="createAccount">
          To save information for future orders, please create an account.
      </RouterLink>
    
    <Card></Card>
</template>

<script>
// has to be able to push the information that the user included in their order
</script>
  
<style>
h1 {
  font-size: xx-large;
  text-align: center;
}
</style>
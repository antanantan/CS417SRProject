<script setup>
import Card from '@/components/Steps_Bottom.vue';
import axios from 'axios';
const continueAsGuest = () => {
  router.push('/allergy_list'); 
};
</script>

<template>
    <h1>Step 4: Place your Order</h1>
<!--the option to create an account should also be here like at the end,
    i.e. "to save information for future orders please create an account" type thing-->
    
    <Card></Card>
</template>
  
<style>
h1 {
  font-size: xx-large;
  text-align: center;
}
</style>
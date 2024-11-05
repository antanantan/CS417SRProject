<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const locationPicker = () => {
  router.push('/location');
};

</script>

<template>
    <p>this page will have a list of allergens and dietary restrictions that the user can filter</p>
          Next Step: Location
    
  </template>

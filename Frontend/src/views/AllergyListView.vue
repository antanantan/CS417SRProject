<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const gotoLocationPicker = () => {
  router.push('/location');
};

</script>

<template>
    <p>this page will have a list of allergens and dietary restrictions that the user can filter</p>
    <div class="text-center mt-4">
        <RouterLink
          to="/location"
          class="text-blue-500 hover:underline"
          @click.prevent="gotoLocationPicker">
          Step 2: Location Picker
        </RouterLink>
    </div>
    
  </template>

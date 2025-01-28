<script setup>
import Card from '@/components/Steps_Bottom.vue';
</script>

<template>
  <h1>Step 2: Select Location</h1>
<!--ref: https://www.google.com/search?q=insert+map+in+vue+using+folium&oq=insert+map+in+vue+using+folium&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDQ0MDFqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8-->


  <form method="POST">
    <label for="zip">ZIP/Postal Code: </label>
    <input type="text" id="zip" name="zip" required>
    <button @click="submitZipCode">Submit</button>
    <br>
    
  </form>
  
  <div>
    <iframe src="/src/assets/map.html" width="800" height="650"></iframe>
  </div>


  <Card></Card>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      mapURL: "/src/assets/map.html" 
    };
  },
};
</script>

<style>
h1 {
  font-size: large;
  text-align: center;
}
</style>
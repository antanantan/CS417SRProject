<script setup>
import Card from '@/components/Steps_Bottom.vue';
</script>

<template>
  <h1>Step 2: Select Location</h1>
<!--ref: https://www.google.com/search?q=insert+map+in+vue+using+folium&oq=insert+map+in+vue+using+folium&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDQ0MDFqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8-->


  <form @submit.prevent="submitZipCode">
      <label for="zip">ZIP/Postal Code: </label>
      <input type="text" v-model="zip" id="zip" name="zip" required />
      <button type="submit">Submit</button>
    </form>
  
  
  <div v-if="mapUrl">
      <iframe :src="mapUrl" width="800" height="650"></iframe>
  </div>

  <Card></Card>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      zip: '', 
      error: null,
      mapUrl: null,
    };
  },
  methods: {
    async submitZipCode() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/location', {zip_code: this.zip,});

        if (response.data.map_url) {
          this.map_url = response.data.map_url;  
          this.error = null;  
        } else {
          this.error = 'Invalid ZIP code or location not found.';
        }
      } catch (err) {
        this.error = 'Error communicating with backend.';
        console.error(err);
      }
    },
  },
};
</script>

<style>
h1 {
  font-size: large;
  text-align: center;
}
</style>
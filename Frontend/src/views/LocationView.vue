<script setup>
import Card from '@/components/Steps_Bottom.vue';
</script>

<template>
  <h1>Step 2: Select Location</h1>

  <form @submit.prevent="generateMap">
      <label for="zip">ZIP/Postal Code: </label>
      <input type="text" v-model="zip_entered" id="zip" name="zip" required/>
      <button type="submit" style="border: 1rem; border-color: black; color:greenyellow">Submit</button>
    </form>
  
  <div v-if="loading"></div>

  <iframe v-if="map_displayed" :src="map_displayed" width="800" height="650"></iframe>

  <Card></Card>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      zip_entered: '', 
      map_displayed: '',
      loading: false,
    };
  },
  methods: {
    async generateMap() {
      if (!this.zip_entered) {
        alert('please enter a zip code.')
        return;
      }

      this.loading = true;

      try {
        const response = await axios.post('http://127.0.0.1:5000/location', {zip_code: this.zip_entered,});

        this.map_displayed = `http://127.0.0.1:5000${response.data.map_url}?t=${new Date().getTime()}`;  
        }
      catch (error) {
        this.error = 'error generating map.';
        console.error(error);
      }
      finally {
        this.loading = false;
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
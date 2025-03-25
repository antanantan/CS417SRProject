<script setup>
import Card from '@/components/Steps_Bottom.vue';
import api from '@/api/auth.js';
</script>

<template>
  <h1>Step 2: Select Location</h1>
  <br>
  <form @submit.prevent="generateMap" style="display: flex; justify-content: center;">
      <label for="zip" style="font-size:large;">ZIP/Postal Code:  </label>
      <input type="text" v-model="zip_entered" id="zip" name="zip" style="border-width: 5px; border-color: #48ab4e; border-radius:10%" required/>
      <button type="submit">Submit</button>
    </form>
  <br>
  <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  <br>

<div class="map_container">
  <iframe v-if="map_displayed" :src="map_displayed"></iframe>
</div>

  <Card></Card>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      zip_entered: '', 
      map_displayed: '',
      errorMessage: null,
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
        const response = await api.post('/location', {zip_code: this.zip_entered,});
        if (response.data.error) {this.errorMessage = response.data.error;} 
        else {this.map_displayed = `${response.data.map_url}?t=${new Date().getTime()}`;}}
      catch (error) {
        this.errorMessage = 'error generating map.';
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
h1 {
  font-size: xx-large;
  text-align: center;
}
button {
  border-width: 5px; 
  border-color: darkgreen; 
  color:white;
  border-radius: 10%;
  background-color: chartreuse;
}
button:hover {
  color: darkgreen;
}
.map_container {
  display: flex;
  justify-content: center;
}
iframe {
  border-width: 1rem; 
  border-radius: 5%;
  border-color: #f27e9f; 
  width: 800px;
  height: 550px;
}
.error-message {
  color: red;
  font-weight: bold;
  display:flex;
  justify-content: center;
  font-size: large;
}

</style>
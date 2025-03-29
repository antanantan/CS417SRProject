<script setup>
import Card from '@/components/Steps_Bottom.vue';
import { api, authApi } from '@/api/auth.js';
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

<div>
  <div v-if="selectedMarker">
    <p><strong>Name:</strong> {{ selectedMarker.name }}</p>
    <p><strong>Address:</strong> {{ selectedMarker.address }}</p>
  </div>
  <div v-else>
    <p style="text-align: center; font-size: x-large;">No marker selected yet.</p>
  </div>
</div>

  <Card></Card>
</template>


<script>
import L from "leaflet";

export default {
  data() {
    return {
      zip_entered: '', 
      map_displayed: '',
      markers: [],
      errorMessage: null,
      selectedMarker: null,
    };
  },
  methods: {
    async generateMap() {
      if (!this.zip_entered) {
        alert('please enter a zip code.')
        return;
      }

      try {
        const response = await fetch('/location', {method: 'POST', headers:{'Content-Type': 'application/json'}, body: JSON.stringify({ zip_code: this.zip_entered }),});
        const data = await response.json();
        if (response.ok) {
          // Clear any previous map
          if (this.map_displayed) {
            this.map_displayed.remove();
          }
          const firstRestaurant = data[0];  // Use the first restaurant to center the map
          this.map = L.map(this.$refs.mapContainer).setView(
            [firstRestaurant.latitude, firstRestaurant.longitude],
            12
          );

          // Set OpenStreetMap tiles
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(this.map);

          // Create markers for each restaurant
          data.forEach((restaurant) => {
            const marker = L.marker([restaurant.latitude, restaurant.longitude])
              .addTo(this.map)
              .bindPopup(`
                <b>${restaurant.name}</b><br>
                ${restaurant.address}
              `)
              .on('click', () => {
                // When marker is clicked, handle marker selection
                this.handleMarkerSelection(restaurant);
              });
            this.markers.push(marker);
          });
        } else {
          this.errorMessage = data.error || 'Error generating map.';
        }}
      catch (error) {
        this.errorMessage = 'error generating map.';
        console.error(error);
      }
    },
    async handleMarkerSelection(markerData) {
      try {
        const response = await fetch('/location_select', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(markerData), 
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();  
        if (data.status === 'success') {
          this.selectedMarker = data.selected_marker; 
        } else {
          console.error('Error: ', data.error);
        }
      } catch (error) {
        console.error('Error sending marker data:', error);
      }
    }
  },
  mounted() {
    fetch('/location_select', {method: 'POST', headers: {'Content-Type': 'application/json',}})
      .then((response) => response.json())
      .then((data) => {
        if (data.status === 'success') {
          this.handleMarkerSelection(data.selected_marker);
        }
      })
      .catch((error) => {
        console.error('Error fetching marker data:', error);
      });
  }
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

<template>
  <h1>Step 2: Select Location</h1>
  <br>
  <form @submit.prevent="generateMap" style="display: flex; justify-content: center;">
      <label for="zip" style="font-size:large;">ZIP/Postal Code:  </label>
      <input type="text" v-model="zip_entered" id="zip" name="zip" style="border-width: 5px; border: solid #48ab4e; border-radius:10%" required/>
      <button type="submit">Submit</button>
    </form>
  <br>
  <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  <br>

<div class="map_wrapper">
  <div ref="map_container" style="height: 100%; width: 100%;"></div>
</div>

<div v-if="selectedMarker" style="text-align: center; font-size: x-large;">
  <p><strong>Name:</strong> {{ selectedMarker.name }}</p>
  <p><strong>Address:</strong> {{ selectedMarker.address }}</p>
  <button @click="confirmSelection" :disabled="!selectedMarker" class="nav-button next-button">> Confirm Selection </button>
</div>
<div v-else>
  <p style="text-align: center; font-size: x-large;">No marker selected yet.</p>
</div>
</template>

<script>
import L from "leaflet";
import { useRouter } from 'vue-router';  // Import the useRouter hook

export default {
  props: ['restaurantId'],
  data() {
    return {
      zip_entered: '', 
      map_displayed: '',
      markers: [],
      errorMessage: null,
      selectedMarker: null, // Will hold the selected restaurant's data
    };
  },
  methods: {
    // Trigger navigation to the menu page after the selection
    proceedToMenu(restaurantId) {
      this.$router.push(`/menu/${restaurantId}`);  // Using this.$router for Options API
    },

    // Confirm the restaurant selection
    confirmSelection() {
      if (this.selectedMarker) {
        this.proceedToMenu(this.selectedMarker.id); // Navigate to the menu page with the selected restaurant ID
      }
    },

    async generateMap() {
      if (!this.zip_entered) {
        alert('Please enter a zip code.')
        return;
      }

      try {
        this.errorMessage = null; // resets error messages
        const response = await fetch('/api/location', {method: 'POST', headers:{'Content-Type': 'application/json'}, body: JSON.stringify({ zip_code: this.zip_entered }),});
        const data = await response.json();

        if (response.ok && data && data.length > 0) {
          const firstRestaurant = data[0];  
          if (this.map) {
            this.map.remove();
          }
          this.map = L.map(this.$refs.map_container).setView(
            [firstRestaurant.latitude, firstRestaurant.longitude],
            12
          );

          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 19}).addTo(this.map);
          this.$nextTick(() => {
            this.map.invalidateSize();
          });       
          data.forEach((restaurant) => {
            const marker = L.marker([restaurant.latitude, restaurant.longitude])
              .addTo(this.map)
              .bindPopup(`
                <b>${restaurant.name}</b><br>
                ${restaurant.address}
              `)
              .on('click', () => {
                this.handleMarkerSelection(restaurant);
              });
            this.markers.push(marker);
          });
          
        } else {
          this.errorMessage = data.error || 'Error generating map.';
        }
      }
      catch (error) {
        this.errorMessage = 'Error generating map.';
        console.error(error);
      }
    },

    async handleMarkerSelection(markerData) {
      try {
        const response = await fetch('/api/location_select', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(markerData),
        });

        if (!response.ok) {
          throw new Error(`HTTP error. Status: ${response.status}`);
        }

        const data = await response.json();

        if (data.status === 'success') {
          this.selectedMarker = data.selected_marker;
        } else {
          console.error('Error:', data.error);
        }
      } catch (e) {
        console.error('Error sending marker data:', e);
      }
    },

    async fetchMenuForRestaurant(restaurantId) {
      try {
        const response = await fetch(`/api/${restaurantId}`, {
          method: 'GET',
        });

        if (!response.ok) {
          throw new Error(`HTTP error. Status: ${response.status}`);
        }

        const data = await response.json();

        if (data.restaurant) {
          console.log('Restaurant Data:', data.restaurant);
          console.log('Menu Data:', data.menu);

          // You can update your UI with the restaurant and menu data here.
        } else {
          console.error('Error fetching menu data:', data.error);
        }
      } catch (error) {
        console.error('Error fetching menu:', error);
      }
    },
  },

  mounted() {
    fetch('/api/location_select', {method: 'POST', headers: {'Content-Type': 'application/json',}, body: JSON.stringify({ defaultRequest: true})})
      .then((response) => response.json())
      .then((data) => {
        if (data.status === 'success') {
          this.handleMarkerSelection(data.selected_marker);
        }
      })
      .catch((error) => {
        console.error('Error fetching marker data:', error);
      });
    console.log('Restaurant ID:', this.restaurantId);
  },
};
</script>

<style scoped>
.nav-button {
  padding: 12px 20px;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.next-button {
  background-color: #db79cf;
  color: white;
  border: 1px solid #bb4da5;
}

.next-button:hover {
  background-color: #bb4da5;
}

.next-button:disabled {
  background-color: #cccccc;
  border-color: #bbbbbb;
  cursor: not-allowed;
}

h1 {
  font-size: xx-large;
  text-align: center;
  padding-top: 2%;
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
.map_wrapper {
  display: flex;
  justify-self: center;
  border-width: 1rem; 
  border-radius: 5%;
  border-color: #f27e9f; 
  width: 800px;
  height: 550px;
  overflow: hidden;
  align-items: center;
}
.map_container div {
  width: 100%; 
  height: 100%; 
  position: relative;
  position: absolute
}
.error-message {
  color: red;
  font-weight: bold;
  display:flex;
  justify-content: center;
  font-size: large;
}

</style>
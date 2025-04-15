<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import L from 'leaflet';
import { api } from '@/api/auth.js'; 
import { Icon } from '@iconify/vue';
import 'leaflet/dist/leaflet.css';

const props = defineProps({
  restaurantId: String,
});

const zipEntered = ref('06825');
const errorMessage = ref(null);
const selectedMarker = ref(null);
const mapContainer = ref(null);
const markers = ref([]);
const map = ref(null);
const restaurants = ref([]);

const router = useRouter();

function createCustomMarker(lat, lng, colorClass = 'text-green-700') {
  const html = `
    <div class="w-[50px] h-[50px] flex items-center justify-center drop-shadow-lg ${colorClass}">
      <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 24 24" fill="currentColor">
        <circle cx="12" cy="9" r="2.5" fill="white" />
        <path d="M12 11.5A2.5 2.5 0 0 1 9.5 9A2.5 2.5 0 0 1 12 6.5A2.5 2.5 0 0 1 14.5 9a2.5 2.5 0 0 1-2.5 2.5M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7"/>
      </svg>
    </div>
  `;

  return L.marker([lat, lng], {
    icon: L.divIcon({
      html,
      className: '',
      iconSize: [50, 50],
      iconAnchor: [25, 50],
    }),
  });
}

const generateMap = async () => {
  if (!zipEntered.value) {
    alert('Please enter a zip code.');
    return;
  }

  try {
    errorMessage.value = null;
    const response = await await api.post('/location', {
      zip_code: zipEntered.value,
    });
    const data = response.data;

    if (Array.isArray(data) && data.length > 0) {
      restaurants.value = data;
      const first = data[0];
      if (map.value) {
        map.value.remove();
        markers.value = [];
      }

      map.value = L.map(mapContainer.value).setView([first.latitude, first.longitude], 12);
      L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://carto.com/">Carto</a>',
        subdomains: 'abcd',
        maxZoom: 19,
      }).addTo(map.value);

      map.value.invalidateSize();

      data.forEach((restaurant) => {
        const marker = createCustomMarker(restaurant.latitude, restaurant.longitude, 'text-green-700')
          .addTo(map.value)
          .bindPopup(`<b>${restaurant.name}</b><br>${restaurant.address}`)
          .on('click', () => {
            handleMarkerSelection(restaurant);
          });

        markers.value.push(marker);
      });
    } else {
      errorMessage.value = data.error || 'Error generating map.';
    }
  } catch (err) {
    errorMessage.value = 'Error generating map.';
    console.error(err);
  }
};

const handleMarkerSelection = async (markerData) => {
  try {
    const res = await api.post('/location_select', markerData);
    const result = res.data;

    if (result.status === 'success') {
      selectedMarker.value = result.selected_marker;
    } else {
      console.error('Error:', result.error);
    }
  } catch (e) {
    console.error('Error sending marker data:', e);
  }
};

const confirmSelection = () => {
  if (selectedMarker.value) {
    router.push(`/menu/${selectedMarker.value.id}`);
  }
};

onMounted(async () => {
  // set default map
  // zipEntered.value = '06825';
  await generateMap();

  try {
    const res = await api.post('/location_select', { defaultRequest: true });
    const data = res.data;
    if (data.status === 'success') {
      await handleMarkerSelection(data.selected_marker);
    } 
  } catch (error) {
    console.error('Error fetching default marker:', error);
  }
  console.log('Restaurant ID:', props.restaurantId);
});
</script>

<template>
  <div class="p-6 flex flex-col md:flex-row gap-6">
    <div class="w-full md:w-2/3 xl:w-1/2">
      <h2 class="text-lg font-semibold mb-4">Pick nearby restaurant</h2>

      <form @submit.prevent="generateMap" class="mb-4">
        <div class="flex items-center !bg-white border border-green-700 rounded-full h-11 flex-grow w-full ">
          <Icon icon="mdi:map-marker-outline" class="w-5 h-5 text-green-700 flex-shrink-0 ml-3" />
          <input type="text" id="zip" v-model="zipEntered" placeholder="Enter zip code..." required class="flex-grow bg-transparent border-none placeholder-neutral-400 focus:ring-0 focus:outline-none text-neutral-700 w-full p-2" />
          <Icon v-if="zipEntered" icon="mdi:close" @click="zipEntered = ''" class="w-5 h-5 text-green-700 cursor-pointer mr-2 transition"/>
          <button type="submit" class="group p-1.5 rounded-full hover:bg-rose-50 transition duration-200 mr-2">
            <Icon icon="mdi:chevron-double-right" class="w-5 h-5 text-green-700 group-hover:text-rose-400" />
          </button>
        </div>
      </form>

      <div v-if="errorMessage" class="text-rose-600 font-semibold mb-4">{{ errorMessage }}</div>

      <div class="border-none rounded-xl shadow-md overflow-hidden w-full h-[450px] mb-6">
        <div ref="mapContainer" class="w-full h-full relative"></div>
      </div>
    </div>

    <!-- right sidebar -->
    <div class="w-full md:w-1/3 xl:w-1/2 overflow-y-auto space-y-4">
      <div class="grid grid-cols-1 xl:grid-cols-2 gap-4">
        <div
          v-for="restaurant in restaurants"
          :key="restaurant.id"
          class="p-4 border rounded-xl shadow-md transition cursor-pointer w-full "
          :class="selectedMarker?.id === restaurant.id ? 'border-green-600 bg-green-50' : 'border-neutral-200'"
          @click="handleMarkerSelection(restaurant)"
        >
          <h3 class="font-semibold text-md text-green-700">{{ restaurant.name }}</h3>
          <p class="text-sm text-neutral-600">{{ restaurant.address }}</p>
        </div>
      </div>
      <button
        v-if="selectedMarker"
        @click="confirmSelection"
        :disabled="!selectedMarker"
        class="px-4 bg-white text-green-700 h-11 rounded-full text-md border border-green-700 hover:bg-green-700 hover:text-white disabled:bg-neutral-400 disabled:cursor-not-allowed"
      >
        Choose This Restaurant
      </button>
      <div v-else class="text-left text-neutral-600">
        No marker selected yet.
      </div>
    </div>

  </div>
</template>

<style scoped>
/* Leaflet styles override */
.leaflet-container {
  width: 100%;
  height: 100%;
}
</style>
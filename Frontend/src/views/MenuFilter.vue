<script setup>
import Card from '@/components/Steps_Bottom.vue';
import { Icon } from '@iconify/vue';
import { useRouter, useRoute } from 'vue-router';
import { ref, computed, onMounted } from "vue";
import { api, authApi } from '@/api/auth.js';
import axios from "axios";
import { svg } from 'leaflet';
import { userAllergies, fetchUserAllergies } from '@/composables/useUserAllergies.js';

const router = useRouter();
const route = useRoute(); // To access route parameters

// make reactive variables for the selected restaurant and menu
const restaurant = ref({ name: "", address: "", phone: "", category: "", price_range:"", status: "", hours: "{}", image:""});
const menu = ref([]);

// Function to fetch menu data for the selected restaurant
const fetchMenu = async (restaurantId) => {
  try {
    console.log("Fetching menu data for restaurant:", restaurantId);
    const response = await api.get(`/menu/${restaurantId}`);
    console.log("API Response:", response.data);

    restaurant.value = response.data.restaurant;
    menu.value = response.data.menu;
  } catch (error) {
    console.error("Error fetching menu:", error);
  }
};  

// When the component is mounted, fetch the restaurant's menu based on the ID from the URL
onMounted(() => {
  const restaurantId = route.params.restaurantId; // Get the restaurantId from the URL
  if (restaurantId) {
    fetchMenu(restaurantId); // Fetch the menu for the restaurant
  } else {
    console.error("No restaurant ID found in the URL");
  }
});

// menu filtering by search and user allergies
const searchQuery = ref("");
const allergyFilterOn = ref(true); 

const toggleAllergyFilter = () => {
  allergyFilterOn.value = !allergyFilterOn.value;
};

const filteredMenu = computed(() => {
  if (!menu.value) return [];
  const userAllergenNames = userAllergies.value.map(a => a.name);

  return menu.value.filter((item) => {
    const matchesName = item.name.toLowerCase().includes(searchQuery.value.toLowerCase());
    const hasAllergies = userAllergenNames.length > 0
      ? item.allergens.some(allergenName => userAllergenNames.includes(allergenName))
      : false;
    return matchesName && (!allergyFilterOn.value || !hasAllergies);
  });
});

const categories = computed(() => {
  const categorySet = new Set(filteredMenu.value.map(item => item.category));
  return Array.from(categorySet);
});
const menuByCategory = (category) => {
  return filteredMenu.value.filter(item => item.category === category);
};

const scrollToCategory = (category) => {
  const element = document.getElementById(`category-${category}`);
  if (element) {
    element.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

// codes used for searching functionality
const searchIndex = ref(0);
const highlightRow = ref(0);
const searchNext = () => {
  if (searchIndex.value < filteredMenu.value.length - 1) {
    searchIndex.value++;
  } else {
    searchIndex.value = 0; 
  }
  highlightRow.value = searchIndex.value;
};
const searchPrev = () => {
  if (searchIndex.value > 0) {
    searchIndex.value--;
  } else {
    searchIndex.value = filteredMenu.value.length - 1;
  }
  highlightRow.value = searchIndex.value;
};
const clearSearch = () => {
  searchQuery.value = "";
};

// functions to parse and display restaurant hours
const hours = ref(null);
const showHours = ref(false);
const today = new Date().toLocaleString("en-US", { weekday: "long" });
// parse hours from JSON string
const parsedHours = computed(() => {
  try {
    return JSON.parse(restaurant.value.hours || "{}");

  } catch (error) {
    console.error("❌ Error parsing hours:", error);
    return {};
  }
});
// switch to show/hide hours
const toggleHours = () => {
  showHours.value = !showHours.value;
};
// sort hours by day of the week
const sortedHours = computed(() => {
  const weekOrder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

  return Object.entries(parsedHours.value ?? {}).sort(
    (a, b) => weekOrder.indexOf(a[0]) - weekOrder.indexOf(b[0])
  );
});
const formattedPhone = computed(() => {
  if (!restaurant.value.phone) return "";
  return restaurant.value.phone.replace(/(\d{3})(\d{3})(\d{4})$/, "($1) $2-$3");
});

const selectedItem = ref(null); // selected menu item for modal
const selectedOptions = ref({});

// open modal for item with options
const openModal = (item) => {
  selectedItem.value = item;
  selectedOptions.value = {}; // reset options
};

// close modal
const closeModal = () => {
  selectedItem.value = null;
};

// add to order (change later)
const addToOrder = () => {
  console.log("Order added:", {
    item: selectedItem.value.name,
    options: selectedOptions.value,
  });
  closeModal();
};

const onInput = () => {
  console.log("Searching for:", searchQuery.value);
};

// proceed to checkout when button is clicked
const proceedToCheckout = () => {
  router.push("/order");
};
</script>

<template>
  <div class="flex flex-col md:flex-row justify-between gap-0 p-3 bg-neutral-50">
    <!-- Left Column (hidden in phone screen) -->
    <div class="w-full md:w-1/3 lg:w-1/4">
      <div class="bg-white rounded-xl shadow-md m-3 overflow-hidden">
        <img v-if="restaurant.image" :src="restaurant.image" alt="Restaurant Image" class="w-full h-40 object-cover" />
        <div class="p-3 text-green-700">
          <h1  class="text-lg font-bold">{{ restaurant.name }}</h1>
          <div class="text-sm text-neutral-500 flex items-center space-x-2">
            <span v-if="restaurant.address" > {{ restaurant.price_range }} </span>
            <span v-if="restaurant.address && restaurant.category" > • </span>
            <span v-if="restaurant.category" > {{ restaurant.category }} </span>
          </div>

          <!-- Address -->
          <div class="flex items-center space-x-2 mt-2">
            <Icon v-if="restaurant.address" icon="mdi:map-marker-outline" class="w-5 h-5 text-green-700 mr-1" />
            <span>{{ restaurant.address }}</span>
          </div>

          <!-- Hours -->
          <div v-if="restaurant.status" class="flex items-center space-x-2 mt-2 cursor-pointer" @click="toggleHours">
            <Icon icon="mdi:clock-outline" class="w-5 h-5 text-green-700 mr-1" />
            <span>{{ restaurant.status }}</span>

            <!-- switch arrows -->
            <Icon v-if="!showHours" icon="mdi:keyboard-arrow-down" class="w-5 h-5 text-green-700 ml-auto" />
            <Icon v-else icon="mdi:keyboard-arrow-up" class="w-5 h-5 text-green-700 ml-auto" />
          </div>

          <!-- table of opening hours -->
          <div v-if="showHours" class="mt-2 ml-8">
            <table class="w-full text-xs">
              <tbody>
                <tr v-for="([day, time]) in sortedHours" :key="day" :class="{ 'font-bold': day === today }">
                  <td class="pr-2 w-1/3">{{ day }}</td>
                  <td>{{ time }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Phone -->
          <div v-if="restaurant.phone" class="flex items-center space-x-2 mt-2">
            <Icon icon="mdi:phone-outline" class="w-5 h-5 text-green-700 mr-1" />
            <a :href="`tel:${restaurant.phone}`" class="underline">{{ formattedPhone }}</a>
          </div>
        </div>
      </div>
      
      <!-- Menu Categories -->
      <div class="hidden md:block p-6 sticky top-12 z-10">
        <h2  class="text-lg font-bold p-2">Menu</h2>
        <ul>
          <!-- <hr class="border-neutral-500"/> -->
          <li v-for="category in categories" :key="category" class="px-2 py-1 text-neutral-700 cursor-pointer hover:bg-rose-100" @click="scrollToCategory(category)">
            {{ category }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Center Column (full width in phones) -->
    <div class="w-full md:w-2/3 lg:w-1/2">
      <!-- Search & Allergy Filter Container -->
      <div class="sticky top-20 z-40 flex justify-center items-center w-full mx-auto gap-3 p-3">
        <!--  Search Box -->
        <div class="flex items-center !bg-white border-1 border-green-700 rounded-full p-1 flex-grow w-full ">
          <Icon icon="mdi:magnify" class="w-5 h-5 text-green-700 m-2 flex-shrink-0" />
          <input type="text" id="menu-search" v-model="searchQuery" placeholder="Search menu..." @input="onInput" class="flex-grow bg-transparent border-none placeholder-neutral-400 focus:outline-none text-neutral-700 w-full" />
          <span v-if="searchQuery && filteredMenu.length" class="mr-2 text-green-700 ">{{ searchIndex + 1 }}/{{ filteredMenu?.length || 0 }}</span>
          <Icon v-if="searchQuery" icon="mdi:keyboard-arrow-up" @click="searchPrev" class="w-5 h-5 text-green-700 mr-2 flex-shrink-0" />
          <Icon v-if="searchQuery" icon="mdi:keyboard-arrow-down" @click="searchNext" class="w-5 h-5 text-green-700 mr-2 flex-shrink-0" />
          <Icon v-if="searchQuery" icon="mdi:close" @click="clearSearch" class="w-5 h-5 text-green-700 mr-2 cursor-pointer flex-shrink-0" />
        </div>

        <!-- Allergy Filter ON/OFF Button-->
        <button @click="toggleAllergyFilter" class="flex items-center p-1 md:w-48 rounded-full border-1 flex-shrink-0 " :class="{'bg-rose-50 text-rose-400 border-rose-400': allergyFilterOn, 'bg-neutral-50 text-neutral-400 border-neutral-400': !allergyFilterOn}">
          <Icon icon="mdi:food-allergy" class="w-5 h-5 m-2 flex-shrink-0" />
          <span class="hidden md:block">Allergy Filter: {{ allergyFilterOn ? 'ON' : 'OFF' }}</span>
        </button>
      </div>

      <!-- Menu List -->
      <span v-if="!filteredMenu.length" class="m-3 text-sm text-neutral-500">No menu found</span>
      <div v-for="category in categories" :key="category" :id="'category-' + category" class="pb-3">
        <h2 class="mx-3 text-xl">{{ category }}</h2>
        <div class="bg-white m-3 rounded-xl shadow-md overflow-hidden">
          <ul>
            <li v-for="(item, index) in menuByCategory(category)" :key="item.id" class="relative">
              <hr v-if="index !== 0" class="border-neutral-500"/>
              <div class="p-3">
                <!-- padding text if image is available -->
                <div :class="{'pr-32': item.image, 'pr-10': !item.image}" class="flex-1">
                  <p class="font-bold truncate">{{ item.name }}</p>
                  <p class="text-neutral-600">${{ item.price.toFixed(2) }}</p>
                  <p v-if="item.ingredients" class="text-sm text-neutral-500 truncate">{{ item.ingredients.join(", ") }}</p>
                  <p v-if="item.description" class="text-sm text-neutral-500 truncate">{{ item.description }}</p>
                  <p v-if="item.allergens.length" class="flex items-center text-sm text-rose-400 truncate">
                    <Icon icon="mdi:food-allergy" class="w-4 h-4 mr-1" />
                    {{ item.allergens.join(", ") }}
                  </p>
                </div>

                <!-- show image if available -->
                <img v-if="item.image" :src="item.image" :alt="item.name"
                  class="w-32 h-full object-cover absolute right-0 top-0 transform "/>

                <!-- show modal if the item has options -->
                <button v-if="Object.keys(item.options).length" @click="openModal(item)" class="group rounded-full text-green-700 shadow-md bg-white hover:!bg-green-700 absolute right-3 bottom-3">
                  <Icon icon="mdi:plus" class="w-5 h-5 text-green-700 group-hover:text-white m-2" />
                </button>

                <button v-else class="group rounded-full text-green-700 hover:bg-green-700 shadow-md absolute right-3 bottom-3">
                  <Icon icon="mdi:plus" class="w-5 h-5 group-hover:text-white m-2" />
                </button>
              </div>

            </li>
          </ul>
        </div>
      </div>

      <!-- Click outside to close -->
      <div v-if="selectedItem" class="z-[9999] fixed inset-0 bg-neutral-700 bg-opacity-50 flex items-center justify-center" @click.self="closeModal">
        <!-- Modal body (scrollable) -->
        <div class="relative p-4 m-4 bg-white rounded-xl shadow-md w-96 max-h-[80vh] flex flex-col overflow-hidden">
          
          <!-- Menu name (fixed at the top) -->
          <div class="sticky top-0 bg-white pb-4">
            <h2 class="text-lg font-bold text-center">{{ selectedItem?.name }}</h2>
          </div>

          <!-- Option selection (scrollable) -->
          <div class="flex-1 overflow-y-auto">
            <p class="text-center text-neutral-600 mb-2">Select your options:</p>
            <div v-for="(options, groupName) in selectedItem?.options" :key="groupName" class="mb-4">
              <strong class="text-sm font-semibold">{{ groupName }}</strong>
              <ul class="mt-2 space-y-2">
                <li v-for="option in options" :key="option.name" class="flex items-center space-x-2">
                  <input type="radio" :name="groupName" :value="option.name" v-model="selectedOptions[groupName]" class="form-radio text-green-700" />
                  <span>{{ option.name }} (+${{ option.extra_price.toFixed(2) }})</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Buttons (fized at the bottom) -->
          <div class="sticky bottom-0 bg-white pt-4 flex justify-end space-x-2">
            <button @click="closeModal" class="px-4 py-2 bg-gray-300 rounded-md hover:bg-gray-400 transition">Cancel</button>
            <button @click="addToOrder" class="px-4 py-2 bg-green-700 text-white rounded-md hover:bg-green-800 transition">Add to Order</button>
          </div>

        </div>
      </div>

    </div>

    <!-- Right Column (hidden in phone screen) -->
    <div class="hidden lg:block w-1/4">
      <div class="bg-white p-3 rounded-xl shadow-md m-3">
        <h3>My order</h3>
        <p>Items: 0</p>
        <p>Total: $0.00</p>
        <button @click="proceedToCheckout" class="border-1 border-green-700 w-auto text-center rounded-xl hover:bg-green-700 hover:text-white transition m-2 p-2">Proceed to checkout</button>
      </div>
    </div>
  </div>
  <Card></Card>
</template>
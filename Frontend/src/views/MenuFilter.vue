<script setup>
import Card from '@/components/Steps_Bottom.vue';
import { useRouter } from 'vue-router';
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import { svg } from 'leaflet';

const router = useRouter();

// make reactive variables for the selected restaurant and menu
const restaurant = ref({ name: "", address: "", phone: "", category: "", price_range:"", status: "", hours: "{}", image:""});
const menu = ref([]);
const showHours = ref(false);
const today = computed(() => {
  return new Date().toLocaleDateString("en-US", { weekday: "long" });
});
const formattedPhone = computed(() => {
  if (!restaurant.value.phone) return "";
  return restaurant.value.phone.replace(/(\+\d)(\d{3})(\d{3})(\d{4})/, "$1 ($2) $3-$4");
});
const categories = computed(() => {
  const categorySet = new Set(menu.value.map(item => item.category));
  return Array.from(categorySet);
});
const menuByCategory = (category) => {
  return menu.value.filter(item => item.category === category);
};

// function to fetch menu data from the Flask API
const fetchMenu = async () => {
  try {
    console.log("📡 Fetching menu data from Flask...");
    const response = await axios.get("http://127.0.0.1:5000/api/menu");
    console.log("✅ API Response:", response.data);

    // API から取得したデータを Vue の状態に格納
    restaurant.value = response.data.restaurant;
    menu.value = response.data.menu;
  } catch (error) {
    console.error("❌ Error fetching menu:", error);
  }
};

const searchQuery = ref("");

const filteredMenu = computed(() => {
  if (!searchQuery.value) return menu.value; // 空なら全メニュー表示
  return menu.value.filter((item) =>
    item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const selectedItem = ref(null); // 選択されたメニュー
const selectedOptions = ref({});

// 📌 モーダルを開く
const openModal = (item) => {
  selectedItem.value = item;
  selectedOptions.value = {}; // オプションの選択をリセット
};

// 📌 モーダルを閉じる
const closeModal = () => {
  selectedItem.value = null;
};

// 📌 オーダーに追加（仮の処理）
const addToOrder = () => {
  console.log("Order added:", {
    item: selectedItem.value.name,
    options: selectedOptions.value,
  });
  closeModal();
};

const clearSearch = () => {
  searchQuery.value = "";
};

const onInput = () => {
  console.log("Searching for:", searchQuery.value);
};

const parsedHours = computed(() => {
  try {
    return JSON.parse(restaurant.value.hours) || {};
  } catch (error) {
    console.error("❌ Error parsing hours:", error);
    return {};
  }
});

// switch to show/hide hours
const toggleHours = () => {
  showHours.value = !showHours.value;
};

const proceedToCheckout = () => {
  router.push("/order"); // クリック時に /order に遷移
};
// Vue インスタンスのマウント時にデータを取得
onMounted(fetchMenu);
</script>

<template>
  <div class="flex justify-between gap-0 p-3 bg-rose-50 mb-16">
    <!-- 📌 Left Column -->
    <div class="w-1/4">
      <div class="bg-white rounded-xl shadow-md m-3">
        <img v-if="restaurant.image" :src="restaurant.image" alt="Restaurant Image" class="w-full h-auto rounded-t-xl" />
        <div class="p-3 text-green-700">
          <h1  class="text-lg font-bold">{{ restaurant.name }}</h1>
          <div class="text-sm text-neutral-500">{{ restaurant.price_range }} • {{ restaurant.category }}</div>

          <!-- 📍 Address -->
          <div class="flex items-center space-x-2 mt-2">
            <svg viewBox="0 0 24 24" fill="none" class="w-5 h-5 stroke-[0.1] stroke-green-700 fill-green-700 mr-1">
              <title>Location Icon</title>
              <path fill-rule="evenodd" clip-rule="evenodd" d="M12 1c2.4 0 4.9.9 6.7 2.8 3.7 3.7 3.7 9.8 0 13.4L12 24l-6.7-6.7c-3.7-3.7-3.7-9.8 0-13.5C7.1 1.9 9.6 1 12 1Zm0 18.8 4.6-4.6c2.5-2.6 2.5-6.7 0-9.3C15.4 4.7 13.7 4 12 4c-1.7 0-3.4.7-4.6 1.9-2.5 2.6-2.5 6.7 0 9.3l4.6 4.6Zm2-9.3a2 2 0 1 1-4 0 2 2 0 0 1 4 0Z"></path>
            </svg>
            <span>{{ restaurant.address }}</span>
          </div>

          <!-- 🕒 Hours -->
          <div class="flex items-center space-x-2 mt-2 cursor-pointer" @click="toggleHours">
            <svg viewBox="0 0 24 24" fill="none" class="w-5 h-5 stroke-[0.1] stroke-green-700 fill-green-700 mr-1">
              <title>Clock Icon</title>
              <path fill-rule="evenodd" clip-rule="evenodd" d="M1 12C1 5.9 5.9 1 12 1s11 4.9 11 11-4.9 11-11 11S1 18.1 1 12Zm3 0c0 4.4 3.6 8 8 8s8-3.6 8-8-3.6-8-8-8-8 3.6-8 8Zm6.5 2.5V7h3v4.5H17v3h-6.5Z"></path>
            </svg>
            <span>{{ restaurant.status }}</span>

            <!-- switch ▼ / ▲ -->
            <svg v-if="!showHours" viewBox="0 0 24 24" fill="none" class="w-5 h-5 stroke-[0.1] stroke-green-700 fill-green-700 ml-auto">
              <title>Down Arrow Icon</title>
              <path d="M18 8v3.8l-6 4.6-6-4.6V8l6 4.6L18 8Z"></path>
            </svg>
            <svg v-if="showHours" viewBox="0 0 24 24" fill="none" class="w-5 h-5 stroke-[0.1] stroke-green-700 fill-green-700 ml-auto">
              <title>Up Arrow Icon</title>
              <path d="M18 16V12.2l-6-4.6-6 4.6V16l6-4.6 6 4.6Z"></path>
            </svg>
          </div>

          <!-- table of opening hours -->
          <div v-if="showHours" class="mt-2 ml-8">
            <table class="w-full text-xs">
              <tbody>
                <tr v-for="(time, day) in parsedHours" :key="day" :class="{ 'font-bold': day === today }">
                  <td class="pr-2 w-1/3">{{ day }}</td>
                  <td>{{ time }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 📞 Phone -->
          <div class="mt-2">
            <a :href="`tel:${restaurant.phone}`" class="underline">{{ formattedPhone }}</a>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-md m-3 p-3">
        <h2  class="text-lg font-bold">Menu</h2>
        <ul class="space-y-2 mt-2">
          <hr class="my-2 border-neutral-500"/>
          <li v-for="category in categories" :key="category" class="text-gray-700">{{ category }}</li>
        </ul>
      </div>
    </div>

    <!-- 📌 Center Column -->
    <div class="w-1/2">
      <!-- 🔍 Search Box -->
      <div class="flex items-center bg-white border-1 border-green-700 rounded-full p-1 w-80 mx-auto m-3">
        <svg viewBox="0 0 24 24" fill="none"class="w-5 h-5 stroke-[0.1] stroke-green-700 fill-green-700 m-2">
          <title>Search Icon</title>
          <path d="M22.6 20.4 18.2 16c1.1-1.6 1.8-3.5 1.8-5.6C20 5.2 15.7.9 10.5.9S1 5.2 1 10.4s4.3 9.5 9.5 9.5c2.1 0 4-.7 5.6-1.8l4.4 4.4 2.1-2.1ZM4 10.5C4 6.9 6.9 4 10.5 4S17 6.9 17 10.5 14.1 17 10.5 17 4 14.1 4 10.5Z"></path>
        </svg>
        <input type="text" v-model="searchQuery" placeholder="Search menu..." @input="onInput" class="flex-1 border-none focus:outline-none text-gray-700 ml-2" />
        <svg v-if="searchQuery" viewBox="0 0 24 24" role="button" tabindex="0" @click="clearSearch" @keydown.enter="clearSearch" class="w-4 h-4 cursor-pointer focus:outline-none stroke-[0.1] stroke-green-700 fill-green-700 m-2" >
          <title>Clear Button</title>
          <path d="M12 1C5.9 1 1 5.9 1 12s4.9 11 11 11 11-4.9 11-11S18.1 1 12 1Zm6 15-2 2-4-4-4 4-2-2 4-4-4-4 2-2 4 4 4-4 2 2-4 4 4 4Z"></path>
        </svg>
      </div>

      <!-- 🥗 Menu List -->
      <div v-for="category in categories" :key="category" class="bg-white p-3 m-3 rounded-xl shadow-md ">
        <h2>{{ category }}</h2>
        <ul class="mt-2 space-y-2">
          <li v-for="item in menuByCategory(category)" :key="item.id" class="relative">
            <hr class="my-2 border-neutral-500"/>
            <p class="font-bold">{{ item.name }}</p>
            <p class="text-neutral-600">${{ item.price.toFixed(2) }}</p>
            <p v-if="item.ingredients" class="text-sm text-neutral-500">{{ item.ingredients.join(", ") }}</p>
            <p v-if="item.description" class="text-sm text-neutral-500">{{ item.description }}</p>
            <p v-if="item.allergens.length">Allergens: {{ item.allergens.join(", ") }}</p>

            <!-- show button if the item has options -->
            <button v-if="Object.keys(item.options).length" @click="openModal(item)" class="group rounded-full text-green-700 hover:bg-green-700 shadow-md absolute right-0 bottom-0">
              <svg viewBox="0 0 24 24" fill="none" class="w-5 h-5 stroke-[0.1] stroke-green-700 fill-green-700 group-hover:fill-white m-2">
                <title>Plus Icon</title>
                <path d="M19 10.5h-5.5V5h-3v5.5H5v3h5.5V19h3v-5.5H19v-3Z"></path>
              </svg>
            </button>
          </li>
        </ul>
      </div>

      <!-- 📌 Modal -->
      <t-modal v-if="selectedItem" v-model="selectedItem" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
        <div class="p-4 m-4 bg-white rounded-xl shadow-md">
          <h2 class="text-lg font-bold text-center mb-4">{{ selectedItem?.name }}</h2>
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

          <div class="flex justify-end space-x-2">
            <button @click="closeModal" class="px-4 py-2 bg-gray-300 rounded-md hover:bg-gray-400 transition">Cancel</button>
            <button @click="addToOrder" class="px-4 py-2 bg-green-700 text-white rounded-md hover:bg-green-800 transition">Add to Order</button>
          </div>
        </div>
      </t-modal>
    </div>

    <div class="w-1/4">
      <div class="bg-white p-3 rounded-xl shadow-md m-3">
        Put allergy list here<br />
        Expand upon click
      </div>
      <div class="bg-white p-3 rounded-xl shadow-md m-3">
        <h3>Your order</h3>
        <p>Items: 0</p>
        <p>Total: $0.00</p>
        <button @click="proceedToCheckout" class="border-1 border-green-700 w-auto place-items-center rounded-xl hover:bg-green-700 hover:text-white transition m-3 p-3">Proceed to checkout</button>
      </div>
    </div>
  </div>
  <Card></Card>
</template>
<script setup>
import axios from 'axios';
import { Icon } from '@iconify/vue';
import { useRouter, useRoute } from 'vue-router';
import { ref, onUpdated, computed, onMounted, watch } from "vue";
import { api, authApi } from "@/api/auth.js";
import { addUserCartItem, updateUserCartItem, deleteUserCartItem, userCart, fetchUserCart } from '@/composables/useUserCart.js';

const router = useRouter();
const route = useRoute();


const createAccount = () => {
  router.push('/create'); 
};

const cancelOrder = () => {
  router.push('/menu'); 
}

const cardNumber = ref('****-****-****-****');
const expiryDate = ref('**/**');
const cvv = ref('***');
const paymentMessage = ref('');

const processPayment = () => {
  paymentMessage.value = "payment processed!";
}
const props = defineProps({
  restaurantId: {
    type: String,
    required: false, // ← optional
  },
});
const restaurantId = computed(() => route.params.restaurantId || '1');
// add item to order
const addItem = async (item) => {
  try {
    if (!item.quantity) {
      const newItem = await addUserCartItem({
          menu_item_id: item.id,
          quantity: 1,
          options: [],
          restaurant_id: restaurantId.value
        });
        item.quantity = 1;
        item.cart_item_id = newItem.cart_item_id;
        await fetchUserCart(restaurantId.value);
        cartItems.value = userCart.value;  
    } else if (item.quantity < 10) {
      item.quantity++
      await updateUserCartItem(item.cart_item_id, item.quantity, []);
      await fetchUserCart(restaurantId.value);
      cartItems.value = userCart.value;  
    } else {
      // when quantity reaches maximum
      alert("Maximum quantity reached");
      item.quantity = 10
    }
  } catch (err) {
    console.error("❌ Failed to add item:", err);
  }
}
// Decrease quantity or remove item from cart
const removeItem = async (item) => {
  try {
    if (item.quantity > 1) {
      item.quantity--;
      await updateUserCartItem(item.cart_item_id, item.quantity, []);
      await fetchUserCart(restaurantId.value);
      cartItems.value = userCart.value;  
    } else {
      await deleteUserCartItem(item.cart_item_id);
      item.quantity = 0;
      item.cart_item_id = null;
      await fetchUserCart(restaurantId.value);
      cartItems.value = userCart.value;  
    }
  } catch (err) {
    console.error("❌ Failed to remove item:", err);
  }
}

// Add item with options via modal
const addItemWithOptions = async () => {
  try {
    const formattedOptions = [];
    for (const groupId in selectedOptions.value) {
      const opt = selectedOptions.value[groupId];
      if (Array.isArray(opt)) {
        opt.forEach(id => formattedOptions.push({ option_item_id: id }));
      } else {
        formattedOptions.push({ option_item_id: opt });
      }
    }

    const newItem = await addUserCartItem({
      menu_item_id: selectedItem.value.id,
      quantity: 1,
      options: formattedOptions,
      restaurant_id: restaurantId.value
    });

    selectedItem.value.quantity = 1;
    selectedItem.value.cart_item_id = newItem.cart_item_id;
    await fetchUserCart(restaurantId.value);
    cartItems.value = userCart.value;  
    closeModal();
  } catch (err) {
    console.error("❌ Failed to add to order:", err);
  }
};

const cartItems = ref([]);
onMounted(async () => {
  try {
    const response = await authApi.get(`/user/cart/${restaurantId.value}`);
    cartItems.value = response.data.cart_items;
  } catch (err) {
    console.error("❌ Failed to load cart:", err);
  }
});

// calculate total amount
const totalAmount = computed(() => {
  return cartItems.value.reduce((total, item) => {
    const base = item.menu_item_price * item.quantity;
    const extras = item.options.reduce((sum, opt) => sum + (opt.extra_price || 0), 0) * item.quantity;
    return total + base + extras;
  }, 0);
});

/** ref: ChatGPT. placeholder script 
const orderItems = ref([
  {},
]);
 price
const totalPrice = computed(() => {
  return orderItems.value.reduce(
    (total, item) => total + item.price * item.quantity,
    0
  );
});*/
</script>

<template>

  <div class="px-10 py-5">
    <h1 class="text-center text-xl text-green-700 font-bold p-3 pb-0">Place your order</h1>
    <ul >
      <li
        v-for="item in cartItems"
        :key="item.cart_item_id"
        class="border-b p-3"
      >
        <!-- menu name and price in the same line -->
        <div class="flex items-center gap-x-2">
          <span class="flex-1 break-words">
            {{ item.menu_item_name }}
          </span>
          <span class="w-[60px] flex-shrink-0 text-left whitespace-nowrap">
            $ {{ item.menu_item_price.toFixed(2) }}
          </span>
        </div>

        <ul v-if="item.options.length" class="mt-1 pl-4">
          <li
            v-for="opt in item.options"
            :key="opt.id"
            class="flex items-center gap-x-2 text-sm text-neutral-500"
          >
            <span class="flex-1 break-words">
              {{ opt.description }}: {{ opt.name }}
            </span>
            <span
              v-if="opt.extra_price > 0"
              class="w-[60px] flex-shrink-0 text-left whitespace-nowrap"
            >
              + $ {{ opt.extra_price.toFixed(2) }}
            </span>
          </li>
        </ul>

        <!-- quantity control here -->
        <div class="mt-2 pl-4">
          <!-- when quantity = 1 -->
          <div
            v-if="item.quantity === 1"
            class="flex items-center justify-center text-green-700 bg-white rounded-full shadow-md w-24"
          >
            <button @click="removeItem(item)">
              <Icon icon="mdi:trash-can-outline" class="w-5 h-5" />
            </button>
            <span class="text-center">{{ item.quantity }}</span>
            <button @click="addItem(item)" class="text-green-700">
              <Icon icon="mdi:plus" class="w-5 h-5 " />
            </button>
          </div>

          <!-- when quantity ≥ 2 -->
          <div
            v-else
            class="flex items-center justify-center bg-white text-green-700 rounded-full shadow-md w-24"
          >
            <button @click="removeItem(item)">
              <Icon icon="mdi:minus" class="w-5 h-5" />
            </button>
            <span class="text-center">{{ item.quantity }}</span>
            <button @click="addItem(item)">
              <Icon icon="mdi:plus" class="w-5 h-5" />
            </button>
          </div>
        </div>
      </li>
    </ul>

    <!-- total -->
    <div class="flex items-center font-bold mt-4 p-3 text-green-700">
      <span class="flex-1">
        Subtotal ({{ cartItems.reduce((sum, i) => sum + i.quantity, 0) }} {{ cartItems.reduce((sum, i) => sum + i.quantity, 0) === 1 ? 'item' : 'items' }})
      </span>
      <span class="w-[60px] flex-shrink-0 text-left whitespace-nowrap">
        $ {{ totalAmount.toFixed(2) }}
      </span>
    </div>
  </div>
    

    <div class="payment-section">
      <h2 style="font-size: larger; font-weight: bold;">Payment Information</h2>

        <div class="card-details">
          <label for="cardNumber">Card Number</label>
          <p>{{ cardNumber }}</p>
          <label for="expiryDate">Expiry Date</label>
          <p>{{ expiryDate }}</p>
          <label for="cvv">CVV</label>
          <p>{{ cvv }}</p>
        </div>

        <form @submit.prevent="processPayment">
        <div class="payment-buttons">
          <button type="submit" class="pay-btn">Pay Now</button>
          <button type="button" class="cancel-btn" @click="cancelOrder">Cancel Order</button>
        </div>
      </form>
      <div class="confirmation">{{ paymentMessage }}</div>
    </div>

    <RouterLink to="/create" class="text-blue-500 hover:underline" @click.prevent="createAccount" style="text-align: center; display: block; font-size: x-large;">
      To save information for future orders, please create an account.
    </RouterLink>

</template>
  
<style scoped>
.order-item .item-name {
  font-weight: bold;
  color: #333;
  padding-left: 8%;
}

.order-item .item-quantity,
.order-item .item-price {
  font-size: 1rem;
  color: #666;
  padding-left: 9%;
}

.order-total {
  text-align: right;
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}
.confirmation {
  color:#388e3c;
  font-size: xx-large;
  text-align: center;
  font-weight: bolder;
  padding: 2%;
}
.payment-section {
  background-color: #F8F8FF;
  padding: 20px;
  border-radius: 8px;
}

.payment-section h2 {
  font-size: large;
  color: #333;
  margin-bottom: 20px;
}

.card-details {
  margin-bottom: 20px;
}

.card-details label {
  display: block;
  font-weight: bold;
  margin-bottom: 8px;
  color: #555;
}

.card-details input {
  width: 100%;
  padding: 12px;
  font-size: 1rem;
  margin-bottom: 20px;
  border-radius: 8px;
  border: 1px solid #ddd;
  background-color: #fafafa;
}

.billing-details input {
  width: 100%;
  padding: 12px;
  font-size: 1rem;
  margin-bottom: 20px;
  border-radius: 8px;
  border: 1px solid #ddd;
  background-color: #fafafa;
}

.payment-buttons {
  display: flex;
  justify-content: space-between;
}
p {
  display: inline-block; 
  padding: 8px; 
  border: 1px solid #ccc; 
  border-radius: 4px;
  background-color: #f9f9f9; 
  font-family: 'Arial', sans-serif;
  font-size: 14px; 
  width: 300px; 
  word-wrap: break-word;
}

button {
  padding: 12px 20px;
  font-size: 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.pay-btn {
  background-color: #4caf50;
  color: white;
  width: 48%;
}

.pay-btn:hover {
  background-color: #388e3c;
}

.cancel-btn {
  background-color: #f6689c;
  color: white;
  width: 48%;
}

.cancel-btn:hover {
  background-color: #d5213f;
}
</style>
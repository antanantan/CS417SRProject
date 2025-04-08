<script setup>
import Card from '@/components/Steps_Bottom.vue';
import { ref, computed } from 'vue';
import axios from 'axios';

const createAccount = () => {
  router.push('/create'); 
};

const cardNumber = ref('****-****-****-****');
const expiryDate = ref('**/**');
const cvv = ref('***');
const paymentMessage = ref('');

const processPayment = () => {
  paymentMessage.value = "payment processed!";
}

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
    <h1>Step 4: Place your Order</h1>

    <h2 style="font-size: x-large; padding-left: 7%; font-weight: bold;">Order Summary</h2>
    <br>
    <div class="order-items">
      <div class="order-item">
        <div class="item-name">Item</div>
        <div class="item-quantity">Quantity</div>
        <div class="item-price">$Price</div>
      </div>
      <div class="order-total">
        <h3 style="padding-right: 7%;">Total: $Total</h3>
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
          <button type="button" class="cancel-btn">Cancel Order</button>
        </div>
      </form>
      <div class="confirmation">{{ paymentMessage }}</div>
    </div>

    <RouterLink to="/create" class="text-blue-500 hover:underline" @click.prevent="createAccount" style="text-align: center; display: block; font-size: x-large;">
      To save information for future orders, please create an account.
    </RouterLink>
    
    <Card></Card>
</template>
  
<style scoped>
h1 {
  font-size: xx-large;
  text-align: center;
  padding-top: 2%;
}
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
  background-color: #ffffff;
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
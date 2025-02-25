<script setup>
import Card from '@/components/Steps_Bottom.vue';
import { ref, computed } from 'vue';
import axios from 'axios';
const createAccount = () => {
  router.push('/create'); 
};
/** ref: ChatGPT. placeholder script 
const orderItems = ref([
  { name: "Pizza", quantity: 2, price: 15.99 },
  { name: "Burger", quantity: 1, price: 9.49 },
  { name: "Soda", quantity: 3, price: 2.49 },
]);
const cardNumber = ref('');
const expiryDate = ref('');
const cvv = ref('');
const billingAddress = ref('');

// Computed property for total price
const totalPrice = computed(() => {
  return orderItems.value.reduce(
    (total, item) => total + item.price * item.quantity,
    0
  );
});

// Methods
const processPayment = () => {
  // Logic to handle the payment processing
  console.log("Processing payment...");
  // For example, you can print out the payment details
  console.log({
    cardNumber: cardNumber.value,
    expiryDate: expiryDate.value,
    cvv: cvv.value,
    billingAddress: billingAddress.value,
  });
};*/
</script>

<template>
    <h1>Step 4: Place your Order</h1>

    <h2>Order Summary</h2>
    <div class="order-items">
        <div class="order-item">
          <div class="item-name">Item</div>
          <div class="item-quantity">Quantity</div>
          <div class="item-price">$Price</div>
    </div>
    <div class="order-total">
      <h3>Total: $Total</h3>
    </div>
    </div>

    <div class="payment-section">
      <h2>Payment Information</h2>

      <form @submit.prevent="processPayment">
        <div class="card-details">
          <label for="cardNumber">Card Number</label>
          <input type="text" id="cardNumber" placeholder="Enter your card number" required />

          <label for="expiryDate">Expiry Date</label>
          <input type="text" id="expiryDate" placeholder="MM/YY" required />

          <label for="cvv">CVV</label>
          <input type="text" id="cvv" placeholder="CVV" required />
        </div>

        <div class="payment-buttons">
          <button type="submit" class="pay-btn">Pay Now</button>
          <button type="button" class="cancel-btn">Cancel Order</button>
        </div>
      </form>
    </div>

    <RouterLink to="/create" class="text-blue-500 hover:underline" @click.prevent="createAccount">
      To save information for future orders, please create an account.
    </RouterLink>
    
    <Card></Card>
</template>
  
<style scoped>
h1 {
  font-size: xx-large;
  text-align: center;
}
.order-item .item-name {
  font-weight: bold;
  color: #333;
}

.order-item .item-quantity,
.order-item .item-price {
  font-size: 1rem;
  color: #666;
}

.order-total {
  text-align: right;
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
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
  background-color: #ff5c5c;
  color: white;
  width: 48%;
}

.cancel-btn:hover {
  background-color: #ff3b3b;
}
</style>
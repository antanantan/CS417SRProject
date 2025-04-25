import { ref } from 'vue';
import { authApi } from '@/api/auth.js';

export const userCart = ref([]);

// Fetch cart items from the backend
export const fetchUserCart = async (restaurantId = 'all') => {
  try {
    const url = restaurantId === 'all'
      ? "/user/cart"
      : `/user/cart/${restaurantId}`;
    const response = await authApi.get(url);
    userCart.value = response.data.cart_items;
    console.log("✅ Cart fetched:", userCart.value);
  } catch (error) {
    console.error("❌ Error fetching cart:", error);
    userCart.value = [];
  }
};

// Add a new item to the cart
export const addUserCartItem = async ({ menu_item_id, quantity = 1, options = [], restaurant_id }) => {
  try {
    const response = await authApi.post("/user/cart/item", {
      menu_item_id,
      quantity,
      options,
      restaurant_id
    });

    const newItem = {
      cart_item_id: response.data.cart_item_id,
      menu_item_id,
      quantity,
      options
    };

    userCart.value.push(newItem);
    console.log("Cart item added:", newItem);
    return newItem;
  } catch (error) {
    console.error("❌ Error adding cart item:", error);
    throw error;
  }
};

// Update an existing cart item (quantity and/or options)
export const updateUserCartItem = async (cart_item_id, quantity, options = []) => {
  try {
    await authApi.patch(`/user/cart/item/${cart_item_id}`, {
      quantity,
      options
    });

    const item = userCart.value.find(i => i.cart_item_id === cart_item_id);
    if (item) {
      item.quantity = quantity;
      item.options = options;
    }

    console.log("✏️ Cart item updated:", cart_item_id);
  } catch (error) {
    console.error("❌ Error updating cart item:", error);
    throw error;
  }
};

// Delete an item from the cart
export const deleteUserCartItem = async (cart_item_id) => {
  try {
    await authApi.delete(`/user/cart/item/${cart_item_id}`);
    userCart.value = userCart.value.filter(item => item.cart_item_id !== cart_item_id);
    console.log("🗑️ Cart item deleted:", cart_item_id);
  } catch (error) {
    console.error("❌ Error deleting cart item:", error);
    throw error;
  }
};
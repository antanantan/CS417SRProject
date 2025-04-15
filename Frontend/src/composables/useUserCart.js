import { ref } from 'vue';
import { authApi } from '@/api/auth.js';

export const userCart = ref([]);

export const fetchUserCart = async () => {
  try {
    const response = await authApi.get("/user/cart");
    userCart.value = response.data;
    console.log("✅ cart state updated:", userCart.value);
  } catch (error) {
    console.error("Error fetching cart data:", error);
    userCart.value = [];
  }
}

export const applyUserCartSelections = (menuItems) => {
    const cartIds = userCart.value.map(item => item.menu_id);
    menuItems.forEach(menuItem => {
        menuItem.selected = cartIds.includes(menuItem.id);
    });
}
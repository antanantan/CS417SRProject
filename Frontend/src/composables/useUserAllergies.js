import { ref } from 'vue';
import { authApi } from '@/api/auth.js';

export const userAllergies = ref([]);

export const fetchUserAllergies = async () => {
  try {
    const response = await authApi.get("/user/allergies");
    userAllergies.value = response.data;
    console.log("✅ allergy state updated:", userAllergies.value);
  } catch (error) {
    console.error("Error fetching allergy data:", error);
    userAllergies.value = [];
  }
};

export const applyUserAllergySelections = (allergenItems) => {
  const allergyIds = userAllergies.value.map(a => a.allergen_id);
  allergenItems.forEach(allergen => {
    allergen.selected = allergyIds.includes(allergen.id);
  });
};
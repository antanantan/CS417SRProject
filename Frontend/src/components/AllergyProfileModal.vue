<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { Icon } from "@iconify/vue";
import { api, authApi } from "@/api/auth.js";
import { userAllergies, fetchUserAllergies, applyUserAllergySelections } from '@/composables/useUserAllergies.js';

// get 'v-model'
const props = defineProps(["modelValue"]);
const emit = defineEmits(['update:modelValue', 'updated']);


// allergen data
const allergenGroups = ref([]);
const allergenItems = ref([]);

// get allergen data from backend
const fetchAllergenData = async () => {
  try {
    const response = await api.get("/allergens");
    allergenGroups.value = response.data.allergen_groups;
    allergenItems.value = response.data.allergen_items.map(item => ({
      ...item,
      selected: false
    }));
  } catch (error) {
    console.error("Error fetching allergy data:", error);
    allergenGroups.value = [];
    allergenItems.value = [];
  }
};

// 初回マウント時にデータ取得
onMounted(async () => {
  await fetchAllergenData();
  await fetchUserAllergies();
  applyUserAllergySelections(allergenItems.value);
});

watch(() => props.modelValue, async (isOpen) => {
  if (isOpen) {
    await fetchUserAllergies();
    applyUserAllergySelections(allergenItems.value);
  }
});

// 検索機能
const searchQuery = ref("");
// const filteredAllergies = computed(() => {
//   return allergenItems.value.filter((a) =>
//     a.name.toLowerCase().includes(searchQuery.value.toLowerCase())
//   );
// });
const filteredAllergenGroups = computed(() => {
  const query = searchQuery.value.toLowerCase();

  return allergenGroups.value
    .map(group => {
      const matchingAllergens = allergenItems.value.filter(allergen =>
        allergen.group_id === group.id &&
        (group.name.toLowerCase().includes(query) ||
         allergen.name.toLowerCase().includes(query))
      );

      return {
        ...group,
        allergens: matchingAllergens,
      };
    })
    .filter(group => group.allergens.length > 0);
});

// 検索をクリア
const clearSearch = () => {
  searchQuery.value = "";
};

// アレルゲンの選択・解除
const toggleAllergen = (allergen) => {
  allergenItems.selected = !allergenItems.selected;
};

// すべてのアレルギーを適用
const applyAllAllergies = async () => {
  const payload = {
    allergies: allergenItems.value
      .filter(a => a.selected)
      .map(a => ({
        allergen_id: a.id,
        scale: 1, // ここは一旦「あるだけで1」としておく。後でseverity選択に変更可能
      })),
  };

  try {
    // console.log("Payload value: ", payload);
    const response = await authApi.post('/user/allergies', payload);
    console.log(response.data.message);
    emit("updated"); 
    emit("update:modelValue", false);// close modal
  } catch (error) {
    console.error(
      'Error saving allergies:',
      error.response?.data?.message || error.message
    );
  }
};

// すべてのアレルギーをリセット
const resetAllAllergies = () => {
  allergenItems.value.forEach((allergy) => {
    allergy.severity = "";
    allergy.selected = false;
  });
};

// モーダルを閉じる
const close = () => {
  emit("update:modelValue", false);
};
</script>

<template>
  <!-- Sidebar Overlay -->
  <div v-show="modelValue" class="z-[9999] fixed inset-0 overflow-hidden ">
    <div
      class="absolute inset-0 bg-neutral-700 bg-opacity-75 transition-opacity duration-700"
      :class="{ 'opacity-75': modelValue, 'opacity-0': !modelValue }"
      @click="close"
    />

    <!-- Sidebar Content -->
    <section class="absolute inset-y-0 right-0 max-w-full flex">
      <div
        class="w-screen max-w-md bg-white shadow-xl transition-transform duration-700 ease-in-out transform"
        :class="{ 'translate-x-0': modelValue, 'translate-x-full': !modelValue }"
      >
        <div class="h-full flex flex-col py-6 px-6">
          <!-- モーダルヘッダー -->
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-semibold text-gray-900">Allergy Filter</h2>
            <button @click="close" class="text-gray-600 hover:text-gray-900">
              <Icon icon="mdi:close" class="w-6 h-6" />
            </button>
          </div>

          <!-- 検索バー -->
          <div class="flex items-center bg-white border-1 border-green-700 rounded-full p-1 w-full mx-auto">
            <Icon icon="mdi:magnify" class="w-5 h-5 text-green-700 m-2" />
            <input
              type="text"
              id="allergen-search"
              name="allergen-search"
              v-model="searchQuery"
              placeholder="Search allergens..."
              class="flex-grow bg-transparent border-none placeholder-neutral-400 focus:outline-none text-gray-700 pr-2"
            />
            <Icon
              v-if="searchQuery"
              icon="mdi:close"
              @click="clearSearch"
              class="w-5 h-5 text-green-700 cursor-pointer mr-2"
            />
          </div>

          <!-- アレルギーリスト -->
          <div class="mt-4 overflow-auto flex-1 ">
            <div v-for="group in filteredAllergenGroups" :key="group.id" class="mb-4">
              <h3 class="text-md font-bold text-gray-800 border-b pb-1">{{ group.name }}</h3>
              <ul class="mt-2 space-y-2">
                <li
                  v-for="allergen in allergenItems.filter(a => a.group_id === group.id)"
                  :key="allergen.id"
                  class="flex items-center"
                >
                  <input
                    type="checkbox"
                    :id="`allergen-${allergen.id}`"
                    :name="`allergen-${allergen.id}`"
                    v-model="allergen.selected"
                    @change="toggleAllergen(allergen)"
                    class="mr-2"
                  />
                  <span class="text-gray-700">{{ allergen.name }}</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- 操作ボタン -->
          <div class="mt-6 flex justify-end space-x-2">
            <button @click="resetAllAllergies" class="px-4 py-2 bg-gray-300 text-gray-800 rounded-full hover:bg-gray-400">Reset</button>
            <button @click="applyAllAllergies" class="px-4 py-2 border-1 border-green-700 text-green-700 rounded-full hover:text-white hover:bg-green-700 transition">Apply</button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
<script setup>
import { useRouter, useRoute } from "vue-router";
import Disclaimer from "@/components/Disclaimer.vue"
import { api, authApi } from "@/api/auth.js";
import { ref, onUpdated, computed, onMounted, watch } from "vue";
import { userAllergies, fetchUserAllergies, applyUserAllergySelections } from '@/composables/useUserAllergies.js';
import { Icon } from "@iconify/vue";

const router = useRouter();
const route = useRoute();

// allergen data
const allergenGroups = ref([]);
const allergenItems = ref([]);

const groupVisibility = ref({});

// get allergen data from backend
const fetchAllergenData = async () => {
  try {
    const response = await api.get("/allergens");
    allergenGroups.value = response.data.allergen_groups;
    allergenItems.value = initializeAllergenItems(response.data.allergen_items);
    groupVisibility.value = Object.fromEntries(allergenGroups.value.map(g => [g.id, false]));
  } catch (error) {
    console.error("Error fetching allergy data:", error);
    allergenGroups.value = [];
    allergenItems.value = [];
  }
};

const initializeAllergenItems = (rawItems) => {
  return rawItems.map(item => ({
    ...item,
    selected: false,
    scale: 2,
  }));
};

// get data when modal is opened
onMounted(async () => {
  await fetchAllergenData();
  await fetchUserAllergies();
  applyUserAllergySelections(allergenItems.value);
});

// search function
const searchQuery = ref("");
const filteredAllergenGroups = computed(() => {
  const query = searchQuery.value.toLowerCase();

  return allergenGroups.value
    .map(group => {
      const allGroupItems = allergenItems.value.filter(a => a.group_id === group.id);
      const matchingItems = allGroupItems.filter(a =>
        group.name.toLowerCase().includes(query) ||
        a.name.toLowerCase().includes(query)
      );

      return {
        ...group,
        allergens: allGroupItems, // keep all items in the group
        filteredAllergens: matchingItems, // only for matching items
      };
    })
    .filter(group => group.filteredAllergens.length > 0); // at least one item matches
});

// clear search input
const clearSearch = () => {
  searchQuery.value = "";
};

// allergen selection/removal
const toggleAllergen = (allergen) => {
  allergenItems.selected = !allergenItems.selected;
};

// update backend with selected allergens
const applyAllAllergies = async () => {
  const payload = {
    allergies: allergenItems.value
      .filter(a => a.selected)
      .map(a => ({
        allergen_id: a.id,
        scale: Number(a.scale), // temporarily set to 1
      })),
  };

  try {
    // console.log("Payload value: ", payload);
    const response = await authApi.put('/user/allergies', payload);
    console.log(response.data.message);
    await fetchUserAllergies();
    applyUserAllergySelections(allergenItems.value);
    router.push("/location");
  } catch (error) {
    console.error(
      'Error saving allergies:',
      error.response?.data?.message || error.message
    );
  }
};

// remove all allergen selections
const resetAllAllergies = () => {
  allergenItems.value.forEach((allergy) => {
    allergy.severity = "";
    allergy.selected = false;
  });
};

// hidden/show allergen group items
const toggleGroup = (groupId) => {
  groupVisibility.value[groupId] = !groupVisibility.value[groupId];
};
// button to sellect all allergens in a group
const toggleGroupSelection = (groupId, selected) => {
  allergenItems.value.forEach(item => {
    if (item.group_id === groupId) {
      item.selected = selected;
    }
  });
};
// range slider to set allergen scale
const updateGroupScale = (groupId, newValue) => {
  const newScale = Number(newValue);
  allergenItems.value.forEach(allergen => {
    if (allergen.group_id === groupId && allergen.selected) {
      allergen.scale = newScale;
    }
  });
};

const groupCheckboxRefs = ref({});
onUpdated(() => {
  filteredAllergenGroups.value.forEach(group => {
    const allSelected = group.allergens.every(a => a.selected);
    const noneSelected = group.allergens.every(a => !a.selected);
    const someSelected = !allSelected && !noneSelected;

    const checkboxEl = groupCheckboxRefs.value[group.id];
    if (checkboxEl) {
      checkboxEl.indeterminate = someSelected;
    }
  });
});

// color severity scale
const severityColor = (scale) => {
  switch (Number(scale)) {
    case 1: return '!border-green-400';
    case 2: return '!border-yellow-400';
    case 3: return '!border-red-400';
  }
};
// get allergen name from id
const getAllergenName = (id) => {
  const found = allergenItems.value.find(item => item.id === id);
  return found ? found.name : 'Unknown';
};

// code for handling disclaimer modal
const isAgreed = ref(false); 
const isDisclaimerVisible = ref(false);
const handleCheckboxClick = (event) => {
  if (!isAgreed.value) { // if still not agreed
    event.preventDefault(); // prevent checkbox from being checked
    isDisclaimerVisible.value = true;
  } else { // if already agreed
    isAgreed.value = false; // uncheck the checkbox
  }
};
const closeDisclaimer = (agreed) => {
  isDisclaimerVisible.value = false;
  isAgreed.value = agreed;
};

// codes used for searching functionality
const searchIndex = ref(0);
const highlightRow = ref(0);
const searchNext = () => {
  if (searchIndex.value < filteredAllergies.value.length - 1) {
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
    searchIndex.value = filteredAllergies.value.length - 1;
  }
  highlightRow.value = searchIndex.value;
};
</script>

<template>
  <div class="flex flex-col p-6 pb-20">
    <div class="shrink-0 z-10 bg-white">
      <!-- header -->
      <div class="flex justify-between items-center pb-2">
        <h2 class="text-lg font-semibold text-neutral-900">Allergy Filter</h2>
      </div>

      <!-- Applied Allergens Badge List -->
      <div class="overflow-x-auto">
        <div class="flex items-center text-sm text-neutral-700 pb-2 space-x-2 min-w-full whitespace-nowrap">
          <span class="pr-2">Applied allergies: </span>
          <span v-if="userAllergies.length === 0" class="italic text-neutral-400">None</span>
          <template v-else>
            <div
              v-for="allergy in userAllergies"
              :key="allergy.allergen_id"
              class="px-2 py-1 border rounded-full"
              :class="severityColor(allergy.scale)"
            >
              {{ getAllergenName(allergy.allergen_id) }}
            </div>
          </template>
        </div>
      </div>

      <div class="w-">
        <!-- search bar -->
        <div class="flex items-center bg-white border border-rose-400 rounded-full h-11 w-full mx-auto">
          <Icon icon="mdi:magnify" class="w-5 h-5 text-rose-400 ml-3" />
          <input
            type="text"
            id="allergen-search"
            name="allergen-search"
            v-model="searchQuery"
            placeholder="Search allergens..."
            class="flex-grow bg-transparent border-none placeholder-neutral-400 focus:ring-0 focus:outline-none text-neutral-700 p-2"
          />
          <Icon
            v-if="searchQuery"
            icon="mdi:close"
            @click="clearSearch"
            class="w-5 h-5 text-rose-400 cursor-pointer mr-3"
          />
        </div>

        <!-- severity scale -->
        <div class="relative text-xs pt-2">
          <div class="absolute w-32 right-4 ">
            <span class="absolute -left-[50%] -translate-x-1/2 flex flex-items justify-center text-neutral-400">
              Severity
              <div class="relative group">
                <Icon icon="mdi:information" class="w-4 h-4 mx-1 cursor-pointer pointer-events-auto" />
                <!-- tooltip -->
                <div
                  class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 text-xs text-white bg-neutral-700 rounded shadow-lg opacity-0 group-hover:!opacity-100 transition-opacity duration-200 whitespace-nowrap z-[9999] pointer-events-none"
                >
                  Choose how severe the reaction is.<br>
                  - Mild: No reaction, or only with raw food. Cooked food is tolerated.<br>
                  - Moderate: Noticeable symptoms such as hives or stomach upset.<br>
                  - Severe: Airborne exposure or risk of anaphylaxis.
                </div>
              </div>
              :
            </span>
            <span class="absolute left-[0%] -translate-x-1/2 text-green-400">Mild</span>
            <span class="absolute left-[50%] -translate-x-1/2 text-yellow-400">Moderate</span>
            <span class="absolute left-[100%] -translate-x-1/2 text-red-400">Severe</span>
          </div>
        </div>

        <!-- allergens list -->
        <div class="mt-4 mb-2 overflow-y-auto flex-1 bg-gradient-to-t from-transparent via-white to-white ">
          <div v-for="group in filteredAllergenGroups" :key="group.id" class="pb-4">
            <!-- if there is only one item in allergen group -->
            <template v-if="group.allergens.length === 1">
              <div class="flex items-center pl-7 relative">
                <label :for="`allergen-${group.allergens[0].id}`" class="custom-input-wrapper w-full text-md font-medium text-neutral-800 pb-1">
                  <input
                    type="checkbox"
                    :id="`allergen-${group.allergens[0].id}`"
                    :name="`allergen-${group.allergens[0].id}`"
                    v-model="group.allergens[0].selected"
                    @change="toggleAllergen(group.allergens[0]) && (group.allergens[0].scale = 2)"
                    class="mr-2 peer appearance-none h-4 w-4 bg-white border border-neutral-300 rounded transition duration-200 focus:ring-0 focus:outline-none focus:ring-transparent checked:bg-rose-400 checked:border-rose-400"
                  />
                  <Icon icon="mdi:check" class="custom-check-icon"
                  />
                  {{ group.name }}
                </label>
                <input
                  type="range"
                  :value="group.allergens[0].selected ? group.allergens[0].scale : 2"
                  :disabled="!group.allergens[0].selected"
                  @input="group.allergens[0].scale = Number($event.target.value)"
                  class="range-slider appearance-none absolute w-32 right-4 rounded-full cursor-pointer "
                  :class="[group.allergens[0].selected ? 'bg-gradient-to-r from-green-100 via-yellow-100 to-red-100' : '!bg-neutral-100 cursor-not-allowed']" 
                  min="1" max="3" step="1"/>
              </div>
            </template>

            <!-- if there are multiple items in allergen group -->
            <template v-else>
              <div
                class="flex items-center cursor-pointer select-none relative"
                @click="toggleGroup(group.id)"
              >
                <!-- toggle icon -->
                <Icon
                  v-if="!groupVisibility[group.id]"
                  icon="mdi:keyboard-arrow-down"
                  class="w-5 h-5 text-neutral-600 mr-2"
                />
                <Icon
                  v-else
                  icon="mdi:keyboard-arrow-up"
                  class="w-5 h-5 text-neutral-600 mr-2"
                />
                <!-- select all  -->
                <div class="custom-input-wrapper">
                  <input
                    type="checkbox"
                    :ref="el => groupCheckboxRefs[group.id] = el"
                    :id="`group-select-${group.id}`"
                    :checked="group.allergens.every(a => a.selected)"
                    @click.stop="toggleGroupSelection(group.id, !group.allergens.every(a => a.selected))"
                    class="mr-2 peer appearance-none h-4 w-4 bg-white border border-neutral-300 rounded transition duration-200 focus:ring-0 focus:outline-none focus:ring-transparent checked:bg-rose-400 checked:border-rose-400 indeterminate:bg-rose-400 indeterminate:border-rose-400"
                  />
                  <Icon icon="mdi:check" class="custom-check-icon"
                    />
                  <Icon 
                    icon="mdi:minus"
                    class="custom-minus-icon"
                  />
                </div>
                <label class="text-md font-medium text-neutral-800 py-1">
                  {{ group.name }}
                </label>
                <input 
                  type="range"
                  @click.stop
                  :value="group.allergens.every(a => a.selected) && group.allergens.every(a => a.scale === group.allergens[0].scale) ? group.allergens[0].scale : 2"
                  :disabled="!group.allergens.every(a => a.selected) || !group.allergens.every(a => a.scale === group.allergens[0].scale)"
                  @input="updateGroupScale(group.id, $event.target.value)" 
                  class="range-slider appearance-none absolute w-32 right-4 rounded-full cursor-pointer "
                  :class="[group.allergens.every(a => a.selected) && group.allergens.every(a => a.scale === group.allergens[0].scale) ? 'bg-gradient-to-r from-green-100 via-yellow-100 to-red-100' : 'bg-neutral-100 cursor-not-allowed']" 
                  min="1" max="3" step="1"
                />
                
              </div>
              <ul v-if="groupVisibility[group.id]" class="pt-1 space-y-2 pl-7 relative">
                <li
                  v-for="allergen in group.filteredAllergens"
                  :key="allergen.id"
                  class="flex items-center"
                >
                  
                  <label :for="`allergen-${allergen.id}`" class="custom-input-wrapper text-neutral-700">
                    <input
                      type="checkbox"
                      :id="`allergen-${allergen.id}`"
                      :name="`allergen-${allergen.id}`"
                      v-model="allergen.selected"
                      @change="toggleAllergen(allergen) && (allergen.scale = 2)"
                      class="mr-2 peer appearance-none h-4 w-4 bg-white border border-neutral-300 rounded transition duration-200 focus:ring-0 focus:outline-none focus:ring-transparent checked:bg-rose-400 checked:border-rose-400"
                    />
                    <Icon icon="mdi:check" class="custom-check-icon"
                    />
                    {{ allergen.name }}
                  </label>
                  <input 
                    type="range"
                    :value="allergen.selected ? allergen.scale : 2"
                    :disabled="!allergen.selected"
                    @input="allergen.scale = Number($event.target.value)"
                    class="range-slider appearance-none absolute w-32 right-4 rounded-full cursor-pointer "
                    :class="[allergen.selected ? 'bg-gradient-to-r from-green-100 via-yellow-100 to-red-100' : 'bg-neutral-100 cursor-not-allowed']" 
                    min="1" max="3" step="1"
                  />
                </li>
              </ul>
            </template>
          </div>
        </div>
      </div>

      <!-- buttons -->
      <div class="fixed left-0 bottom-14 bg-white w-full p-4 z-50">
        <div class="flex items-center justify-between w-full pl-4">
          <label class="custom-input-wrapper flex items-center">
            <input type="checkbox" id="agree" :checked="isAgreed" @click="handleCheckboxClick" class="mr-2 peer appearance-none h-4 w-4 bg-white border border-neutral-300 rounded transition duration-200 focus:ring-0 focus:outline-none focus:ring-transparent checked:bg-rose-400 checked:border-rose-400" />
            <Icon icon="mdi:check" class="custom-check-icon" />
            <span for="agree" class="text-sm text-neutral-700">
              I agree to to the terms of the disclaimer.
            </span>
          </label>
          <div class="flex space-x-4">
            <button @click="resetAllAllergies" class="px-4 w-24 h-11 bg-neutral-300 text-neutral-800 rounded-full hover:bg-neutral-400">Reset</button>
            <button @click="applyAllAllergies" :disabled="!isAgreed" class="px-4 w-24 h-11 border border-rose-400 text-rose-400 rounded-full hover:text-white hover:bg-rose-400 transition disabled:opacity-50 " :title="!isAgreed ? 'Please agree to continue.' : ''">Apply</button>
          </div>
        </div>
        <Disclaimer v-if="isDisclaimerVisible" @close="closeDisclaimer"/>
      </div>
    </div>
  </div>

</template>
 
<style>
.range-slider::-webkit-slider-thumb {
  appearance: none;
  height: 1rem;
  width: 1rem;
  border-radius: 9999px;
  cursor: pointer;
  border: none;
  background-color: #ffffff;
  box-shadow: 0 0 2px #9FA6AD;
}

.range-slider:disabled::-webkit-slider-thumb {
  background-color: #d4d4d4; /* neutral-300 */
}

.range-slider::-moz-range-thumb {
  height: 1rem;
  width: 1rem;
  border-radius: 9999px;
  cursor: pointer;
  border: none;
  box-shadow: 0 0 2px #9FA6AD;
}

.range-slider:disabled::-moz-range-thumb {
  background-color: #d4d4d4;
}
</style>
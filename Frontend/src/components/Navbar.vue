<script setup>
import { RouterLink, useRoute } from 'vue-router';
import { ref } from 'vue';
import logo from '@/assets/img/logo.png';
import { Icon } from '@iconify/vue';
import { api, authApi } from "@/api/auth.js";
import AllergyProfileModal from "@/components/AllergyProfileModal.vue";
import { userAllergies, fetchUserAllergies, applyUserAllergySelections } from '@/composables/useUserAllergies.js';

const isActiveLink = (routePath) => {
  const route = useRoute();
  return route.path === routePath;
};

const showFilterModal = ref(false);

const openAllergyModal = () => {
  showFilterModal.value = true;
};
</script>

<template>
  <nav class="bg-green-700 w-full fixed top-0 left-0 z-50 shadow-md">
    <div class="flex h-16 items-center justify-between px-4">
      <div class="flex flex-1 items-center justify-center md:items-stretch md:justify-start">
        <RouterLink class="flex flex-shrink-0 items-center" to="/">
          <img class="h-10 w-auto" :src="logo" alt="Eat Well Logo"/>
          <span class="hidden md:block text-white text-2xl font-bold ">
          </span>
        </RouterLink>
        <div class="md:ml-auto">
          <div class="flex items-center space-x-2">
            <RouterLink
              to="/login"
              :class="[
                isActiveLink('/')
                  ? 'bg-green-900'
                  : 'hover:bg-gray-900 hover:text-white',
                'text-white',
                'px-3',
                'py-2',
                'rounded-md',
              ]">Log In</RouterLink
            ><br></br>
            <RouterLink
              to="/allergy_list"
              :class="[
                isActiveLink('/login')
                  ? 'bg-green-900'
                  : 'hover:bg-gray-900 hover:text-white',
                'text-white',
                'px-3',
                'py-2',
                'rounded-md',
              ]"
              >Guest</RouterLink>

            <RouterLink to="/profile" class="group rounded-full bg-green-700 text-white hover:bg-white mr-8">
              <Icon icon='mdi:user' class="w-7 h-7 group-hover:text-green-700 m-2" ></Icon>
            </RouterLink>

            <button @click="openAllergyModal" class="group rounded-full bg-green-700 text-white hover:bg-white mr-8">
              <Icon icon='mdi:food-allergy' class="w-7 h-7 group-hover:text-green-700 m-2" ></Icon>
            </button>


            <RouterLink to="/order" class="group rounded-full bg-green-700 text-white hover:bg-white mr-10">
              <Icon icon='mdi:cart' class="w-7 h-7 group-hover:text-green-700 m-2"></Icon>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </nav>
  <AllergyProfileModal v-model="showFilterModal" @updated="fetchUserAllergies" />

</template>
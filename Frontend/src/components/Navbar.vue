<script setup>
import { RouterLink, useRoute } from 'vue-router';
import logo from '@/assets/img/logo.png';
import { Icon } from '@iconify/vue';

const isActiveLink = (routePath) => {
  const route = useRoute();
  return route.path === routePath;
};
</script>

<template>
  <nav class="bg-green-700">
    <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
      <div class="flex h-20 items-center justify-between">
        <div class="flex flex-1 items-center justify-center md:items-stretch md:justify-start">
          <RouterLink class="flex flex-shrink-0 items-center mr-4" to="/">
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

              <button class="group rounded-full bg-green-700 text-white hover:bg-white mr-8">
                <Icon icon='mdi:user' class="w-7 h-7 group-hover:text-green-700 m-2" ></Icon>
              </button>

              <button class="group rounded-full bg-green-700 text-white hover:bg-white mr-8">
                <Icon icon='mdi:food-allergy' class="w-7 h-7 group-hover:text-green-700 m-2" ></Icon>
              </button>

              <button class="group rounded-full bg-green-700 text-white hover:bg-white">
                <Icon icon='mdi:cart' class="w-7 h-7 group-hover:text-green-700 m-2"></Icon>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>
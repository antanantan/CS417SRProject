<script setup>
import { Icon } from '@iconify/vue';
</script>

<template>
  <div class="how-it-works mt-10 px-4 text-center">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">How It Works</h2>
    <div class="flex flex-wrap justify-center gap-4">
      
      <div class="bg-white p-6 rounded-lg shadow-lg w-full sm:w-64 text-center hover:shadow-xl transition-shadow">
        <Icon icon="mdi:food-allergy" class="h-12 w-12 text-green-600 mx-auto mb-4" />
        <h3 class="text-xl font-semibold text-gray-700">Allergy Profile</h3>
        <p class="text-sm text-gray-500 mt-2">Set your dietary preferences to filter menus accordingly.</p>
      </div>
      
      <div class="bg-white p-6 rounded-lg shadow-lg w-full sm:w-64 text-center hover:shadow-xl transition-shadow">
        <Icon icon="carbon:location" class="h-12 w-12 text-green-600 mx-auto mb-4" />
        <h3 class="text-xl font-semibold text-gray-700">Location Selection</h3>
        <p class="text-sm text-gray-500 mt-2">Find restaurants near you based on your location.</p>
      </div>
      
      <div class="bg-white p-6 rounded-lg shadow-lg w-full sm:w-64 text-center hover:shadow-xl transition-shadow">
        <Icon icon="ph:fork-knife-bold" class="h-12 w-12 text-green-600 mx-auto mb-4" />
        <h3 class="text-xl font-semibold text-gray-700">Menu Filtering</h3>
        <p class="text-sm text-gray-500 mt-2">See only the items that match your dietary needs.</p>
      </div>
      
    
      <div class="bg-white p-6 rounded-lg shadow-lg w-full sm:w-64 text-center hover:shadow-xl transition-shadow">
        <Icon icon="mdi:credit-card-check-outline" class="h-12 w-12 text-green-600 mx-auto mb-4" />
        <h3 class="text-xl font-semibold text-gray-700">Secure Ordering</h3>
        <p class="text-sm text-gray-500 mt-2">Place your order securely and enjoy a safe dining experience.</p>
      </div>
      
    </div>
  </div>
</template>

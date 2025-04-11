<script setup>
import Navbar from '@/components/Navbar.vue';
import BottomNavigation from '@/components/BottomNavigation.vue';
import { RouterView, useRoute} from 'vue-router';
import { computed } from 'vue';

const route = useRoute();

// Determine if the bottom navigation should be shown
const showBottomNav = computed(() => {
  // Only show on ordering flow pages
  const orderFlowRoutes = ['/allergy_list', '/location', '/menu', '/order'];
  const basePath = '/' + route.path.split('/')[1];
  
  return orderFlowRoutes.includes(basePath) ||
         orderFlowRoutes.some(path => route.path.startsWith(path + '/'));
});
</script>

<template>
  <v-app>
    <Navbar />
    <v-main>
      <div class="py-16 pb-24">
        <RouterView />
      </div>
    </v-main>
    <BottomNavigation v-if="showBottomNav"/>
  </v-app>
</template>

<style>
body{
  padding-bottom: 56px;
  -webkit-tap-highlight-color: transparent;  
}

.v-bottom-navigation, 
.navigation-container,
.v-btn {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  touch-action: manipulation;
}
</style>
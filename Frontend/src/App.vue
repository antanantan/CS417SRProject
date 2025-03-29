<script setup>
import Navbar from '@/components/Navbar.vue';
import Card from '@/components/Steps_Bottom.vue';
import { RouterView } from 'vue-router';
</script>

<template>
  <Navbar />
  <div class="py-16">
      <RouterView />
  </div>
</template>
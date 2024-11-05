<script setup>
import HomeCards from '@/components/HomeCards.vue';
</script>

<template>
  <Hero />
  <HomeCards />
  <JobListings :limit="3" :showButton="true" />
</template>
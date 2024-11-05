<script setup>
import Hero from '@/components/Hero.vue';
import HomeCards from '@/components/HomeCards.vue';
</script>

<template>
  <Hero />
  <HomeCards />
  <JobListings :limit="3" :showButton="true" />
</template>
<script setup>
import Hero from '@/components/Hero.vue';
import HomeCards from '@/components/HomeCards.vue';
import HowItWorks from '@/components/HowItWorks.vue';
</script>

<!--we should have a function to create an account on this homepage (i don't know why we didn't already have one)-->
<template>
  <Hero/>
  <HomeCards/>
  <h1 style="text-align: center; font-size: xx-large">Ready to Eat Well? <a href="/create" style="color:palevioletred"> Start Here.</a></h1>
  <!-- above link is just a placeholder for the actual account creation-->
  <HowItWorks/>
</template>
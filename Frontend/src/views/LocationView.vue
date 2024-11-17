<script setup>
import Card from '@/components/Steps_Bottom.vue';
</script>

<template>
  <p>Step 2: Select your desired location</p>
  <!--insert map from flask backend. takes in zip code input and spits out a location in folium-->
    <Card></Card>
</template>

<!--TODO: implement map view somehow. a map.py was started in the backend-->
  
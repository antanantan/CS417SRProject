<script setup>
import Card from '@/components/Steps_Bottom.vue';

</script>

<template>
  <h1>Step 2: Select Location</h1>
<!--ref: https://www.google.com/search?q=insert+map+in+vue+using+folium&oq=insert+map+in+vue+using+folium&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDQ0MDFqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8-->

<!--TODO: fix file ref-->
  <div>
    <iframe :src="map.html" width="600" height="450"></iframe>
  </div>

  <Card></Card>
</template>


<script>
export default {
  data() {
    return {
      mapURL: "/assets/map.html" // Update with the correct path
    };
  },
};
</script>

<style>
h1 {
  font-size: large;
  text-align: center;
}
</style>
<!--TODO: implement map view somehow. a map.py was started in the backend-->
  
<!--how to use icons T-T -->
<!-- how to make navigation bar... NAVIGABLE??-->
<script scoped>
import { GrowBottomNavigation } from "bottom-navigation-vue";
import "bottom-navigation-vue/dist/style.css";
import OrderView from "@/views/OrderView.vue";
import { Icon } from '@iconify/vue';
import AllergyListView from "@/views/AllergyListView.vue";
import LocationView from "@/views/LocationView.vue";
import { ref } from "vue";
import { RouterLink } from "vue-router";

export default {
    components: { GrowBottomNavigation },
    data: () => ({
    selected: ref,
    options: [
      { id: 1, title: 'Step 1: Allergy Profile', color: '#db79cf', path: '/'},
      { id: 2, title: 'Step 2: Choose Restaurant', color: '#db79cf'},
      { id: 3, title: 'Step 3: Menu Filter', color: '#db79cf'},
      { id: 4, title: 'Step 4: Place Order', color: '#db79cf'}
    ]
    }),
  };

</script>

<template>
    <GrowBottomNavigation :options="options" v-model=RouterLink />
      <li v-for="option in options" :key="option.id">
        <router-link 
          :to="option.path"
          :style="{ color: option.color }"
          :class="{ active: isActive(option.path) }">
          {{ option.title }}
        </router-link>
      </li>

</template>


<style scoped>

</style>

<!--ref: https://mbanga-anele.medium.com/how-to-add-a-sophisticated-bottom-navigation-bar-to-your-vue-apps-12cd46185f94-->
<!--ref: https://github.com/imanmalekian31/vue-bottom-navigation -->
<!--ref: https://vuetifyjs.com/en/components/bottom-navigation/#usage-->
<!--https://vue-bottom-navigation.netlify.app/-->
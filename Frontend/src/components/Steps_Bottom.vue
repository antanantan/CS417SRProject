<script setup>
import { GrowBottomNavigation } from "bottom-navigation-vue";
import "bottom-navigation-vue/dist/style.css";
import { Icon } from '@iconify/vue';
import { useRouter, useRoute } from "vue-router";
import { ref, watch} from 'vue';

const route = useRoute(); 
const selectedOption = ref(route.path);


const options = [
      { id: 1, icon:'mdi:food-allergy', title: 'Step 1: Allergy Profile',  color: '#db79cf', path: '/allergy_list'},
      { id: 2, icon:'carbon:location', title: 'Step 2: Choose Restaurant', color: '#db79cf', path: '/location'},
      { id: 3, icon:'ph:fork-knife-bold', title: 'Step 3: Menu Filter', color: '#db79cf', path: '/menu'},
      { id: 4, icon:'mdi:credit-card-check-outline', title: 'Step 4: Place Order', color: '#db79cf', path: '/order'},
];

watch(route, (newRoute) => {
  selectedOption.value = newRoute.path;
});

</script>

<template>
  <div class="bottom-navigation">
    <GrowBottomNavigation 
    v-model="selectedOption" 
    :options="options"
    class="flex justify-around items-center text-center"
    >
      <template #icon="{ props }">
        <div class ="flex justify-center items-center">
        <Icon :icon="props.icon" class="h-7 w-7 mb-1" />
        </div>
      </template>

      <template #title="{ props }">
        <span class="text-xs font-semibold">
          {{ props.title }}
        </span>
      </template> 
    </GrowBottomNavigation>
  </div>
</template>





<!--ref: https://mbanga-anele.medium.com/how-to-add-a-sophisticated-bottom-navigation-bar-to-your-vue-apps-12cd46185f94-->
<!--ref: https://github.com/imanmalekian31/vue-bottom-navigation -->
<!--ref: https://vuetifyjs.com/en/components/bottom-navigation/#usage-->
<!--https://vue-bottom-navigation.netlify.app/-->
<!--https://vue-bottom-navigation.netlify.app/guide/grow-->
<!--how to use icons T-T -->
<!-- how to make navigation bar... NAVIGABLE??-->
<script scoped>
import { GrowBottomNavigation } from "bottom-navigation-vue";
import "bottom-navigation-vue/dist/style.css";
import OrderView from "@/views/OrderView.vue";
import { Icon } from '@iconify/vue';

const gotoOrderView = () => {
    router.push('/order');
  };
export default {
    components: { GrowBottomNavigation },
    data: () => ({
    selected: 1,
    options: [
      { id: 1, Icon:"mdi:food-allergy", class:"h-12 w-12 text-green-600 mx-auto mb-4", title: 'Step 1: Allergy Profile', color: '#db79cf', path: onclick=gotoOrderView},
      { id: 2, icon: 'test.png', title: 'Step 2: Choose Restaurant', color: '#db79cf', path: '/location'},
      { id: 3, icon: 'test.png', title: 'Step 3: Menu Filter', color: '#db79cf', path: ''},
      { id: 4, icon: 'test.png', title: 'Step 4: Place Order', color: '#db79cf', path: '/'}
    ]
    }),
  };

</script>

<template>
  <GrowBottomNavigation :options="options" v-model="selected" />
</template>


<style scoped>

</style>

<!--ref: https://mbanga-anele.medium.com/how-to-add-a-sophisticated-bottom-navigation-bar-to-your-vue-apps-12cd46185f94-->
<!--ref: https://github.com/imanmalekian31/vue-bottom-navigation -->
<!--ref: https://vuetifyjs.com/en/components/bottom-navigation/#usage-->
<!--https://vue-bottom-navigation.netlify.app/-->
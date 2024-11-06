<script setup>
import HomeCards from '@/components/HomeCards.vue';
import Card from '@/components/Steps_Bottom.vue';
import Steps_Bottom from '@/components/Steps_Bottom.vue';

const gotoLocation = () => {
    router.push('/location');
  };
  
const gotoOrderView = () => {
    router.push('/order');
  };
  
</script>

<template>
    <p>this page will allow the user to select menu options that are not grayed out based on their allergy preferences</p>
    <div class="text-center mt-4">
        <RouterLink
        to="/order"
        class="text-blue-500 hover:underline"
        @click.prevent="gotoOrderView"
        >
        Step 4: Ordering
        </RouterLink>
    </div>
    <Card></Card>
</template>
  
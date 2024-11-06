<script setup>
import Card from '@/components/Steps_Bottom.vue';

const gotoAllergyList = () => {
    router.push('/allergy_list');
  };
  
const gotoMenuFilter = () => {
    router.push('/menu');
  };
  
</script>

<template>
    <p>this page will allow the user to select a restaurant based on a location on the map that will be displayed i suppose</p>
    <div class="text-center mt-4">
        <RouterLink
        to="/allergy_list"
        class="text-blue-500 hover:underline"
        @click.prevent="gotoAllergyList"
        >
        Go Back
        </RouterLink>
    </div>
    <br>
    <div class="text-center mt-4">
        <RouterLink
        to="/menu"
        class="text-blue-500 hover:underline"
        @click.prevent="gotoMenuFilter"
        >
        Step 3: Menu
        </RouterLink>
    </div>
    <Card>
    </Card>
</template>

<!--TODO: implement map view somehow. a map.py was started in the backend-->
  
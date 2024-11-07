<script setup>
import Card from '@/components/Steps_Bottom.vue';
import {ref} from 'vue';
import {useRouter, RouterLink } from "vue-router";
import Disclaimer from '@/components/Disclaimer.vue';

const router = useRouter();

const gotoLocationPicker = () => {
  router.push('/location');};
</script>

<template>
    <p>this page will have a list of allergens and dietary restrictions that the user can filter</p>
    <div class="text-center mt-4">
        <RouterLink
          to="/location"
          class="text-blue-500 hover:underline"
          @click.prevent="gotoLocationPicker">
          Step 2: Location Picker
        </RouterLink>
      </div>

      <div>
    <h2>Checklist</h2>
    <ul>
      <li v-for="(item, index) in items" :key="index">
        <input type="checkbox" v-model="item.checked">
        <label>{{ item.label }}</label>
      </li>
    </ul>
  </div>
      <Card></Card>
</template>

<script>
export default {
    data() {
      return {
        items: [
          { label: 'Peanuts', checked: false },
          { label: 'Tree Nuts', checked: false },
          { label: 'Shellfish', checked: false }
        ]
      }
    }
  }

</script>

  

<!--TODO: implement checklist feature-->
<!--reference: https://www.google.com/search?q=how+to+implement+a+checklist+in+vue&sca_esv=2100fb941db67f3a&ei=6ZkqZ8fcKLqHptQPxqS4kAE&ved=0ahUKEwiH9ZbYnMaJAxW6g4kEHUYSDhIQ4dUDCBA&uact=5&oq=how+to+implement+a+checklist+in+vue&gs_lp=Egxnd3Mtd2l6LXNlcnAiI2hvdyB0byBpbXBsZW1lbnQgYSBjaGVja2xpc3QgaW4gdnVlMgUQIRigATIFECEYoAEyBRAhGKABMgUQIRifBTIFECEYnwUyBRAhGJ8FMgUQIRifBTIFECEYnwVIwQ5QqglYsQpwBHgBkAEAmAGDAaABpAKqAQMyLjG4AQPIAQD4AQGYAgegArECwgIKEAAYsAMY1gQYR8ICBhAAGBYYHsICCxAAGIAEGIYDGIoFwgIIEAAYgAQYogSYAwCIBgGQBgiSBwM2LjGgB8YV&sclient=gws-wiz-serp-->
<!--there are probably much nicer ways to do this-->
<script setup>
import Card from '@/components/Steps_Bottom.vue';
import {useRouter } from "vue-router";
import Modal from '@/components/Disclaimer.vue';

const router = useRouter();
</script>

<!--NOTE: the disclaimer CLOSES on the test page, but not on this page. why won't it close-->
<template>
  <Modal @close="closeModal"/>
  <h1>Step 1: Select your allergies/dietary restrictions</h1>
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
  components: {
      Modal,
    },
    data() {
      return {
        isModalVisible: true,
      };
    },
    methods: {
      showModal() {
        this.isModalVisible = true;
      },
      closeModal() {
        this.isModalVisible = false;
      }
    },
    data() {
      return {
        items: [
          { label: 'Peanuts', checked: false },
          { label: 'Tree Nuts', checked: false },
          { label: 'Shellfish', checked: false }
        ]
      }
    },
  };
    
</script>

<style>
h1 {
  font-size: large;
  text-align: center;
}
</style>

<!--TODO: implement checklist feature-->
<!--reference: https://www.google.com/search?q=how+to+implement+a+checklist+in+vue&sca_esv=2100fb941db67f3a&ei=6ZkqZ8fcKLqHptQPxqS4kAE&ved=0ahUKEwiH9ZbYnMaJAxW6g4kEHUYSDhIQ4dUDCBA&uact=5&oq=how+to+implement+a+checklist+in+vue&gs_lp=Egxnd3Mtd2l6LXNlcnAiI2hvdyB0byBpbXBsZW1lbnQgYSBjaGVja2xpc3QgaW4gdnVlMgUQIRigATIFECEYoAEyBRAhGKABMgUQIRifBTIFECEYnwUyBRAhGJ8FMgUQIRifBTIFECEYnwVIwQ5QqglYsQpwBHgBkAEAmAGDAaABpAKqAQMyLjG4AQPIAQD4AQGYAgegArECwgIKEAAYsAMY1gQYR8ICBhAAGBYYHsICCxAAGIAEGIYDGIoFwgIIEAAYgAQYogSYAwCIBgGQBgiSBwM2LjGgB8YV&sclient=gws-wiz-serp-->
<!--there are probably much nicer ways to do this-->
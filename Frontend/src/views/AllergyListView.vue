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

  <div class="allergy-container">
    <div class="controls">
      <input class="search-box" v-model="searchQuery" @input="filterAllergies" placeholder="Search allergies...">
      <button class="btn" @click="searchPrev">Prev</button>
      <button class="btn" @click="searchNext">Next</button>
      <span>{{ searchIndex + 1 }}/{{ filteredAllergies.length }}</span>
    </div>
    <div class="actions">
      <button class="btn apply" @click="applyAllAllergies">Apply All</button>
      <button class="btn reset" @click="resetAllAllergies">Reset All</button>
    </div>
    <p>{{ countSelectedAllergies }} allergies applied</p>
    <table>
      <thead>
        <tr>
          <th>Allergy</th>
          <th>Intolerance</th>
          <th>Mild</th>
          <th>Moderate</th>
          <th>Strong</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(allergy, index) in filteredAllergies" :key="allergy.id"
        :class="{ highlighted: index === highlightRow }">
          <td>{{ allergy.name }}</td>
          <td><input type="radio" :value="'intolerance'" v-model="allergy.severity" @click="toggleRadio(allergy, 'intolerance')"></td>
          <td><input type="radio" :value="'mild'" v-model="allergy.severity" @click="toggleRadio(allergy, 'mild')"></td>
          <td><input type="radio" :value="'moderate'" v-model="allergy.severity" @click="toggleRadio(allergy, 'moderate')"></td>
          <td><input type="radio" :value="'strong'" v-model="allergy.severity" @click="toggleRadio(allergy, 'strong')"></td>
        </tr>
      </tbody>
    </table>
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
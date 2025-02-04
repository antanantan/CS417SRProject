<script setup>
import Card from '@/components/Steps_Bottom.vue';
import {useRouter} from "vue-router";
import Modal from "@/components/Disclaimer.vue"
import { ref, computed } from 'vue';
const router = useRouter();

const isModalVisible = ref(true);
const closeModal = (closeandNavigate) => {
  isModalVisible.value = false;
  if (closeandNavigate){ //only navs if disagree stupid { } messed me up for so long
    router.push('/');
  }
};

const allergies = ref([
  { id: 1, name: 'Milk', severity: '', selected: false },
  { id: 2, name: 'Eggs', severity: '', selected: false },
  { id: 3, name: 'Peanuts', severity: '', selected: false },
  { id: 4, name: 'Tree nuts', severity: '', selected: false },
  { id: 5, name: 'Sesame', severity: '', selected: false },
  { id: 6, name: 'Soy', severity: '', selected: false },
  { id: 7, name: 'Fish', severity: '', selected: false },
  { id: 8, name: 'Shellfish', severity: '', selected: false },
  { id: 9, name: 'Wheat', severity: '', selected: false },
  { id: 10, name: 'Triticale', severity: '', selected: false },
  { id: 11, name: 'Celery', severity: '', selected: false },
  { id: 12, name: 'Carrot', severity: '', selected: false },
  { id: 13, name: 'Avocado', severity: '', selected: false },
  { id: 14, name: 'Bell Pepper', severity: '', selected: false },
  { id: 15, name: 'Potato', severity: '', selected: false },
  { id: 16, name: 'Pumpkin', severity: '', selected: false },
  { id: 17, name: 'Mushroom', severity: '', selected: false },
  { id: 18, name: 'Onion', severity: '', selected: false },
  { id: 19, name: 'Mustard', severity: '', selected: false },
  { id: 20, name: 'Spices', severity: '', selected: false },
  { id: 21, name: 'Gluten', severity: '', selected: false }
]);

//search functionality
const searchQuery = ref("");
const filteredAllergies = computed(() => {
  return allergies.value
    ? allergies.value.filter(a =>
    a.name.toLowerCase().includes(searchQuery.value.toLowerCase()))
    : [];
});

// Selecting allergies 
const toggleRadio = (allergy, severity) => {
  allergy.severity = allergy.severity === severity ? "" : severity; 
};

const applyAllAllergies = () => {
  allergies.value.forEach(allergy => {
    if (allergy.severity) {
      allergy.selected = true;
    }
  });
};

const resetAllAllergies = () => {
  allergies.value.forEach(allergy => {
    allergy.severity = "";
    allergy.selected = false;
  });
};

const searchIndex = ref(0);
const highlightRow = ref(0);

const searchNext = () => {
  if (searchIndex.value < filteredAllergies.value.length - 1) {
    searchIndex.value++;
  } else {
    searchIndex.value = 0; // loop back
  }
  highlightRow.value = searchIndex.value;
};

const searchPrev = () => {
  if (searchIndex.value > 0) {
    searchIndex.value--;
  } else {
    searchIndex.value = filteredAllergies.value.length - 1; // loop back
  }
  highlightRow.value = searchIndex.value;
};

</script>

<!--TODO: fix disclaimer why no work-->
<template>
  <Modal v-show="isModalVisible" @close="closeModal"/>

  <h1>Step 1: Select your allergies/dietary restrictions</h1>
      <div>
    <ul v-if="filteredAllergies.length">
      <li v-for="(allergy, index) in filteredAllergies" :key="index">
      </li>
    </ul>
    <p v-else>No allergies found</p>
  </div>

  <div class="allergy-container">
    <div class="controls">
      <input class="search-box" v-model="searchQuery" placeholder="Search allergies...">
      <button class="btn" @click="searchPrev">Prev</button>
      <button class="btn" @click="searchNext">Next</button>
      <span v-if="filteredAllergies.length">{{ searchIndex + 1 }}/{{ filteredAllergies?.length || 0 }}</span> 
      <span v-else>No Allergies found</span>
    </div>
    <div class="actions">
      <button class="btn apply" @click="applyAllAllergies">Apply All</button>
      <button class="btn reset" @click="resetAllAllergies">Reset All</button>
    </div>

    <p>{{ allergies.filter(a => a.selected).length }} allergies applied</p>

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
      <tbody v-if="filteredAllergies.length">
        <tr v-for="(allergy, index) in filteredAllergies" :key="allergy.id"
        :class="{ highlighted: index === highlightRow }">
          <td>{{ allergy.name }}</td>
          <td><input type="radio" value="'intolerance'" v-model="allergy.severity" @change="allergy.selected = !!allergy.severity"</td>
          <td><input type="radio" value="'mild'" v-model="allergy.severity" @change="allergy.selected = !!allergy.severity"></td>
          <td><input type="radio" value="'moderate'" v-model="allergy.severity" @change="allergy.selected = !!allergy.severity"></td>
          <td><input type="radio" value="'strong'" v-model="allergy.severity" @change="allergy.selected = !!allergy.severity"></td>
        </tr>
      </tbody>
    </table>
  </div>

  <Card></Card>
</template>

<!--TODO: we need to take this information and send it to the backend and cross-check it with a mock menu?
          or we really need to figure out where to get a comprehensive allergen database-->
 
<style scoped>
.allergy-container {
  padding: 20px;
  padding-bottom: 100px;
}
.controls, .actions {
  margin-bottom: 10px;
}
.search-box, .btn {
  padding: 8px;
  margin-right: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.btn.apply {
  background-color: #4CAF50; /* Green */
  color: white;
}
.btn.reset {
  background-color: #f44336; /* Red */
  color: white;
}
.highlighted {
  background-color: yellow;
}
</style>

<!--reference: https://www.google.com/search?q=how+to+implement+a+checklist+in+vue&sca_esv=2100fb941db67f3a&ei=6ZkqZ8fcKLqHptQPxqS4kAE&ved=0ahUKEwiH9ZbYnMaJAxW6g4kEHUYSDhIQ4dUDCBA&uact=5&oq=how+to+implement+a+checklist+in+vue&gs_lp=Egxnd3Mtd2l6LXNlcnAiI2hvdyB0byBpbXBsZW1lbnQgYSBjaGVja2xpc3QgaW4gdnVlMgUQIRigATIFECEYoAEyBRAhGKABMgUQIRifBTIFECEYnwUyBRAhGJ8FMgUQIRifBTIFECEYnwVIwQ5QqglYsQpwBHgBkAEAmAGDAaABpAKqAQMyLjG4AQPIAQD4AQGYAgegArECwgIKEAAYsAMY1gQYR8ICBhAAGBYYHsICCxAAGIAEGIYDGIoFwgIIEAAYgAQYogSYAwCIBgGQBgiSBwM2LjGgB8YV&sclient=gws-wiz-serp-->

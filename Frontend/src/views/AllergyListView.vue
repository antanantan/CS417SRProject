<script setup>
import Card from '@/components/Steps_Bottom.vue';
import {useRouter} from "vue-router";
import Modal from "@/components/Disclaimer.vue"

const router = useRouter();

</script>


<!--TODO: fix disclaimer why no work-->
<template>
  <Modal v-show="isModalVisible" @close="closeModal"/>

  <h1>Step 1: Select your allergies/dietary restrictions</h1>
      <div>
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

<!--TODO: we need to take this information and send it to the backend and cross-check it with a mock menu?
          or we really need to figure out where to get a comprehensive allergen database-->

<script>
export default {
  data() {
    return {
      allergies: [
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
      ],
      searchQuery: '',
      filteredAllergies: [],
      highlightRow: 0,
      searchIndex: 0
    };
  },
  computed: {
    countSelectedAllergies() {
      return this.allergies.filter(a => a.severity).length;
    }
  },
  methods: {
    applyAllAllergies() {
      this.allergies.forEach(allergy => {
        if (allergy.severity) {
          allergy.selected = true;
        }
      });
    },
    resetAllAllergies() {
      this.allergies.forEach(allergy => {
        allergy.severity = '';
        allergy.selected = false;
      });
    },
    filterAllergies() {
      this.filteredAllergies = this.allergies.filter(a => a.name.toLowerCase().includes(this.searchQuery.toLowerCase()));
      this.highlightRow = 0;
      this.searchIndex = 0;
    },
    searchNext() {
      if (this.searchIndex < this.filteredAllergies.length - 1) {
        this.searchIndex++;
      } else {
        this.searchIndex = 0; // Loop back to the first item
      }
      this.highlightRow = this.searchIndex;
    },
    searchPrev() {
      if (this.searchIndex > 0) {
        this.searchIndex--;
      } else {
        this.searchIndex = this.filteredAllergies.length - 1; // Loop back to the last item
      }
      this.highlightRow = this.searchIndex;
    },
    toggleRadio(allergy, severity) {
      if (allergy.severity === severity) {
        allergy.severity = ''; // clear the selection
      } else {
        allergy.severity = severity; // select the new value
      }
    }
  },
  mounted() {
    this.filteredAllergies = this.allergies;
  }
}


</script>


<style scoped>
.allergy-container {
  padding: 20px;
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

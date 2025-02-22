<script setup>
import Card from '@/components/Steps_Bottom.vue';
import {useRouter} from "vue-router";
import Modal from "@/components/Disclaimer.vue"
import { ref, computed, onMounted} from 'vue';
import axios from "axios";

const router = useRouter();

// code for handling modal
const isModalVisible = ref(true);
const closeModal = (closeandNavigate) => {
  isModalVisible.value = false;
  if (closeandNavigate){
    router.push('/');
  }
};

// code for pulling allergy list from backend
const allergies = ref([]);
const loadAllergies = async () => {
  const token = localStorage.getItem("jwt"); 
  try {
    const response = await axios.get('http://localhost:5000/generate_list', {
      headers: { Authorization: `Bearer ${token}` }
    });

    allergies.value = response.data.allergies.map(item => ({
      ...item,
      severity: '',  
      selected: false  
    }));
  } catch (error) {
    console.error('Error loading allergies:', error);
  }
};

onMounted(() => {loadAllergies();});

// function to handle saving allergy profile to user.
const saveAllergies = async () => {
  const token = localStorage.getItem("token");; 
  const allergiesData = allergies.value.map(allergy => {
    let scale = null;

// Update the scale based on severity
  if (allergy.severity === 'intolerance') {
    scale = 0;
  } else if (allergy.severity === 'mild') {
    scale = 1;
  } else if (allergy.severity === 'moderate') {
    scale = 2;
  } else if (allergy.severity === 'strong') {
    scale = 3;
  }   
  return {
    name: allergy.name,
    scale: scale
  };
  }).filter(allergy => allergy.scale !== null);
  if (allergiesData.length === 0) {
    console.log("Empty list.");
    return; 
  }


  console.log("Sending this data:", allergiesData);

  try {
    const response = await axios.post('http://localhost:5000/save_allergy', 
      { allergies: allergiesData },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    console.log(response.data.message); 
  } catch (error) {
    console.error('Error saving allergies:', error.response?.data?.message || error.message);
  }
};



//search functionality
const searchQuery = ref("");
const filteredAllergies = computed(() => {
  return allergies.value
    ? allergies.value.filter(a =>
    a.name.toLowerCase().includes(searchQuery.value.toLowerCase()))
    : [];
});


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



// codes used for searching functionality
const searchIndex = ref(0);
const highlightRow = ref(0);
const searchNext = () => {
  if (searchIndex.value < filteredAllergies.value.length - 1) {
    searchIndex.value++;
  } else {
    searchIndex.value = 0; 
  }
  highlightRow.value = searchIndex.value;
};
const searchPrev = () => {
  if (searchIndex.value > 0) {
    searchIndex.value--;
  } else {
    searchIndex.value = filteredAllergies.value.length - 1;
  }
  highlightRow.value = searchIndex.value;
};
</script>

<template>
  <Modal v-show="isModalVisible" @close="closeModal"/>

  <h1>Step 1: Select Your Allergies/Dietary Restrictions</h1>
  

  <div class="allergy-container">
    <div class="controls">
      <input class="search-box" v-model="searchQuery" placeholder="Search allergies...">
      <button class="btn" @click="searchPrev">Prev</button>
      <button class="btn" @click="searchNext">Next</button>
      <span v-if="filteredAllergies.length">{{ searchIndex + 1 }}/{{ filteredAllergies?.length || 0 }}</span> 
      <span v-else>No Allergies Found</span>
    </div>

    <div class="actions">
      <button class="btn apply" @click="applyAllAllergies">Apply All</button>
      <button class="btn reset" @click="resetAllAllergies">Reset All</button>
      <button class="btn save" @click="saveAllergies">Test Save</button>
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
          <td><input type="radio" value="intolerance" v-model="allergy.severity" @change="allergy.selected = allergy.severity != null && allergy.severity !== ''"></td>
          <td><input type="radio" value="mild" v-model="allergy.severity" @change="allergy.selected = allergy.severity != null && allergy.severity !== ''"></td>
          <td><input type="radio" value="moderate" v-model="allergy.severity" @change="allergy.selected = allergy.severity != null && allergy.severity !== ''"></td>
          <td><input type="radio" value="strong" v-model="allergy.severity" @change="allergy.selected = allergy.severity != null && allergy.severity !== ''"></td>
        </tr>
      </tbody>
    </table>
  </div>

  <Card></Card>
</template>
 


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
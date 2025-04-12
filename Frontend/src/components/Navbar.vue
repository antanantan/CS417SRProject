<script setup>
import { RouterLink, useRoute } from 'vue-router';
import { ref, onMounted, watch } from 'vue';
import logo from '@/assets/img/logo.png';
import { Icon } from '@iconify/vue';
import { api, authApi, checkAuthStatus } from "@/api/auth.js";
import AllergyProfileModal from "@/components/AllergyProfileModal.vue";
import { userAllergies, fetchUserAllergies, applyUserAllergySelections } from '@/composables/useUserAllergies.js';
import router from '@/router';

const isActiveLink = (routePath) => {
  const route = useRoute();
  return route.path === routePath;
};

const showFilterModal = ref(false);
const isLoggedIn = ref(false);
const isGuest = ref(false);
const errorMessage = ref('');
const isLoading = ref(true);


const checkAuth = async() => {
  isLoading.value = true;
  errorMessage.value = '';
  try{
    const token = localStorage.getItem('token');
    //no token so logged out 
    if(!token){
      isLoggedIn.value = false;
      isGuest.value = false;
      isLoading.value = false;
      return;
    }
    //checking token in backend
    const authResult = await checkAuthStatus(token);
    if (authResult.authenticated){
      isLoggedIn.value = true;
      isGuest.value = authResult.is_guest;

      // fetches user allergies if authenticated
      if (isLoggedIn.value){
        await fetchUserAllergies().catch(err => {
          console.error('Error fetching user allergies:', err);
          errorMessage.value = 'Failed to fetch user allergies.';
        });
      }
    } else{
        // token invalid or expired
        isLoggedIn.value = false;
        isGuest.value = false;
        localStorage.removeItem('token');
        localStorage.removeItem('is_guest');
      }
  } catch (error) {
      console.error('Error checking auth status:', error);
      isLoggedIn.value = false;
      isGuest.value = false;
      errorMessage.value = 'Failed to check authentication status.';
  } finally {
      isLoading.value = false;
  }
};

// Check auth status on component mount
onMounted(() => {
  checkAuth();
});

// Watch for route changes to refresh auth state
watch(() => router.currentRoute.value.path, (newPath, oldPath) => {
  if (['/login', '/create', '/profile'].includes(oldPath)) {
    checkAuth();
  }
});

const openAllergyModal = () => {
  showFilterModal.value = true;
};

// Logout
const handleLogout = async () => {
  try {
    if (isLoggedIn.value && !isGuest.value) {
      await authApi.post('/auth/logout');
    }
    // clear storage regardless of API success
    localStorage.removeItem('token');
    localStorage.removeItem('is_guest');
    isLoggedIn.value = false;
    isGuest.value = false;
    router.push('/login');
  } catch (error) {
    console.error('Logout error:', error);
    // If API call fails, still clear local storage
    localStorage.removeItem('token');
    localStorage.removeItem('is_guest');
    isLoggedIn.value = false;
    isGuest.value = false;
    router.push('/login');
  }
};

// convert guest account to a regular account
const convertToAccount = async () => {
  try {
    // store route to return after account verification
    const currentPath = router.currentRoute.value.path;
    localStorage.setItem('returnPath', currentPath);
    localStorage.setItem('convertingFromGuest', 'true');

    //get curr allergies to transfer 
    await fetchUserAllergies().catch(err => {
      console.error('Unable to fetch user allergies:', err);
    });

    await router.push('/create');
  } catch (err) {
  console.error('Unable to prepare for account conversion:', err);
  errorMessage.value = "Unable to prepare for account conversion";
  }
};

const continueAsGuest = async () => {
  try {
    const response = await api.post('/auth/guest');
    if (response.status === 200) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('is_guest', 'true');
      isLoggedIn.value = true;
      isGuest.value = true;
      router.push('/allergy_list');
    }
  } catch (err) {
    console.error('Unable to create guest session', err);
    errorMessage.value = "Unable to create guest session";
  }
};

</script>

<template>
  <nav class="bg-green-700 w-full fixed top-0 left-0 z-50 shadow-md">
    <div class="flex h-16 items-center justify-between px-4">
      <div class="flex flex-1 items-center justify-center md:items-stretch md:justify-start">
        <RouterLink class="flex flex-shrink-0 items-center" to="/">
          <img class="h-10 w-auto" :src="logo" alt="Eat Well Logo"/>
          <span class="hidden md:block text-white text-2xl font-bold">
          </span>
        </RouterLink>
        <div class="md:ml-auto">
          <div class="flex items-center space-x-2">
            <!-- Loading indicator -->
            <div v-if="isLoading" class="text-white text-sm">
              Loading...
            </div>
            
            <!-- Error message -->
            <div v-if="errorMessage" class="text-red-200 text-sm mr-2">
              {{ errorMessage }}
            </div>
            
            <!-- Show Guest Mode badge when in guest mode -->
            <div v-if="!isLoading && isGuest" class="bg-yellow-100 text-yellow-800 rounded-full px-3 py-1 text-sm flex items-center mr-2">
              <span>Guest Mode</span>
              <button
                @click="convertToAccount"
                class="ml-2 text-blue-600 hover:text-blue-800 text-xs underline">
                Create Account
              </button>
            </div>
            
            <!-- Show login/signup only if not logged in at all -->
            <template v-if="!isLoading && !isLoggedIn && !isGuest">
              <RouterLink
                to="/login"
                :class="[
                  isActiveLink('/login') ? 'bg-green-900' : 'hover:bg-gray-900 hover:text-white',
                  'text-white',
                  'px-3',
                  'py-2',
                  'rounded-md',
                ]">Log In</RouterLink>
              
              <RouterLink
                to="/create"
                :class="[
                  isActiveLink('/create') ? 'bg-green-900' : 'hover:bg-gray-900 hover:text-white',
                  'text-white',
                  'px-3',
                  'py-2',
                  'rounded-md',
                ]">Sign Up</RouterLink>
              
              <button
                @click="continueAsGuest"
                class="text-white px-3 py-2 rounded-md hover:bg-gray-900">
                Guest
              </button>
            </template>

            <!-- Show logout for both regular users and guests -->
            <button v-if="!isLoading && (isLoggedIn || isGuest)" 
              @click="handleLogout"
              class="text-white px-3 py-2 rounded-md hover:bg-gray-900">
              Logout
            </button>

            <!-- Profile and other buttons - only show when not loading -->
            <RouterLink v-if="!isLoading" to="/profile" class="group rounded-full bg-green-700 text-white hover:bg-white mr-8">
              <Icon icon='mdi:user' class="w-7 h-7 group-hover:text-green-700 m-2"></Icon>
            </RouterLink>

            <button v-if="!isLoading" @click="openAllergyModal" class="group rounded-full bg-green-700 text-white hover:bg-white mr-8">
              <Icon icon='mdi:food-allergy' class="w-7 h-7 group-hover:text-green-700 m-2"></Icon>
            </button>

            <RouterLink v-if="!isLoading" to="/allergy_list" class="group rounded-full bg-green-700 text-white hover:bg-white mr-10">
              <Icon icon='mdi:cart' class="w-7 h-7 group-hover:text-green-700 m-2"></Icon>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </nav>
  <AllergyProfileModal v-model="showFilterModal" @updated="fetchUserAllergies" />
</template>
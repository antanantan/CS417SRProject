<script setup>
import {computed, ref, watch, onMounted} from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';

const route = useRoute();
const router = useRouter();
const isNavigating = ref(false);

const orderState = ref({
    allergiesSelected: false,
    restaurantSelected: false,
    itemsInCart: false
})

// Checks the localstorage for persisted state
onMounted(() => {
    // Try to restore navigation state from localStorage
    const savedState = localStorage.getItem('orderState');
    if (savedState) {
        try {
            const parsedState = JSON.parse(savedState);
            orderState.value = { ...orderState.value, ...parsedState };
        } catch (e) {
            console.error('Failed to parse saved order state:', e);
        }
    }
    
    // Initialize based on current route
    updateStateFromRoute(route.path);
});

// Updates orderState when the route changes
const updateStateFromRoute = (path) => {
    // If on allergies page or beyond, mark allergies as selected
    if (path.includes('/location') || path.includes('/menu') || path.includes('/order')) {
        orderState.value.allergiesSelected = true;
    }
    
    // If on location page or beyond, mark restaurant as selected
    if (path.includes('/menu') || path.includes('/order')) {
        orderState.value.restaurantSelected = true;
    }
    
    // If on order page, mark items as in cart
    if (path.includes('/order')) {
        orderState.value.itemsInCart = true;
    }
    
    localStorage.setItem('orderState', JSON.stringify(orderState.value));
};

// Function to check if a step is completed
const isStepCompleted = (index) => {
    if (index === 0) return orderState.value.allergiesSelected;
    if (index === 1) return orderState.value.restaurantSelected;
    if (index === 2) return orderState.value.itemsInCart;
    return false;
};

const routes = [
    {name: 'Allergies', path: '/allergy_list', icon: 'mdi:peanut-outline' },
    {name: 'Location', path: '/location', icon: 'carbon:location' },
    {name: 'Menu', path: '/menu', icon: 'ph:fork-knife-bold' },
    {name: 'Order', path: '/order', icon: 'mdi:cart-outline' }, 
];

// tab value
const activeTab = ref(0);

// gets index of tab based on current path
const activeTabIndex = (currentPath) => {
    try {
        // Handle the routes with params like /menu/{restaurantId}
        const basePath = '/' + currentPath.split('/')[1];
        
        // find matching route
        const index = routes.findIndex(r => 
            r.path === basePath || basePath.startsWith(r.path)
        );
        
        return index !== -1 ? index : activeTab.value;
    } catch (error) {
        console.error('Error finding active tab:', error);
        return activeTab.value; 
    }
};

// Prevent skipping steps in the process
const isDisabled = computed(() => {
    return routes.map((_, index) => {
        // Allow going to previous tabs or current tab
        if (index <= activeTab.value) return false;

        // Allow going to next tab
        if (index === activeTab.value + 1) return false;
        
        // Disable steps that aren't immediately next or previous
        return true;
    });
});

// Update active tab when route changes
watch(() => route.path, (newPath) => {
    activeTab.value = activeTabIndex(newPath);
    // Also update state based on current route
    updateStateFromRoute(newPath);
}, { immediate: true });

// Also watch for matched routes (handles nested routes)
watch(() => route.matched, () => {
    activeTab.value = activeTabIndex(route.path);
}, { deep: true });

// Navigation function - optimized for single-click response
const navigate = async (tabIndex, event) => {
    // Prevent any default browser behaviors
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    
    // Prevent navigation if already processing a navigation
    if (isNavigating.value) {
        console.log('Navigation already in progress, ignoring click');
        return;
    }
    
    // Set navigating state immediately to prevent double-clicks
    isNavigating.value = true;
    
    try {
        // Don't navigate if already on correct route
        if (activeTab.value === tabIndex) {
            console.log('Already on this tab, no navigation needed');
            isNavigating.value = false;
            return;
        }
        
        // Check if user is trying to skip steps
        if (tabIndex > activeTab.value) {
            if (tabIndex === 1 && !orderState.value.allergiesSelected) {
                alert('Please save your allergies first');
                isNavigating.value = false;
                return;
            } 
            else if (tabIndex === 2 && !orderState.value.restaurantSelected) {
                alert('Please select a restaurant first');
                isNavigating.value = false;
                return;
            }
            else if (tabIndex === 3 && !orderState.value.itemsInCart) {
                alert('Please add items to your cart first');
                isNavigating.value = false;
                return;
            }
        }

        // Get target route
        const targetRoute = routes[tabIndex].path;
        
        // Special case for menu route with restaurant ID
        if (targetRoute === '/menu' && route.path.startsWith('/menu')) {
            // Extract restaurant ID from current path
            const restaurantId = route.params.restaurantId;
            if (restaurantId) {
                console.log(`Navigating to menu with restaurant ID: ${restaurantId}`);
                await router.push(`/menu/${restaurantId}`);
                return;
            }
        } 
        
        // Regular navigation
        console.log(`Navigating to: ${targetRoute}`);
        await router.push(targetRoute);
    } catch (error) {
        console.error('Error navigating to tab:', error);
    } finally {
        // Reset navigation state after a short delay
        // Use shorter delay to improve responsiveness
        setTimeout(() => {
            isNavigating.value = false;
        }, 200); 
    }
};

// Calculate progress for progress bar
const progressPercentage = computed(() => {
    return (activeTab.value / (routes.length - 1)) * 100;
});

const completedSteps = computed(() => {
    return activeTab.value + 1; // Current Step
});

const totalSteps = computed(() => routes.length);

</script>

<template>
    <div class="navigation-container">
        <div class="progress-bar">
            <div 
                class="progress-fill" 
                :style="{ width: `${progressPercentage}%` }"
            ></div>
        </div>
        
        <v-bottom-navigation 
            v-model="activeTab" 
            color="primary" 
            grow 
            class="order-bottom-nav" 
            fixed
            user-select="none"
        >
            <v-btn 
                v-for="(item, index) in routes" 
                :key="item.path"
                @click="(e) => navigate(index, e)"
                :disabled="isDisabled[index]"
                :value="index"
                class="nav-btn"
            >   
                <Icon :icon="item.icon" width="24" height="24" />
                <span>{{ item.name }}</span>
                <Icon 
                    v-if="isStepCompleted(index)" 
                    icon="mdi:check-circle"
                    class="completed-icon green-icon"
                    width="16" 
                    height="16"
                />
            </v-btn>
        </v-bottom-navigation>
    </div>
</template>


<style scoped>
.navigation-container {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  z-index: 10;
  /* Prevent text selection */
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.completed-icon {
  position: absolute;
  top: 8px;
  right: 8px;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background-color: #e0e0e0;
}

.progress-fill {
  height: 100%;
  background-color: #db79cf; 
  transition: width 0.3s ease;
}

.order-bottom-nav {
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
}


.v-btn :deep(.v-btn__content) {
  flex-direction: column;
}


.nav-btn {
  cursor: pointer;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  touch-action: manipulation;
}

@media (max-width: 600px) {
  .v-btn :deep(.v-btn__content span) {
    font-size: 12px;
  }
}

.green-icon {
  color: #4CAF50;
}
</style>
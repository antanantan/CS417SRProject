<script setup>
import {computed, ref, watch, onMounted, onBeforeUnmount} from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';

const route = useRoute();
const router = useRouter();
const isNavigating = ref(false);
let navigationTimeoutId = null;

const orderState = ref({
    allergiesSelected: false,
    restaurantSelected: false,
    itemsInCart: false
})

/**
 * Reset navigation state and clear any timeouts
 * Centralizing this logic prevents race conditions
 */
const resetNavigationState = () => {
    isNavigating.value = false;
    if (navigationTimeoutId) {
        clearTimeout(navigationTimeoutId);
        navigationTimeoutId = null;
    }
};

// Clean up event listeners and timeouts when component is unmounted
onBeforeUnmount(() => {
    resetNavigationState();
});

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

    // Reset navigation state when component mounts
    resetNavigationState();
});

/**
 * Updates orderState when the route changes
 * Handles resetting states appropriately when going backward
 */
const updateStateFromRoute = (path) => {
    if (!path) return; // Guard against empty paths
    
    const currentIndex = activeTabIndex(path)
    
    // Reset state for steps ahead of current step 
    if (currentIndex < 1) {
        orderState.value.restaurantSelected = false;
        orderState.value.itemsInCart = false;
    } else if (currentIndex < 2) {
        orderState.value.itemsInCart = false;
    }
    
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
    
    // Safely persist to localStorage
    try {
        localStorage.setItem('orderState', JSON.stringify(orderState.value));
    } catch (e) {
        console.error('Failed to save order state:', e);
    }
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

// Active tab tracking
const activeTab = ref(0);

/**
 * Gets index of tab based on current path
 * Optimized for performance with error handling
 */
const activeTabIndex = (currentPath) => {
    try {
        if (!currentPath) return 0;
        
        // Handle routes with params like /menu/{restaurantId}
        const basePath = '/' + currentPath.split('/')[1];
        
        // Find matching route
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
    updateStateFromRoute(newPath);
}, { immediate: true });

// Update active tab when route changes for nested routes
watch(() => route.matched, () => {
    activeTab.value = activeTabIndex(route.path);
}, { deep: true });

/**
 * Enhanced navigation function with proper safeguards
 * - Uses single-source-of-truth for navigation state
 * - Implements proper cleanup
 * - Handles edge cases and errors
 */
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
        // Get target route
        const targetRoute = routes[tabIndex].path;
        
        // When clicking the current tab, refresh the route instead of navigating
        if (activeTab.value === tabIndex) {
            console.log('Refreshing current route:', targetRoute);
            
            // Special case for menu route with restaurant ID
            if (targetRoute === '/menu' && route.path.startsWith('/menu')) {
                const restaurantId = route.params.restaurantId;
                if (restaurantId) {
                    await router.replace({ 
                        path: `/menu/${restaurantId}`, 
                        force: true 
                    });
                    updateStateFromRoute(`/menu/${restaurantId}`);
                    resetNavigationState();
                    return;
                }
            }
            
            // Regular refresh for other routes
            await router.replace({ 
                path: targetRoute, 
                force: true 
            });
            updateStateFromRoute(targetRoute);
            resetNavigationState();
            return;
        }
        
        // Check if user is trying to skip steps
        if (tabIndex > activeTab.value) {
            if (tabIndex === 1 && !orderState.value.allergiesSelected) {
                alert('Please save your allergies first');
                resetNavigationState(); // Use resetNavigationState instead of just setting isNavigating
                return;
            } 
            else if (tabIndex === 2 && !orderState.value.restaurantSelected) {
                alert('Please select a restaurant first');
                resetNavigationState();
                return;
            }
            else if (tabIndex === 3 && !orderState.value.itemsInCart) {
                alert('Please add items to your cart first');
                resetNavigationState();
                return;
            }
        }

        // Special case for menu route with restaurant ID
        if (targetRoute === '/menu' && route.path.startsWith('/menu')) {
            // Extract restaurant ID from current path
            const restaurantId = route.params.restaurantId;
            if (restaurantId) {
                console.log(`Navigating to menu with restaurant ID: ${restaurantId}`);
                await router.push(`/menu/${restaurantId}`);
                updateStateFromRoute(`/menu/${restaurantId}`);
                resetNavigationState();
                return;
            }
        } 
        
        // Regular navigation
        console.log(`Navigating to: ${targetRoute}`);
        await router.push(targetRoute);
        updateStateFromRoute(targetRoute);
        resetNavigationState();
    } catch (error) {
        console.error('Error navigating to tab:', error);
        resetNavigationState();
    }
};
</script>

<template>
    <div class="navigation-container">
        <v-bottom-navigation 
            v-model="activeTab" 
            color="primary" 
            grow 
            class="order-bottom-nav" 
            fixed
        >
            <v-btn 
                v-for="(item, index) in routes" 
                :key="item.path"
                @click="(e) => navigate(index, e)"
                :disabled="isDisabled[index] || isNavigating"
                :value="index"
                class="nav-btn"
                v-bind="{ 'data-state': isNavigating ? 'navigating' : 'idle' }"
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
  transition: transform 0.1s ease;
}

.nav-btn:active {
  transform: scale(0.95);
}
.nav-btn[data-state="navigating"] {
  opacity: 0.7;
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
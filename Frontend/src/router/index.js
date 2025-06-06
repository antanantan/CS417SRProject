import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import AllergyListView from '@/views/AllergyListView.vue'
import LocationView from '@/views/LocationView.vue';
import MenuFilter from '@/views/MenuFilter.vue';
import OrderView from '@/views/OrderView.vue';
import PasswordReset from '@/views/PasswordReset.vue';
import Test from '@/views/Test.vue'
import Profile from '@/views/Profile.vue';
import CreateAccount from '@/views/CreateAccount.vue';
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/forgot-password',
      name: 'Forgot',
      component: PasswordReset 
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView 
    },
    {
      path: '/allergy_list',
      name: 'Allergy',
      component: AllergyListView 
    },
    {
      path: '/location',
      name: 'Location',
      component: LocationView 
    },
    {
      path: '/menu/:restaurantId?',
      name: 'Menu',
      component: MenuFilter,
      props: false, 
    },
    {
      path: '/order/:restaurantId?',
      name: 'Order',
      component: OrderView,
      props: false, 
    },
    {
      path: '/test',
      name: 'Test',
      component: Test 
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile 
    },
    {
      path: '/create',
      name: 'Create',
      component: CreateAccount
    },
  ],
})


export default router;

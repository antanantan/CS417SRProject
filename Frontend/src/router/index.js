import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import AllergyListView from '@/views/AllergyListView.vue'
import LocationView from '@/views/LocationView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
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
    }
  ]
})

export default router;

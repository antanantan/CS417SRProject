import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

import 'devextreme/dist/css/dx.light.css';
import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'leaflet/dist/leaflet.css';

const app = createApp(App)

app.use(router)

app.mount('#app')

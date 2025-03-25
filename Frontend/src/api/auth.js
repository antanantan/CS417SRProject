import axios from 'axios';

const api = axios.create({
    baseURL: '/api', // http://localhost didn't work
});

export default api;
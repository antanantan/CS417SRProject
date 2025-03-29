import axios from 'axios';


const api = axios.create({
    baseURL: '/api', // http://localhost didn't work
});


const authApi = axios.create({
    baseURL: '/api',
});

authApi.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
        return config;
    } else {
        return Promise.reject({ response: { status: 401, message: "No token" } });
    }
});

export { api, authApi };
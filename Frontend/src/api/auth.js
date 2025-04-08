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

// Check if user is authenticated as guest or regular user
const checkAuthStatus = async () => {
    try {
        const response = await authApi.get("/auth/check");
        return {
            authenticated: response.data.authenticated,
            isGuest: response.data.is_guest,
            message: response.data.message
        };
    } catch (error) {
        console.error("Auth check error:", error);
        return { 
            authenticated: false, 
            isGuest: false, 
            message: "Authentication check failed" 
        };
    }
};

// Create a guest session
const createGuestSession = async () => {
    try {
        const response = await api.post("/auth/guest");
        if (response.status === 200) {
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('is_guest', 'true');
            return true;
        }
        return false;
    } catch (error) {
        console.error("Guest session creation failed:", error);
        return false;
    }
};

// Logout functionality
const logout = async () => {
    try {
        if (localStorage.getItem('token')) {
            await authApi.post("/auth/logout");
        }
    } catch (error) {
        console.error("Logout error:", error);
    } finally {
        localStorage.removeItem('token');
        localStorage.removeItem('is_guest');
    }
};

export { api, authApi, checkAuthStatus, createGuestSession, logout };
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/services/api";

export const useUserStore = defineStore("user", () => {
  const user = ref(null);
  const token = ref(localStorage.getItem("token"));
  const loading = ref(false);

  const isAuthenticated = computed(() => !!token.value);
  const isAdmin = computed(() => user.value?.is_admin || false);

  const initializeAuth = () => {
    const savedToken = localStorage.getItem("token");
    if (savedToken) {
      token.value = savedToken;
      api.defaults.headers.common["Authorization"] = `Bearer ${savedToken}`;
      loadUser();
    }
  };

  const login = async (credentials) => {
    try {
      loading.value = true;

      const response = await api.post("/auth/login", credentials);
      const { access_token, user: userData } = response.data;

      token.value = access_token;
      user.value = userData;

      // Store token
      localStorage.setItem("token", access_token);
      api.defaults.headers.common["Authorization"] = `Bearer ${access_token}`;

      return userData;
    } finally {
      loading.value = false;
    }
  };

  const register = async (userData) => {
    try {
      loading.value = true;

      const response = await api.post("/auth/register", userData);
      return response.data;
    } finally {
      loading.value = false;
    }
  };

  const logout = () => {
    user.value = null;
    token.value = null;
    localStorage.removeItem("token");
    delete api.defaults.headers.common["Authorization"];
  };

  const loadUser = async () => {
    try {
      const response = await api.get("/auth/me");
      user.value = response.data;
      return response.data;
    } catch (error) {
      // If user fetch fails, clear auth
      logout();
      throw error;
    }
  };

  const updateProfile = async (profileData) => {
    try {
      loading.value = true;

      const response = await api.put("/auth/profile", profileData);
      user.value = { ...user.value, ...response.data };

      return response.data;
    } finally {
      loading.value = false;
    }
  };

  const changePassword = async (passwordData) => {
    try {
      loading.value = true;

      await api.post("/auth/change-password", passwordData);
    } finally {
      loading.value = false;
    }
  };

  return {
    user,
    token,
    loading,
    isAuthenticated,
    isAdmin,
    initializeAuth,
    login,
    register,
    logout,
    loadUser,
    updateProfile,
    changePassword,
  };
});

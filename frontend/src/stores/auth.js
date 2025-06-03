import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/services/api";
import router from "@/router";

export const useAuthStore = defineStore("auth", () => {
  const user = ref(null);
  const accessToken = ref(localStorage.getItem("access_token"));
  const refreshToken = ref(localStorage.getItem("refresh_token"));
  const loading = ref(false);
  const error = ref(null);
  const initialized = ref(false);

  const isAuthenticated = computed(() => !!user.value && !!accessToken.value);
  const isAdmin = computed(() => user.value?.is_admin || false);

  const setTokens = (tokens) => {
    accessToken.value = tokens.access_token;
    refreshToken.value = tokens.refresh_token;
    localStorage.setItem("access_token", tokens.access_token);
    localStorage.setItem("refresh_token", tokens.refresh_token);
    api.defaults.headers.common[
      "Authorization"
    ] = `Bearer ${tokens.access_token}`;
  };

  const clearTokens = () => {
    accessToken.value = null;
    refreshToken.value = null;
    user.value = null;
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    delete api.defaults.headers.common["Authorization"];
  };

  const initialize = async () => {
    if (initialized.value) return;
    
    try {
      if (accessToken.value) {
        api.defaults.headers.common["Authorization"] = `Bearer ${accessToken.value}`;
        await checkAuth();
      }
    } catch (error) {
      console.error("Auth initialization failed:", error);
      clearTokens();
    } finally {
      initialized.value = true;
    }
  };

  const login = async (credentials) => {
    try {
      loading.value = true;
      error.value = null;

      const response = await api.post("/auth/login", credentials);
      const { access_token, refresh_token, user: userData } = response.data;

      setTokens({ access_token, refresh_token });
      user.value = userData;

      return true;
    } catch (err) {
      error.value = err.response?.data?.detail || "Login failed";
      return false;
    } finally {
      loading.value = false;
    }
  };

  const register = async (userData) => {
    try {
      loading.value = true;
      error.value = null;

      await api.post("/auth/register", userData);

      // Auto-login after registration
      return await login({
        email: userData.email,
        password: userData.password,
      });
    } catch (err) {
      error.value = err.response?.data?.detail || "Registration failed";
      return false;
    } finally {
      loading.value = false;
    }
  };

  const logout = async () => {
    clearTokens();
    if (router.currentRoute.value.path !== "/auth/login") {
      router.push({ name: "Login" });
    }
  };

  const checkAuth = async () => {
    if (!accessToken.value) return false;

    try {
      api.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${accessToken.value}`;
      const response = await api.get("/auth/me");
      user.value = response.data;
      return true;
    } catch (err) {
      if (refreshToken.value) {
        return await refreshAccessToken();
      }
      clearTokens();
      return false;
    }
  };

  const refreshAccessToken = async () => {
    try {
      const response = await api.post(
        "/auth/refresh",
        {},
        {
          headers: { Authorization: `Bearer ${refreshToken.value}` },
        }
      );

      const {
        access_token,
        refresh_token: newRefreshToken,
        user: userData,
      } = response.data;
      setTokens({ access_token, refresh_token: newRefreshToken });
      user.value = userData;

      return true;
    } catch (err) {
      clearTokens();
      return false;
    }
  };

  const changePassword = async (passwordData) => {
    try {
      loading.value = true;
      error.value = null;

      await api.post("/auth/change-password", passwordData);
      return true;
    } catch (err) {
      error.value = err.response?.data?.detail || "Password change failed";
      return false;
    } finally {
      loading.value = false;
    }
  };

  const setup2FA = async () => {
    try {
      const response = await api.post("/auth/setup-2fa");
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || "2FA setup failed";
      throw err;
    }
  };

  const disable2FA = async () => {
    try {
      await api.post("/auth/disable-2fa");
      if (user.value) {
        user.value.is_2fa_enabled = false;
      }
      return true;
    } catch (err) {
      error.value = err.response?.data?.detail || "2FA disable failed";
      return false;
    }
  };

  return {
    user,
    loading,
    error,
    initialized,
    isAuthenticated,
    isAdmin,
    initialize,
    login,
    register,
    logout,
    checkAuth,
    changePassword,
    setup2FA,
    disable2FA,
  };
});

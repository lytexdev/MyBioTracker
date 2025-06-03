import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

// Layouts
import AuthLayout from "@/layouts/AuthLayout.vue";
import DashboardLayout from "@/layouts/DashboardLayout.vue";

// Auth views
import Login from "@/views/auth/Login.vue";
import Register from "@/views/auth/Register.vue";

// Main views
import Dashboard from "@/views/Dashboard.vue";
import Nutrition from "@/views/nutrition/Nutrition.vue";
import AddMeal from "@/views/nutrition/AddMeal.vue";
import ScanBarcode from "@/views/nutrition/ScanBarcode.vue";
import Caffeine from "@/views/caffeine/Caffeine.vue";
import AddCaffeine from "@/views/caffeine/AddCaffeine.vue";
import Profile from "@/views/profile/Profile.vue";
import Reports from "@/views/reports/Reports.vue";
import Admin from "@/views/Admin.vue";

const routes = [
  {
    path: "/",
    redirect: "/dashboard",
  },
  {
    path: "/auth",
    component: AuthLayout,
    children: [
      {
        path: "login",
        name: "Login",
        component: Login,
        meta: { guest: true },
      },
      {
        path: "register",
        name: "Register",
        component: Register,
        meta: { guest: true },
      },
    ],
  },
  {
    path: "/",
    component: DashboardLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: "dashboard",
        name: "Dashboard",
        component: Dashboard,
      },
      {
        path: "nutrition",
        name: "Nutrition",
        component: Nutrition,
      },
      {
        path: "nutrition/add-meal",
        name: "AddMeal",
        component: AddMeal,
      },
      {
        path: "nutrition/scan",
        name: "ScanBarcode",
        component: ScanBarcode,
      },
      {
        path: "caffeine",
        name: "Caffeine",
        component: Caffeine,
      },
      {
        path: "caffeine/add",
        name: "AddCaffeine",
        component: AddCaffeine,
      },
      {
        path: "profile",
        name: "Profile",
        component: Profile,
      },
      {
        path: "reports",
        name: "Reports",
        component: Reports,
      },
    ],
  },
  {
    path: "/admin",
    name: "Admin",
    component: Admin,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Route guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  
  // Initialize auth store if not already done
  if (!authStore.initialized) {
    await authStore.initialize();
  }
  
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiresGuest = to.matched.some(record => record.meta.guest);
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin);
  
  if (requiresAuth && !authStore.isAuthenticated) {
    next("/auth/login");
  } else if (requiresGuest && authStore.isAuthenticated) {
    next("/dashboard");
  } else if (requiresAdmin && !authStore.user?.is_admin) {
    next("/dashboard");
  } else {
    next();
  }
});

export default router;

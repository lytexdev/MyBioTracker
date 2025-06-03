import { defineStore } from "pinia";
import { ref, watch } from "vue";

export const useThemeStore = defineStore("theme", () => {
  const darkMode = ref(false);

  const initializeTheme = () => {
    // Check if we're in browser environment
    if (typeof window === 'undefined') return;

    const savedTheme = localStorage.getItem("theme");
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

    if (savedTheme) {
      darkMode.value = savedTheme === "dark";
    } else {
      darkMode.value = prefersDark;
    }

    applyTheme();
    
    // Watch for system theme changes
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    mediaQuery.addEventListener("change", (e) => {
      if (!localStorage.getItem("theme")) {
        darkMode.value = e.matches;
        applyTheme();
      }
    });
  };

  const toggleTheme = () => {
    darkMode.value = !darkMode.value;
    applyTheme();
    
    // Save to localStorage if available
    if (typeof window !== 'undefined') {
      localStorage.setItem("theme", darkMode.value ? "dark" : "light");
    }
  };

  const setTheme = (theme) => {
    darkMode.value = theme === "dark";
    applyTheme();
    
    // Save to localStorage if available
    if (typeof window !== 'undefined') {
      localStorage.setItem("theme", theme);
    }
  };

  const applyTheme = () => {
    // Check if we're in browser environment
    if (typeof window === 'undefined' || typeof document === 'undefined') return;

    if (darkMode.value) {
      document.documentElement.setAttribute("data-theme", "dark");
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.removeAttribute("data-theme");
      document.documentElement.classList.remove("dark");
    }
  };

  return {
    darkMode,
    initializeTheme,
    toggleTheme,
    setTheme,
  };
});

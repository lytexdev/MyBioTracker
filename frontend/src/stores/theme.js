import { defineStore } from "pinia";
import { ref } from "vue";

export const useThemeStore = defineStore("theme", () => {
  const darkMode = ref(false);

  const initTheme = () => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
      darkMode.value = savedTheme === "dark";
    } else {
      darkMode.value = window.matchMedia(
        "(prefers-color-scheme: dark)"
      ).matches;
    }
    updateDocumentClass();
  };

  const toggleTheme = () => {
    darkMode.value = !darkMode.value;
    localStorage.setItem("theme", darkMode.value ? "dark" : "light");
    updateDocumentClass();
  };

  const updateDocumentClass = () => {
    if (darkMode.value) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  };

  return {
    darkMode,
    initTheme,
    toggleTheme,
  };
});

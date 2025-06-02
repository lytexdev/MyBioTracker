import { defineStore } from "pinia";
import { ref } from "vue";

export const useToastStore = defineStore("toast", () => {
  const toasts = ref([]);

  const addToast = (toast) => {
    const id = Date.now() + Math.random();
    const newToast = {
      id,
      type: "info",
      duration: 5000,
      ...toast,
    };

    toasts.value.push(newToast);

    // Auto remove after duration
    if (newToast.duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, newToast.duration);
    }

    return id;
  };

  const removeToast = (id) => {
    const index = toasts.value.findIndex((toast) => toast.id === id);
    if (index > -1) {
      toasts.value.splice(index, 1);
    }
  };

  const success = (message, description = null) => {
    return addToast({
      type: "success",
      message,
      description,
    });
  };

  const error = (message, description = null) => {
    return addToast({
      type: "error",
      message,
      description,
      duration: 7000, // Longer duration for errors
    });
  };

  const warning = (message, description = null) => {
    return addToast({
      type: "warning",
      message,
      description,
    });
  };

  const info = (message, description = null) => {
    return addToast({
      type: "info",
      message,
      description,
    });
  };

  const clear = () => {
    toasts.value = [];
  };

  return {
    toasts,
    addToast,
    removeToast,
    success,
    error,
    warning,
    info,
    clear,
  };
});

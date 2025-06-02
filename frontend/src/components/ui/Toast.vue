<template>
  <div class="toast-container">
    <Transition
      v-for="toast in toasts"
      :key="toast.id"
      name="toast"
      appear
    >
      <div :class="['toast', `toast-${toast.type}`]">
        <div class="toast-icon">
          <Icon :name="getIcon(toast.type)" size="20" />
        </div>
        <div class="toast-content">
          <div class="toast-message">{{ toast.message }}</div>
          <div v-if="toast.description" class="toast-description">
            {{ toast.description }}
          </div>
        </div>
        <button @click="removeToast(toast.id)" class="toast-close">
          <Icon name="x" size="16" />
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useToastStore } from '@/stores/toast'
import Icon from './Icon.vue'

const toastStore = useToastStore()

const toasts = computed(() => toastStore.toasts)

const getIcon = (type) => {
  const icons = {
    success: 'check-circle',
    error: 'alert-circle',
    warning: 'alert-triangle',
    info: 'info'
  }
  return icons[type] || 'info'
}

const removeToast = (id) => {
  toastStore.removeToast(id)
}
</script>

<style lang="scss" scoped>
.toast-container {
  position: fixed;
  top: var(--space-lg);
  right: var(--space-lg);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  max-width: 400px;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: flex-start;
  gap: var(--space-md);
  padding: var(--space-lg);
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  pointer-events: auto;
  min-width: 350px;
  
  &.toast-success {
    border-left: 4px solid var(--success);
    
    .toast-icon {
      color: var(--success);
    }
  }
  
  &.toast-error {
    border-left: 4px solid var(--error);
    
    .toast-icon {
      color: var(--error);
    }
  }
  
  &.toast-warning {
    border-left: 4px solid var(--warning);
    
    .toast-icon {
      color: var(--warning);
    }
  }
  
  &.toast-info {
    border-left: 4px solid var(--info);
    
    .toast-icon {
      color: var(--info);
    }
  }
}

.toast-icon {
  flex-shrink: 0;
  margin-top: 2px;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-message {
  font-weight: 500;
  color: var(--text-primary);
  line-height: 1.4;
}

.toast-description {
  margin-top: var(--space-xs);
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.4;
}

.toast-close {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  border: none;
  background: none;
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
  }
}

// Toast animations
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

@media (max-width: 768px) {
  .toast-container {
    left: var(--space-lg);
    right: var(--space-lg);
    top: var(--space-lg);
  }
  
  .toast {
    min-width: auto;
  }
}
</style>

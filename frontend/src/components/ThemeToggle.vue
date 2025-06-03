<template>
  <button
    @click="toggleTheme"
    class="theme-toggle"
    :class="{ 'theme-toggle--dark': themeStore.darkMode }"
    :title="themeStore.darkMode ? 'Switch to light mode' : 'Switch to dark mode'"
    aria-label="Toggle theme"
  >
    <div class="theme-toggle__track">
      <div class="theme-toggle__thumb">
        <Icon
          v-if="themeStore.darkMode"
          name="moon"
          class="theme-toggle__icon theme-toggle__icon--moon"
        />
        <Icon
          v-else
          name="sun"
          class="theme-toggle__icon theme-toggle__icon--sun"
        />
      </div>
    </div>
  </button>
</template>

<script setup>
import { useThemeStore } from '@/stores/theme'
import Icon from '@/components/ui/Icon.vue'

const themeStore = useThemeStore()

const toggleTheme = () => {
  themeStore.toggleTheme()
}
</script>

<style lang="scss" scoped>
.theme-toggle {
  position: relative;
  width: 3.5rem;
  height: 2rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  border-radius: 1rem;
  transition: var(--transition);

  &:focus {
    outline: none;
    box-shadow: 0 0 0 2px var(--primary);
  }

  &:hover {
    transform: scale(1.05);
  }

  &__track {
    width: 100%;
    height: 100%;
    background: var(--bg-secondary);
    border: 2px solid var(--border);
    border-radius: 1rem;
    position: relative;
    transition: var(--transition);
    overflow: hidden;

    .theme-toggle--dark & {
      background: var(--bg-tertiary);
      border-color: var(--primary);
    }
  }

  &__thumb {
    position: absolute;
    top: 2px;
    left: 2px;
    width: 1.25rem;
    height: 1.25rem;
    background: var(--bg-primary);
    border-radius: 50%;
    transition: var(--transition);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: var(--shadow-sm);

    .theme-toggle--dark & {
      transform: translateX(1.5rem);
      background: var(--primary);
    }
  }

  &__icon {
    width: 0.75rem;
    height: 0.75rem;
    transition: var(--transition);

    &--sun {
      color: #f59e0b;
    }

    &--moon {
      color: #ffffff;
    }
  }
}

// Responsive design
@media (max-width: 768px) {
  .theme-toggle {
    width: 3rem;
    height: 1.75rem;

    &__thumb {
      width: 1rem;
      height: 1rem;

      .theme-toggle--dark & {
        transform: translateX(1.25rem);
      }
    }

    &__icon {
      width: 0.625rem;
      height: 0.625rem;
    }
  }
}
</style> 
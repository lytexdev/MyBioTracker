<template>
  <div class="language-switcher" ref="switcherRef">
    <button 
      @click="toggleDropdown" 
      class="language-button"
      :class="{ active: isOpen }"
    >
      <span class="current-flag">{{ currentLanguage.flag }}</span>
      <span class="current-name">{{ currentLanguage.name }}</span>
      <Icon 
        name="chevron-down" 
        size="16" 
        class="chevron"
        :class="{ rotated: isOpen }"
      />
    </button>
    
    <Transition name="dropdown">
      <div v-if="isOpen" class="language-dropdown">
        <button
          v-for="locale in availableLocales"
          :key="locale.code"
          @click="switchLanguage(locale.code)"
          class="language-option"
          :class="{ active: locale.code === currentLocale }"
        >
          <span class="flag">{{ locale.flag }}</span>
          <span class="name">{{ locale.name }}</span>
          <Icon 
            v-if="locale.code === currentLocale" 
            name="check" 
            size="16" 
            class="check-icon"
          />
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { availableLocales, setLocale, getCurrentLocale } from '@/i18n'
import Icon from './Icon.vue'

const { locale } = useI18n()

const isOpen = ref(false)
const switcherRef = ref(null)

const currentLocale = computed(() => getCurrentLocale())

const currentLanguage = computed(() => {
  return availableLocales.find(l => l.code === currentLocale.value) || availableLocales[0]
})

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const switchLanguage = (localeCode) => {
  setLocale(localeCode)
  isOpen.value = false
}

const handleClickOutside = (event) => {
  if (switcherRef.value && !switcherRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style lang="scss" scoped>
.language-switcher {
  position: relative;
  display: inline-block;
}

.language-button {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text-primary);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all var(--transition);
  min-width: 120px;
  
  &:hover {
    background: var(--bg-tertiary);
    border-color: var(--border-hover);
  }
  
  &.active {
    background: var(--bg-tertiary);
    border-color: var(--primary);
  }
  
  .current-flag {
    font-size: 1.1rem;
  }
  
  .current-name {
    flex: 1;
    text-align: left;
    font-weight: 500;
  }
  
  .chevron {
    transition: transform var(--transition);
    color: var(--text-secondary);
    
    &.rotated {
      transform: rotate(180deg);
    }
  }
}

.language-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: var(--space-xs);
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  z-index: 1000;
  overflow: hidden;
}

.language-option {
  width: 100%;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-size: 0.875rem;
  cursor: pointer;
  transition: background var(--transition);
  
  &:hover {
    background: var(--bg-secondary);
  }
  
  &.active {
    background: var(--primary-light);
    color: var(--primary);
    font-weight: 500;
  }
  
  .flag {
    font-size: 1.1rem;
    width: 20px;
    text-align: center;
  }
  
  .name {
    flex: 1;
    text-align: left;
  }
  
  .check-icon {
    color: var(--primary);
  }
}

// Dropdown Animation
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from {
  opacity: 0;
  transform: translateY(-8px) scale(0.95);
}

.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.95);
}

// Responsive
@media (max-width: 768px) {
  .language-button {
    min-width: 100px;
    
    .current-name {
      display: none;
    }
  }
  
  .language-dropdown {
    left: auto;
    right: 0;
    min-width: 150px;
  }
}
</style> 
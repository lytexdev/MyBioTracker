<template>
  <div class="step-container">
    <div class="step-header">
      <h2>Geschlecht auswählen</h2>
      <p>Wir benötigen diese Information für eine präzise Berechnung Ihres Kalorienbedarfs.</p>
    </div>

    <div class="gender-options">
      <div 
        v-for="option in onboardingStore.genderOptions" 
        :key="option.value"
        class="gender-card"
        :class="{ 'selected': onboardingStore.formData.gender === option.value }"
        @click="selectGender(option.value)"
      >
        <div class="gender-icon">
          <Icon 
            :name="getGenderIcon(option.value)" 
            size="32" 
          />
        </div>
        <div class="gender-label">
          {{ option.label }}
        </div>
      </div>
    </div>

    <div v-if="onboardingStore.errors.gender" class="field-error">
      {{ onboardingStore.errors.gender }}
    </div>
  </div>
</template>

<script setup>
import { useOnboardingStore } from '@/stores/onboarding'
import Icon from '@/components/ui/Icon.vue'

const onboardingStore = useOnboardingStore()

const selectGender = (value) => {
  onboardingStore.updateFormData('gender', value)
}

const getGenderIcon = (gender) => {
  switch (gender) {
    case 'male': return 'user'
    case 'female': return 'user'
    case 'diverse': return 'user'
    default: return 'user'
  }
}
</script>

<style lang="scss" scoped>
.step-container {
  width: 100%;
  max-width: 500px;
  text-align: center;
}

.step-header {
  margin-bottom: var(--space-2xl);
  
  h2 {
    margin-bottom: var(--space-md);
    color: var(--text-primary);
    font-size: 1.75rem;
    font-weight: 600;
  }
  
  p {
    color: var(--text-secondary);
    font-size: 1rem;
    line-height: 1.5;
  }
}

.gender-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: var(--space-lg);
  margin-bottom: var(--space-xl);
}

.gender-card {
  padding: var(--space-xl);
  border: 2px solid var(--border);
  border-radius: var(--radius-lg);
  background: var(--bg-primary);
  cursor: pointer;
  transition: var(--transition);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-md);
  
  &:hover {
    border-color: var(--primary);
    background: var(--bg-secondary);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  &.selected {
    border-color: var(--primary);
    background: var(--primary-light);
    background: rgba(34, 197, 94, 0.1);
    
    .gender-icon {
      color: var(--primary);
    }
    
    .gender-label {
      color: var(--primary);
      font-weight: 600;
    }
  }
}

.gender-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  transition: var(--transition);
}

.gender-label {
  font-size: 1rem;
  font-weight: 500;
  color: var(--text-primary);
  transition: var(--transition);
}

.field-error {
  color: var(--error);
  font-size: 0.875rem;
  text-align: center;
  margin-top: var(--space-md);
}

// Mobile Responsiveness
@media (max-width: 480px) {
  .gender-options {
    grid-template-columns: 1fr;
    gap: var(--space-md);
  }
  
  .gender-card {
    padding: var(--space-lg);
  }
  
  .gender-icon {
    width: 50px;
    height: 50px;
  }
  
  .step-header {
    h2 {
      font-size: 1.5rem;
    }
    
    p {
      font-size: 0.875rem;
    }
  }
}
</style> 
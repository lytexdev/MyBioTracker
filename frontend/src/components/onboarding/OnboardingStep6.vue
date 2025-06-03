<template>
  <div class="step-container">
    <div class="step-header">
      <h2>Ihr Ziel</h2>
      <p>Was möchten Sie mit MyBioTracker erreichen? Dies hilft uns bei personalisierten Empfehlungen.</p>
    </div>

    <div class="goal-options">
      <div 
        v-for="option in onboardingStore.goalOptions" 
        :key="option.value"
        class="goal-card"
        :class="{ 'selected': onboardingStore.formData.goal === option.value }"
        @click="selectGoal(option.value)"
      >
        <div class="goal-icon">
          <Icon 
            :name="getGoalIcon(option.value)" 
            size="28" 
          />
        </div>
        <div class="goal-label">
          {{ option.label }}
        </div>
        <div class="goal-description">
          {{ getGoalDescription(option.value) }}
        </div>
      </div>
    </div>

    <div v-if="onboardingStore.errors.goal" class="field-error">
      {{ onboardingStore.errors.goal }}
    </div>
  </div>
</template>

<script setup>
import { useOnboardingStore } from '@/stores/onboarding'
import Icon from '@/components/ui/Icon.vue'

const onboardingStore = useOnboardingStore()

const selectGoal = (value) => {
  onboardingStore.updateFormData('goal', value)
}

const getGoalIcon = (goal) => {
  switch (goal) {
    case 'lose_weight': return 'trending-down'
    case 'gain_weight': return 'trending-up'
    case 'maintain_weight': return 'minus'
    case 'build_muscle': return 'activity'
    case 'stay_fit': return 'heart'
    default: return 'target'
  }
}

const getGoalDescription = (goal) => {
  switch (goal) {
    case 'lose_weight': return 'Gesund und nachhaltig Gewicht reduzieren'
    case 'gain_weight': return 'Kontrolliert an Gewicht zunehmen'
    case 'maintain_weight': return 'Aktuelles Gewicht halten'
    case 'build_muscle': return 'Muskelmasse aufbauen und stärker werden'
    case 'stay_fit': return 'Gesunde Ernährung und Fitness beibehalten'
    default: return ''
  }
}
</script>

<style lang="scss" scoped>
.step-container {
  width: 100%;
  max-width: 600px;
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

.goal-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-lg);
  margin-bottom: var(--space-xl);
}

.goal-card {
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
  text-align: center;
  
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
    
    .goal-icon {
      background: var(--primary);
      color: white;
    }
    
    .goal-label {
      color: var(--primary);
      font-weight: 600;
    }
  }
}

.goal-icon {
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

.goal-label {
  font-size: 1.125rem;
  font-weight: 500;
  color: var(--text-primary);
  transition: var(--transition);
}

.goal-description {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.4;
}

.field-error {
  color: var(--error);
  font-size: 0.875rem;
  text-align: center;
  margin-top: var(--space-md);
}

// Mobile Responsiveness
@media (max-width: 768px) {
  .goal-options {
    grid-template-columns: 1fr;
    gap: var(--space-md);
  }
}

@media (max-width: 480px) {
  .goal-card {
    padding: var(--space-lg);
  }
  
  .goal-icon {
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
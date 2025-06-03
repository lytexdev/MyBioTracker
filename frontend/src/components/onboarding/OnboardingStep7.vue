<template>
  <div class="step-container">
    <div class="step-header">
      <h2>Aktivitätslevel</h2>
      <p>Wie aktiv sind Sie im Alltag? Dies beeinflusst Ihren täglichen Kalorienbedarf erheblich.</p>
    </div>

    <div class="activity-options">
      <div 
        v-for="option in onboardingStore.activityLevelOptions" 
        :key="option.value"
        class="activity-card"
        :class="{ 'selected': onboardingStore.formData.activityLevel === option.value }"
        @click="selectActivityLevel(option.value)"
      >
        <div class="activity-header">
          <div class="activity-icon">
            <Icon 
              :name="getActivityIcon(option.value)" 
              size="24" 
            />
          </div>
          <div class="activity-factor">
            Faktor: {{ option.factor }}
          </div>
        </div>
        <div class="activity-label">
          {{ option.label.split('(')[0].trim() }}
        </div>
        <div class="activity-description">
          {{ getActivityDescription(option.value) }}
        </div>
      </div>
    </div>

    <div v-if="onboardingStore.errors.activityLevel" class="field-error">
      {{ onboardingStore.errors.activityLevel }}
    </div>
  </div>
</template>

<script setup>
import { useOnboardingStore } from '@/stores/onboarding'
import Icon from '@/components/ui/Icon.vue'

const onboardingStore = useOnboardingStore()

const selectActivityLevel = (value) => {
  onboardingStore.updateFormData('activityLevel', value)
}

const getActivityIcon = (level) => {
  switch (level) {
    case 'sedentary': return 'device-desktop'
    case 'lightly_active': return 'walk'
    case 'moderately_active': return 'bike'
    case 'very_active': return 'run'
    case 'extremely_active': return 'flame'
    default: return 'activity'
  }
}

const getActivityDescription = (level) => {
  switch (level) {
    case 'sedentary': return 'Bürojob, wenig Bewegung, kein Sport'
    case 'lightly_active': return 'Leichte Aktivität oder Sport 1-3x pro Woche'
    case 'moderately_active': return 'Moderate Aktivität oder Sport 3-5x pro Woche'
    case 'very_active': return 'Intensive Aktivität oder Sport 6-7x pro Woche'
    case 'extremely_active': return 'Sehr intensive Aktivität, körperliche Arbeit oder 2x täglich Sport'
    default: return ''
  }
}
</script>

<style lang="scss" scoped>
.step-container {
  width: 100%;
  max-width: 700px;
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

.activity-options {
  display: grid;
  gap: var(--space-md);
  margin-bottom: var(--space-xl);
}

.activity-card {
  padding: var(--space-lg);
  border: 2px solid var(--border);
  border-radius: var(--radius-lg);
  background: var(--bg-primary);
  cursor: pointer;
  transition: var(--transition);
  text-align: left;
  
  &:hover {
    border-color: var(--primary);
    background: var(--bg-secondary);
    transform: translateY(-1px);
    box-shadow: var(--shadow-sm);
  }
  
  &.selected {
    border-color: var(--primary);
    background: var(--primary-light);
    background: rgba(34, 197, 94, 0.1);
    
    .activity-icon {
      background: var(--primary);
      color: white;
    }
    
    .activity-label {
      color: var(--primary);
      font-weight: 600;
    }
    
    .activity-factor {
      background: var(--primary);
      color: white;
    }
  }
}

.activity-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-md);
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  transition: var(--transition);
}

.activity-factor {
  font-size: 0.75rem;
  font-weight: 600;
  padding: var(--space-xs) var(--space-sm);
  background: var(--bg-secondary);
  color: var(--text-secondary);
  border-radius: var(--radius);
  transition: var(--transition);
}

.activity-label {
  font-size: 1rem;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: var(--space-sm);
  transition: var(--transition);
}

.activity-description {
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
@media (max-width: 480px) {
  .activity-card {
    padding: var(--space-md);
  }
  
  .activity-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-sm);
  }
  
  .activity-icon {
    width: 35px;
    height: 35px;
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
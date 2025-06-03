<template>
  <div class="step-container">
    <div class="step-header">
      <h2>Geburtsdatum</h2>
      <p>Ihr Alter ist wichtig für die Berechnung Ihres Grundumsatzes und Kalorienbedarfs.</p>
    </div>

    <div class="form-group">
      <label for="birthDate" class="form-label">
        Geburtsdatum
      </label>
      <input
        id="birthDate"
        type="date"
        :value="onboardingStore.formData.birthDate"
        @input="updateBirthDate"
        class="form-input date-input"
        :class="{ 'error': onboardingStore.errors.birthDate }"
        :max="maxDate"
        :min="minDate"
      />
      
      <div v-if="calculatedAge" class="age-display">
        Ihr Alter: {{ calculatedAge }} Jahre
      </div>
      
      <div v-if="onboardingStore.errors.birthDate" class="field-error">
        {{ onboardingStore.errors.birthDate }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useOnboardingStore } from '@/stores/onboarding'

const onboardingStore = useOnboardingStore()

const updateBirthDate = (event) => {
  onboardingStore.updateFormData('birthDate', event.target.value)
}

const maxDate = computed(() => {
  const today = new Date()
  const thirteenYearsAgo = new Date(today.getFullYear() - 13, today.getMonth(), today.getDate())
  return thirteenYearsAgo.toISOString().split('T')[0]
})

const minDate = computed(() => {
  const today = new Date()
  const oneHundredTwentyYearsAgo = new Date(today.getFullYear() - 120, today.getMonth(), today.getDate())
  return oneHundredTwentyYearsAgo.toISOString().split('T')[0]
})

const calculatedAge = computed(() => {
  if (!onboardingStore.formData.birthDate) return null
  
  const today = new Date()
  const birthDate = new Date(onboardingStore.formData.birthDate)
  let age = today.getFullYear() - birthDate.getFullYear()
  const monthDiff = today.getMonth() - birthDate.getMonth()
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--
  }
  
  return age
})
</script>

<style lang="scss" scoped>
.step-container {
  width: 100%;
  max-width: 400px;
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

.form-group {
  text-align: left;
}

.form-label {
  display: block;
  margin-bottom: var(--space-sm);
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.date-input {
  width: 100%;
  padding: var(--space-lg);
  border: 2px solid var(--border);
  border-radius: var(--radius-lg);
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 1rem;
  transition: var(--transition);
  
  &:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
  }
  
  &.error {
    border-color: var(--error);
  }
  
  // Custom date input styling
  &::-webkit-calendar-picker-indicator {
    background-color: var(--primary);
    border-radius: 3px;
    cursor: pointer;
    padding: 2px;
  }
}

.age-display {
  margin-top: var(--space-md);
  padding: var(--space-md);
  background: var(--bg-secondary);
  border-radius: var(--radius);
  color: var(--text-primary);
  font-weight: 500;
  text-align: center;
  border: 1px solid var(--border);
}

.field-error {
  color: var(--error);
  font-size: 0.875rem;
  margin-top: var(--space-sm);
}

// Mobile Responsiveness
@media (max-width: 480px) {
  .step-header {
    h2 {
      font-size: 1.5rem;
    }
    
    p {
      font-size: 0.875rem;
    }
  }
  
  .date-input {
    padding: var(--space-md);
  }
}
</style> 
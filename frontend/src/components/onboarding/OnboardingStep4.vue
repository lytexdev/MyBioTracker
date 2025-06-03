<template>
  <div class="step-container">
    <div class="step-header">
      <h2>Aktuelles Gewicht</h2>
      <p>Ihr Gewicht wird für die Berechnung Ihres BMI und Kalorienbedarfs verwendet.</p>
    </div>

    <div class="form-group">
      <label for="weight" class="form-label">
        Gewicht in kg
      </label>
      <div class="input-wrapper">
        <input
          id="weight"
          type="number"
          :value="onboardingStore.formData.weight"
          @input="updateWeight"
          class="form-input number-input"
          :class="{ 'error': onboardingStore.errors.weight }"
          placeholder="70"
          min="30"
          max="300"
          step="0.1"
        />
        <span class="input-suffix">kg</span>
      </div>
      
      <div class="weight-slider">
        <input
          type="range"
          :value="onboardingStore.formData.weight || 70"
          @input="updateWeightFromSlider"
          min="30"
          max="200"
          class="slider"
        />
        <div class="slider-labels">
          <span>30 kg</span>
          <span>200 kg</span>
        </div>
      </div>
      
      <div v-if="bmiPreview" class="bmi-preview">
        <div class="bmi-value">
          BMI: {{ bmiPreview.value }}
        </div>
        <div class="bmi-category" :class="bmiPreview.categoryClass">
          {{ bmiPreview.category }}
        </div>
      </div>
      
      <div v-if="onboardingStore.errors.weight" class="field-error">
        {{ onboardingStore.errors.weight }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useOnboardingStore } from '@/stores/onboarding'

const onboardingStore = useOnboardingStore()

const updateWeight = (event) => {
  const value = event.target.value
  onboardingStore.updateFormData('weight', value ? parseFloat(value) : '')
}

const updateWeightFromSlider = (event) => {
  const value = parseFloat(event.target.value)
  onboardingStore.updateFormData('weight', value)
}

const bmiPreview = computed(() => {
  const weight = onboardingStore.formData.weight
  const height = onboardingStore.formData.height
  
  if (!weight || !height) return null
  
  const heightInMeters = height / 100
  const bmi = weight / (heightInMeters * heightInMeters)
  const bmiRounded = Math.round(bmi * 10) / 10
  
  let category = ''
  let categoryClass = ''
  
  if (bmi < 18.5) {
    category = 'Untergewicht'
    categoryClass = 'underweight'
  } else if (bmi < 25) {
    category = 'Normalgewicht'
    categoryClass = 'normal'
  } else if (bmi < 30) {
    category = 'Übergewicht'
    categoryClass = 'overweight'
  } else {
    category = 'Adipositas'
    categoryClass = 'obese'
  }
  
  return {
    value: bmiRounded,
    category,
    categoryClass
  }
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

.input-wrapper {
  position: relative;
  margin-bottom: var(--space-lg);
}

.number-input {
  width: 100%;
  padding: var(--space-lg);
  padding-right: 3rem;
  border: 2px solid var(--border);
  border-radius: var(--radius-lg);
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 1.125rem;
  font-weight: 500;
  text-align: center;
  transition: var(--transition);
  
  &:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
  }
  
  &.error {
    border-color: var(--error);
  }
  
  &::placeholder {
    color: var(--text-muted);
  }
}

.input-suffix {
  position: absolute;
  right: var(--space-lg);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
  font-weight: 500;
  pointer-events: none;
}

.weight-slider {
  margin-bottom: var(--space-lg);
}

.slider {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: var(--border);
  outline: none;
  appearance: none;
  cursor: pointer;
  
  &::-webkit-slider-thumb {
    appearance: none;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: var(--primary);
    cursor: pointer;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
    
    &:hover {
      transform: scale(1.1);
      box-shadow: var(--shadow-md);
    }
  }
  
  &::-moz-range-thumb {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: var(--primary);
    cursor: pointer;
    border: none;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
    
    &:hover {
      transform: scale(1.1);
      box-shadow: var(--shadow-md);
    }
  }
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  margin-top: var(--space-sm);
  font-size: 0.75rem;
  color: var(--text-muted);
}

.bmi-preview {
  padding: var(--space-lg);
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  text-align: center;
  margin-bottom: var(--space-lg);
}

.bmi-value {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--space-sm);
}

.bmi-category {
  font-size: 0.875rem;
  font-weight: 500;
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius);
  display: inline-block;
  
  &.underweight {
    background: rgba(59, 130, 246, 0.1);
    color: #3b82f6;
  }
  
  &.normal {
    background: rgba(34, 197, 94, 0.1);
    color: var(--primary);
  }
  
  &.overweight {
    background: rgba(245, 158, 11, 0.1);
    color: #f59e0b;
  }
  
  &.obese {
    background: rgba(239, 68, 68, 0.1);
    color: var(--error);
  }
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
  
  .number-input {
    padding: var(--space-md);
    padding-right: 2.5rem;
    font-size: 1rem;
  }
  
  .input-suffix {
    right: var(--space-md);
  }
  
  .bmi-preview {
    padding: var(--space-md);
  }
}
</style> 
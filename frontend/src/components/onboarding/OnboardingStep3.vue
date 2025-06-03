<template>
  <div class="step-container">
    <div class="step-header">
      <h2>Körpergröße</h2>
      <p>Ihre Größe wird für die Berechnung Ihres BMI und Kalorienbedarfs benötigt.</p>
    </div>

    <div class="form-group">
      <label for="height" class="form-label">
        Größe in cm
      </label>
      <div class="input-wrapper">
        <input
          id="height"
          type="number"
          :value="onboardingStore.formData.height"
          @input="updateHeight"
          class="form-input number-input"
          :class="{ 'error': onboardingStore.errors.height }"
          placeholder="175"
          min="100"
          max="250"
        />
        <span class="input-suffix">cm</span>
      </div>
      
      <div class="height-slider">
        <input
          type="range"
          :value="onboardingStore.formData.height || 175"
          @input="updateHeightFromSlider"
          min="100"
          max="250"
          class="slider"
        />
        <div class="slider-labels">
          <span>100 cm</span>
          <span>250 cm</span>
        </div>
      </div>
      
      <div v-if="onboardingStore.errors.height" class="field-error">
        {{ onboardingStore.errors.height }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { useOnboardingStore } from '@/stores/onboarding'

const onboardingStore = useOnboardingStore()

const updateHeight = (event) => {
  const value = event.target.value
  onboardingStore.updateFormData('height', value ? parseInt(value) : '')
}

const updateHeightFromSlider = (event) => {
  const value = parseInt(event.target.value)
  onboardingStore.updateFormData('height', value)
}
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

.height-slider {
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
}
</style> 
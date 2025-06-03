<template>
  <div class="step-container">
    <div class="step-header">
      <h2>Körperfettanteil</h2>
      <p>Optional: Falls bekannt, hilft uns Ihr Körperfettanteil bei präziseren Berechnungen.</p>
    </div>

    <div class="form-group">
      <label for="bodyFat" class="form-label">
        Körperfettanteil in % (optional)
      </label>
      <div class="input-wrapper">
        <input
          id="bodyFat"
          type="number"
          :value="onboardingStore.formData.bodyFat"
          @input="updateBodyFat"
          class="form-input number-input"
          :class="{ 'error': onboardingStore.errors.bodyFat }"
          placeholder="15"
          min="3"
          max="50"
          step="0.1"
        />
        <span class="input-suffix">%</span>
      </div>
      
      <div class="body-fat-info">
        <h4>Orientierungswerte:</h4>
        <div class="info-grid">
          <div class="info-item">
            <strong>Männer:</strong>
            <div class="ranges">
              <span class="range essential">Essential: 2-5%</span>
              <span class="range athlete">Athletisch: 6-13%</span>
              <span class="range fitness">Fitness: 14-17%</span>
              <span class="range average">Durchschnitt: 18-24%</span>
            </div>
          </div>
          <div class="info-item">
            <strong>Frauen:</strong>
            <div class="ranges">
              <span class="range essential">Essential: 10-13%</span>
              <span class="range athlete">Athletisch: 14-20%</span>
              <span class="range fitness">Fitness: 21-24%</span>
              <span class="range average">Durchschnitt: 25-31%</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="skip-option">
        <button 
          type="button" 
          @click="skipBodyFat"
          class="btn btn-outline skip-button"
        >
          Überspringen
        </button>
      </div>
      
      <div v-if="onboardingStore.errors.bodyFat" class="field-error">
        {{ onboardingStore.errors.bodyFat }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { useOnboardingStore } from '@/stores/onboarding'

const onboardingStore = useOnboardingStore()

const updateBodyFat = (event) => {
  const value = event.target.value
  onboardingStore.updateFormData('bodyFat', value ? parseFloat(value) : '')
}

const skipBodyFat = () => {
  onboardingStore.updateFormData('bodyFat', '')
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
  margin-bottom: var(--space-xl);
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

.body-fat-info {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  margin-bottom: var(--space-xl);
  border: 1px solid var(--border);
  
  h4 {
    margin-bottom: var(--space-md);
    color: var(--text-primary);
    font-size: 1rem;
    font-weight: 600;
  }
}

.info-grid {
  display: grid;
  gap: var(--space-lg);
  
  @media (min-width: 480px) {
    grid-template-columns: 1fr 1fr;
  }
}

.info-item {
  strong {
    display: block;
    margin-bottom: var(--space-sm);
    color: var(--text-primary);
    font-size: 0.875rem;
  }
}

.ranges {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.range {
  font-size: 0.75rem;
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius);
  
  &.essential {
    background: rgba(59, 130, 246, 0.1);
    color: #3b82f6;
  }
  
  &.athlete {
    background: rgba(34, 197, 94, 0.1);
    color: var(--primary);
  }
  
  &.fitness {
    background: rgba(245, 158, 11, 0.1);
    color: #f59e0b;
  }
  
  &.average {
    background: rgba(156, 163, 175, 0.1);
    color: var(--text-secondary);
  }
}

.skip-option {
  text-align: center;
  margin-bottom: var(--space-lg);
}

.skip-button {
  min-width: 150px;
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
  
  .body-fat-info {
    padding: var(--space-md);
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style> 
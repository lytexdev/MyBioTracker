<template>
  <div class="step-container">
    <div class="step-header">
      <h2>Zielgewicht</h2>
      <p>Optional: Haben Sie ein spezifisches Gewichtsziel? Dies hilft bei der Fortschrittsverfolgung.</p>
    </div>

    <div class="form-group">
      <label for="targetWeight" class="form-label">
        Zielgewicht in kg (optional)
      </label>
      <div class="input-wrapper">
        <input
          id="targetWeight"
          type="number"
          :value="onboardingStore.formData.targetWeight"
          @input="updateTargetWeight"
          class="form-input number-input"
          :class="{ 'error': onboardingStore.errors.targetWeight }"
          placeholder="65"
          min="30"
          max="300"
          step="0.1"
        />
        <span class="input-suffix">kg</span>
      </div>
      
      <div class="skip-option">
        <button 
          type="button" 
          @click="skipTargetWeight"
          class="btn btn-outline skip-button"
        >
          Überspringen
        </button>
      </div>
      
      <div v-if="onboardingStore.errors.targetWeight" class="field-error">
        {{ onboardingStore.errors.targetWeight }}
      </div>
    </div>

    <!-- Profile Summary -->
    <div class="profile-summary">
      <h3>Ihr Profil im Überblick</h3>
      <div class="summary-grid">
        <div class="summary-item">
          <div class="summary-label">Geschlecht</div>
          <div class="summary-value">{{ getGenderLabel() }}</div>
        </div>
        
        <div class="summary-item">
          <div class="summary-label">Alter</div>
          <div class="summary-value">{{ calculatedAge }} Jahre</div>
        </div>
        
        <div class="summary-item">
          <div class="summary-label">Größe</div>
          <div class="summary-value">{{ onboardingStore.formData.height }} cm</div>
        </div>
        
        <div class="summary-item">
          <div class="summary-label">Gewicht</div>
          <div class="summary-value">{{ onboardingStore.formData.weight }} kg</div>
        </div>
        
        <div v-if="onboardingStore.formData.bodyFat" class="summary-item">
          <div class="summary-label">Körperfett</div>
          <div class="summary-value">{{ onboardingStore.formData.bodyFat }}%</div>
        </div>
        
        <div class="summary-item">
          <div class="summary-label">Ziel</div>
          <div class="summary-value">{{ getGoalLabel() }}</div>
        </div>
        
        <div class="summary-item">
          <div class="summary-label">Aktivität</div>
          <div class="summary-value">{{ getActivityLabel() }}</div>
        </div>
        
        <div v-if="onboardingStore.formData.targetWeight" class="summary-item">
          <div class="summary-label">Zielgewicht</div>
          <div class="summary-value">{{ onboardingStore.formData.targetWeight }} kg</div>
        </div>
      </div>
      
      <div v-if="calculatedMetrics" class="metrics-preview">
        <div class="metric">
          <div class="metric-label">BMI</div>
          <div class="metric-value">{{ calculatedMetrics.bmi }}</div>
        </div>
        <div class="metric">
          <div class="metric-label">Grundumsatz</div>
          <div class="metric-value">{{ calculatedMetrics.bmr }} kcal</div>
        </div>
        <div class="metric">
          <div class="metric-label">Gesamtumsatz</div>
          <div class="metric-value">{{ calculatedMetrics.tdee }} kcal</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useOnboardingStore } from '@/stores/onboarding'

const onboardingStore = useOnboardingStore()

const updateTargetWeight = (event) => {
  const value = event.target.value
  onboardingStore.updateFormData('targetWeight', value ? parseFloat(value) : '')
}

const skipTargetWeight = () => {
  onboardingStore.updateFormData('targetWeight', '')
}

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

const calculatedMetrics = computed(() => {
  const { weight, height, gender, birthDate } = onboardingStore.formData
  
  if (!weight || !height || !gender || !birthDate) return null
  
  const age = calculatedAge.value
  if (!age) return null
  
  // BMI
  const heightInMeters = height / 100
  const bmi = Math.round((weight / (heightInMeters * heightInMeters)) * 10) / 10
  
  // BMR (Mifflin-St Jeor Equation)
  let bmr
  if (gender === 'male') {
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
  } else {
    bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
  }
  
  // TDEE
  const activityFactor = onboardingStore.activityLevelOptions.find(
    option => option.value === onboardingStore.formData.activityLevel
  )?.factor || 1.2
  
  const tdee = bmr * activityFactor
  
  return {
    bmi,
    bmr: Math.round(bmr),
    tdee: Math.round(tdee)
  }
})

const getGenderLabel = () => {
  const option = onboardingStore.genderOptions.find(
    opt => opt.value === onboardingStore.formData.gender
  )
  return option?.label || ''
}

const getGoalLabel = () => {
  const option = onboardingStore.goalOptions.find(
    opt => opt.value === onboardingStore.formData.goal
  )
  return option?.label || ''
}

const getActivityLabel = () => {
  const option = onboardingStore.activityLevelOptions.find(
    opt => opt.value === onboardingStore.formData.activityLevel
  )
  return option?.label.split('(')[0].trim() || ''
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

.form-group {
  text-align: left;
  margin-bottom: var(--space-2xl);
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

.skip-option {
  text-align: center;
  margin-bottom: var(--space-lg);
}

.skip-button {
  min-width: 150px;
}

.profile-summary {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  padding: var(--space-xl);
  border: 1px solid var(--border);
  text-align: left;
  
  h3 {
    margin-bottom: var(--space-lg);
    color: var(--text-primary);
    font-size: 1.25rem;
    font-weight: 600;
    text-align: center;
  }
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-md);
  margin-bottom: var(--space-xl);
}

.summary-item {
  padding: var(--space-md);
  background: var(--bg-primary);
  border-radius: var(--radius);
  border: 1px solid var(--border);
}

.summary-label {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: var(--space-xs);
}

.summary-value {
  font-size: 1rem;
  font-weight: 500;
  color: var(--text-primary);
}

.metrics-preview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: var(--space-md);
  padding-top: var(--space-lg);
  border-top: 1px solid var(--border);
}

.metric {
  text-align: center;
  padding: var(--space-md);
  background: var(--bg-primary);
  border-radius: var(--radius);
  border: 1px solid var(--border);
}

.metric-label {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: var(--space-xs);
}

.metric-value {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--primary);
}

.field-error {
  color: var(--error);
  font-size: 0.875rem;
  margin-top: var(--space-sm);
}

// Mobile Responsiveness
@media (max-width: 768px) {
  .summary-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .metrics-preview {
    grid-template-columns: 1fr;
  }
}

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
  
  .profile-summary {
    padding: var(--space-lg);
  }
  
  .summary-grid {
    grid-template-columns: 1fr;
  }
}
</style> 
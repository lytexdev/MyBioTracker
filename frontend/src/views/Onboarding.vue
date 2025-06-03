<template>
  <div class="onboarding">
    <div class="onboarding-container">
      <!-- Header with Progress -->
      <div class="onboarding-header">
        <div class="progress-section">
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :style="{ width: `${onboardingStore.progress}%` }"
            ></div>
          </div>
          <div class="progress-text">
            Schritt {{ onboardingStore.currentStep }} von {{ onboardingStore.totalSteps }}
          </div>
        </div>
        
        <button 
          v-if="!onboardingStore.isFirstStep" 
          @click="onboardingStore.previousStep"
          class="back-button"
        >
          <Icon name="arrow-left" size="20" />
        </button>
      </div>

      <!-- Step Content -->
      <div class="onboarding-content">
        <Transition name="slide" mode="out-in">
          <component 
            :is="currentStepComponent" 
            :key="onboardingStore.currentStep"
          />
        </Transition>
      </div>

      <!-- Navigation -->
      <div class="onboarding-navigation">
        <button 
          v-if="!onboardingStore.isFirstStep"
          @click="onboardingStore.previousStep"
          class="btn btn-outline nav-button"
        >
          Zurück
        </button>
        
        <button 
          v-if="!onboardingStore.isLastStep"
          @click="handleNext"
          :disabled="!onboardingStore.canProceed"
          class="btn btn-primary nav-button"
        >
          Weiter
        </button>
        
        <button 
          v-if="onboardingStore.isLastStep"
          @click="handleComplete"
          :disabled="onboardingStore.isLoading"
          class="btn btn-primary nav-button"
        >
          <span v-if="onboardingStore.isLoading">Wird gespeichert...</span>
          <span v-else>Profil erstellen</span>
        </button>
      </div>

      <!-- Error Message -->
      <div v-if="onboardingStore.errors.general" class="error-message">
        {{ onboardingStore.errors.general }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useOnboardingStore } from '@/stores/onboarding'
import { useToastStore } from '@/stores/toast'
import Icon from '@/components/ui/Icon.vue'

// Step Components
import OnboardingStep1 from '@/components/onboarding/OnboardingStep1.vue'
import OnboardingStep2 from '@/components/onboarding/OnboardingStep2.vue'
import OnboardingStep3 from '@/components/onboarding/OnboardingStep3.vue'
import OnboardingStep4 from '@/components/onboarding/OnboardingStep4.vue'
import OnboardingStep5 from '@/components/onboarding/OnboardingStep5.vue'
import OnboardingStep6 from '@/components/onboarding/OnboardingStep6.vue'
import OnboardingStep7 from '@/components/onboarding/OnboardingStep7.vue'
import OnboardingStep8 from '@/components/onboarding/OnboardingStep8.vue'

const router = useRouter()
const onboardingStore = useOnboardingStore()
const toastStore = useToastStore()

const stepComponents = {
  1: OnboardingStep1,
  2: OnboardingStep2,
  3: OnboardingStep3,
  4: OnboardingStep4,
  5: OnboardingStep5,
  6: OnboardingStep6,
  7: OnboardingStep7,
  8: OnboardingStep8
}

const currentStepComponent = computed(() => {
  return stepComponents[onboardingStore.currentStep]
})

const handleNext = () => {
  if (onboardingStore.validateCurrentStep()) {
    onboardingStore.nextStep()
  }
}

const handleComplete = async () => {
  const success = await onboardingStore.completeOnboarding()
  
  if (success) {
    toastStore.success('Profil erfolgreich erstellt!')
    router.push('/dashboard')
  }
}
</script>

<style lang="scss" scoped>
.onboarding {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-lg);
}

.onboarding-container {
  width: 100%;
  max-width: 600px;
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
}

.onboarding-header {
  padding: var(--space-xl);
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.progress-section {
  flex: 1;
  text-align: center;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--border);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: var(--space-md);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary), var(--primary-dark));
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.back-button {
  position: absolute;
  left: var(--space-lg);
  width: 40px;
  height: 40px;
  border: none;
  background: var(--bg-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-tertiary);
    color: var(--primary);
  }
}

.onboarding-content {
  padding: var(--space-2xl);
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.onboarding-navigation {
  padding: var(--space-xl);
  border-top: 1px solid var(--border);
  display: flex;
  gap: var(--space-md);
  justify-content: space-between;
  
  @media (max-width: 480px) {
    flex-direction: column;
  }
}

.nav-button {
  flex: 1;
  max-width: 200px;
  
  @media (max-width: 480px) {
    max-width: none;
  }
}

.error-message {
  padding: var(--space-md) var(--space-xl);
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
  text-align: center;
  font-size: 0.875rem;
  border-top: 1px solid rgba(239, 68, 68, 0.2);
}

// Slide Transition
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

// Mobile Responsiveness
@media (max-width: 768px) {
  .onboarding {
    padding: var(--space-md);
  }
  
  .onboarding-container {
    max-width: none;
  }
  
  .onboarding-header {
    padding: var(--space-lg);
  }
  
  .onboarding-content {
    padding: var(--space-xl);
    min-height: 350px;
  }
  
  .onboarding-navigation {
    padding: var(--space-lg);
  }
}

@media (max-width: 480px) {
  .onboarding-content {
    padding: var(--space-lg);
  }
  
  .back-button {
    left: var(--space-md);
  }
}
</style> 
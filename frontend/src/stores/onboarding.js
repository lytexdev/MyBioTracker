import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useProfileStore } from './profile'
import { useAuthStore } from './auth'
import api from '@/services/api'

export const useOnboardingStore = defineStore('onboarding', () => {
  const authStore = useAuthStore()
  
  // State
  const currentStep = ref(1)
  const totalSteps = ref(8)
  const isLoading = ref(false)
  const errors = ref({})
  
  // Form data
  const formData = ref({
    gender: '',
    birthDate: '',
    height: '',
    weight: '',
    bodyFat: '',
    goal: '',
    activityLevel: '',
    targetWeight: ''
  })
  
  // Options for select fields
  const genderOptions = [
    { value: 'male', label: 'Männlich' },
    { value: 'female', label: 'Weiblich' },
    { value: 'diverse', label: 'Divers' }
  ]
  
  const goalOptions = [
    { value: 'lose_weight', label: 'Abnehmen' },
    { value: 'gain_weight', label: 'Zunehmen' },
    { value: 'maintain_weight', label: 'Gewicht halten' },
    { value: 'build_muscle', label: 'Muskeln aufbauen' },
    { value: 'stay_fit', label: 'Fit bleiben' }
  ]
  
  const activityLevelOptions = [
    { value: 'sedentary', label: 'Sehr niedrig (Bürojob, wenig Bewegung)', factor: 1.2 },
    { value: 'lightly_active', label: 'Niedrig (leichte Aktivität 1-3x/Woche)', factor: 1.375 },
    { value: 'moderately_active', label: 'Moderat (moderate Aktivität 3-5x/Woche)', factor: 1.55 },
    { value: 'very_active', label: 'Hoch (intensive Aktivität 6-7x/Woche)', factor: 1.725 },
    { value: 'extremely_active', label: 'Sehr hoch (sehr intensive Aktivität, körperliche Arbeit)', factor: 1.9 }
  ]
  
  // Computed
  const progress = computed(() => (currentStep.value / totalSteps.value) * 100)
  
  const isFirstStep = computed(() => currentStep.value === 1)
  const isLastStep = computed(() => currentStep.value === totalSteps.value)
  
  const canProceed = computed(() => {
    switch (currentStep.value) {
      case 1: return formData.value.gender
      case 2: return formData.value.birthDate && isValidBirthDate(formData.value.birthDate)
      case 3: return formData.value.height && formData.value.height >= 100 && formData.value.height <= 250
      case 4: return formData.value.weight && formData.value.weight >= 30 && formData.value.weight <= 300
      case 5: return true // Body fat is optional
      case 6: return formData.value.goal
      case 7: return formData.value.activityLevel
      case 8: return true // Target weight is optional
      default: return false
    }
  })
  
  // Validation helpers
  const isValidBirthDate = (date) => {
    if (!date) return false
    const birthDate = new Date(date)
    const today = new Date()
    const age = today.getFullYear() - birthDate.getFullYear()
    return age >= 13 && age <= 120
  }
  
  // Actions
  const nextStep = () => {
    if (canProceed.value && !isLastStep.value) {
      currentStep.value++
      clearErrors()
    }
  }
  
  const previousStep = () => {
    if (!isFirstStep.value) {
      currentStep.value--
      clearErrors()
    }
  }
  
  const goToStep = (step) => {
    if (step >= 1 && step <= totalSteps.value) {
      currentStep.value = step
      clearErrors()
    }
  }
  
  const updateFormData = (field, value) => {
    formData.value[field] = value
    clearFieldError(field)
  }
  
  const setError = (field, message) => {
    errors.value[field] = message
  }
  
  const clearFieldError = (field) => {
    if (errors.value[field]) {
      delete errors.value[field]
    }
  }
  
  const clearErrors = () => {
    errors.value = {}
  }
  
  const validateCurrentStep = () => {
    clearErrors()
    
    switch (currentStep.value) {
      case 1:
        if (!formData.value.gender) {
          setError('gender', 'Bitte wählen Sie Ihr Geschlecht aus')
          return false
        }
        break
        
      case 2:
        if (!formData.value.birthDate) {
          setError('birthDate', 'Bitte geben Sie Ihr Geburtsdatum ein')
          return false
        }
        if (!isValidBirthDate(formData.value.birthDate)) {
          setError('birthDate', 'Bitte geben Sie ein gültiges Geburtsdatum ein (13-120 Jahre)')
          return false
        }
        break
        
      case 3:
        if (!formData.value.height) {
          setError('height', 'Bitte geben Sie Ihre Größe ein')
          return false
        }
        if (formData.value.height < 100 || formData.value.height > 250) {
          setError('height', 'Bitte geben Sie eine gültige Größe ein (100-250 cm)')
          return false
        }
        break
        
      case 4:
        if (!formData.value.weight) {
          setError('weight', 'Bitte geben Sie Ihr Gewicht ein')
          return false
        }
        if (formData.value.weight < 30 || formData.value.weight > 300) {
          setError('weight', 'Bitte geben Sie ein gültiges Gewicht ein (30-300 kg)')
          return false
        }
        break
        
      case 5:
        if (formData.value.bodyFat && (formData.value.bodyFat < 3 || formData.value.bodyFat > 50)) {
          setError('bodyFat', 'Bitte geben Sie einen gültigen Körperfettanteil ein (3-50%)')
          return false
        }
        break
        
      case 6:
        if (!formData.value.goal) {
          setError('goal', 'Bitte wählen Sie Ihr Ziel aus')
          return false
        }
        break
        
      case 7:
        if (!formData.value.activityLevel) {
          setError('activityLevel', 'Bitte wählen Sie Ihr Aktivitätslevel aus')
          return false
        }
        break
        
      case 8:
        if (formData.value.targetWeight && (formData.value.targetWeight < 30 || formData.value.targetWeight > 300)) {
          setError('targetWeight', 'Bitte geben Sie ein gültiges Zielgewicht ein (30-300 kg)')
          return false
        }
        break
    }
    
    return true
  }
  
  const completeOnboarding = async () => {
    if (!validateCurrentStep()) return false
    
    isLoading.value = true
    
    try {
      // Calculate BMR and other metrics
      const age = calculateAge(formData.value.birthDate)
      const bmr = calculateBMR(formData.value.gender, formData.value.weight, formData.value.height, age)
      const activityFactor = activityLevelOptions.find(option => option.value === formData.value.activityLevel)?.factor || 1.2
      const tdee = bmr * activityFactor
      
      const profileData = {
        gender: formData.value.gender,
        birth_date: formData.value.birthDate,
        height: parseInt(formData.value.height),
        weight: parseFloat(formData.value.weight),
        body_fat: formData.value.bodyFat ? parseFloat(formData.value.bodyFat) : null,
        goal: formData.value.goal,
        activity_level: formData.value.activityLevel,
        target_weight: formData.value.targetWeight ? parseFloat(formData.value.targetWeight) : null,
        age,
        bmr: Math.round(bmr),
        tdee: Math.round(tdee),
        bmi: calculateBMI(formData.value.weight, formData.value.height)
      }
      
      console.log('🚀 Sending profile data:', profileData)
      
      // Submit profile data
      await api.post('/profile', profileData)
      
      // Update auth user (no longer setting onboarding_completed)
      await authStore.loadUser()
      
      return true
    } catch (error) {
      console.error('❌ Error completing onboarding:', error)
      console.error('Response data:', error.response?.data)
      setError('general', 'Fehler beim Speichern des Profils. Bitte versuchen Sie es erneut.')
      return false
    } finally {
      isLoading.value = false
    }
  }
  
  // Helper functions
  const calculateAge = (birthDate) => {
    const today = new Date()
    const birth = new Date(birthDate)
    let age = today.getFullYear() - birth.getFullYear()
    const monthDiff = today.getMonth() - birth.getMonth()
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--
    }
    
    return age
  }
  
  const calculateBMR = (gender, weight, height, age) => {
    // Mifflin-St Jeor Equation
    if (gender === 'male') {
      return (10 * weight) + (6.25 * height) - (5 * age) + 5
    } else {
      return (10 * weight) + (6.25 * height) - (5 * age) - 161
    }
  }
  
  const calculateBMI = (weight, height) => {
    const heightInMeters = height / 100
    return Math.round((weight / (heightInMeters * heightInMeters)) * 10) / 10
  }
  
  const reset = () => {
    currentStep.value = 1
    formData.value = {
      gender: '',
      birthDate: '',
      height: '',
      weight: '',
      bodyFat: '',
      goal: '',
      activityLevel: '',
      targetWeight: ''
    }
    errors.value = {}
    isLoading.value = false
  }
  
  return {
    // State
    currentStep,
    totalSteps,
    isLoading,
    errors,
    formData,
    
    // Options
    genderOptions,
    goalOptions,
    activityLevelOptions,
    
    // Computed
    progress,
    isFirstStep,
    isLastStep,
    canProceed,
    
    // Actions
    nextStep,
    previousStep,
    goToStep,
    updateFormData,
    validateCurrentStep,
    completeOnboarding,
    reset
  }
}) 
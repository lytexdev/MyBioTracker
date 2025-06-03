<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-header">
        <h1>MyBioTracker</h1>
        <p>Start tracking your nutrition and caffeine</p>
      </div>

      <div class="register-card">
        <form @submit.prevent="handleRegister" class="register-form">
          <h2>Create Account</h2>
          
          <div class="form-group">
            <label for="email" class="form-label">Email *</label>
            <input
              id="email"
              v-model="registerForm.email"
              type="email"
              class="form-input"
              placeholder="your@email.com"
              required
              autocomplete="email"
            >
          </div>

          <div class="form-group">
            <label for="password" class="form-label">Password *</label>
            <div class="password-input">
              <input
                id="password"
                v-model="registerForm.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                placeholder="Choose a secure password"
                required
                autocomplete="new-password"
              >
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="password-toggle"
              >
                <Icon :name="showPassword ? 'eye-off' : 'eye'" size="18" />
              </button>
            </div>
            <div class="password-requirements">
              <small>Password must be at least 8 characters long</small>
            </div>
          </div>

          <div class="form-group">
            <label for="confirmPassword" class="form-label">Confirm Password *</label>
            <input
              id="confirmPassword"
              v-model="registerForm.confirmPassword"
              type="password"
              class="form-input"
              placeholder="Confirm your password"
              required
              autocomplete="new-password"
            >
            <div v-if="passwordMismatch" class="field-error">
              Passwords do not match
            </div>
          </div>

          <div class="form-group">
            <label class="checkbox-label">
              <input
                v-model="registerForm.agreeToTerms"
                type="checkbox"
                class="checkbox-input"
                required
              >
              <span class="checkbox-custom"></span>
              I agree to the 
              <router-link to="/terms" target="_blank">Terms of Service</router-link>
              and 
              <router-link to="/privacy" target="_blank">Privacy Policy</router-link>
            </label>
          </div>

          <div class="form-group">
            <label class="checkbox-label">
              <input
                v-model="registerForm.newsletter"
                type="checkbox"
                class="checkbox-input"
              >
              <span class="checkbox-custom"></span>
              Send me updates about new features and tips
            </label>
          </div>

          <button
            type="submit"
            class="btn btn-primary btn-full"
            :disabled="loading || !isFormValid"
          >
            <Icon v-if="loading" name="loader" class="animate-spin" />
            {{ loading ? 'Creating account...' : 'Create Account' }}
          </button>

          <div class="divider">
            <span>or</span>
          </div>

          <div class="social-login">
            <button type="button" class="btn btn-outline btn-full social-btn" disabled>
              <Icon name="chrome" size="18" />
              Sign up with Google
            </button>
          </div>

          <div class="login-link">
            Already have an account?
            <router-link to="/auth/login">Sign in</router-link>
          </div>
        </form>
      </div>

      <!-- Benefits -->
      <div class="benefits-card">
        <h3>Why MyBioTracker?</h3>
        <div class="benefits-list">
          <div class="benefit-item">
            <Icon name="utensils" size="20" />
            <span>Track nutrition and macros</span>
          </div>
          <div class="benefit-item">
            <Icon name="coffee" size="20" />
            <span>Monitor caffeine intake</span>
          </div>
          <div class="benefit-item">
            <Icon name="target" size="20" />
            <span>Set and achieve goals</span>
          </div>
          <div class="benefit-item">
            <Icon name="trending-up" size="20" />
            <span>View detailed analytics</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'
import Icon from '@/components/ui/Icon.vue'

const router = useRouter()
const authStore = useAuthStore()
const toastStore = useToastStore()

const loading = ref(false)
const showPassword = ref(false)

const registerForm = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  agreeToTerms: false,
  newsletter: false
})

const passwordMismatch = computed(() => {
  return registerForm.password && registerForm.confirmPassword && 
         registerForm.password !== registerForm.confirmPassword
})

const isFormValid = computed(() => {
  return registerForm.email &&
         registerForm.password &&
         registerForm.password.length >= 8 &&
         registerForm.password === registerForm.confirmPassword &&
         registerForm.agreeToTerms
})

const handleRegister = async () => {
  if (!isFormValid.value) {
    toastStore.error('Please fill in all required fields correctly')
    return
  }

  try {
    loading.value = true
    
    const success = await authStore.register({
      email: registerForm.email,
      password: registerForm.password,
      newsletter: registerForm.newsletter
    })
    
    if (success) {
      toastStore.success('Account created successfully! Let\'s set up your profile.')
      router.push('/onboarding')
    } else {
      toastStore.error(authStore.error || 'Registration failed')
    }
    
  } catch (error) {
    console.error('Registration failed:', error)
    toastStore.error('Registration failed. Please try again.')
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #cbd5e1 100%);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-lg);
  
  // Subtle pattern overlay
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
      radial-gradient(circle at 20% 50%, rgba(34, 197, 94, 0.1) 0%, transparent 50%),
      radial-gradient(circle at 80% 20%, rgba(34, 197, 94, 0.05) 0%, transparent 50%),
      radial-gradient(circle at 40% 80%, rgba(34, 197, 94, 0.08) 0%, transparent 50%);
    pointer-events: none;
  }
  
  // Fade in animation für die gesamte Seite
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.register-container {
  width: 100%;
  max-width: 450px;
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
  
  // Staggered animation für Container-Elemente
  > * {
    animation: slideInUp 0.6s ease-out backwards;
  }
  
  > *:nth-child(1) { animation-delay: 0.1s; }
  > *:nth-child(2) { animation-delay: 0.2s; }
  > *:nth-child(3) { animation-delay: 0.3s; }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.register-header {
  text-align: center;
  color: var(--text-primary);
  position: relative;
  z-index: 1;
  
  h1 {
    margin: 0 0 var(--space-sm) 0;
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: bounceIn 0.8s ease-out 0.2s backwards;
  }
  
  p {
    margin: 0;
    color: var(--text-secondary);
    font-size: 1.125rem;
    animation: fadeInUp 0.6s ease-out 0.4s backwards;
  }
}

@keyframes bounceIn {
  0% {
    transform: scale(0.3);
    opacity: 0;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.8;
  }
  70% {
    transform: scale(0.9);
    opacity: 0.9;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.register-card,
.benefits-card {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  padding: var(--space-2xl);
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--border);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  }
}

.register-form {
  h2 {
    margin: 0 0 var(--space-xl) 0;
    text-align: center;
    color: var(--text-primary);
    font-size: 1.5rem;
    animation: fadeIn 0.6s ease-out 0.5s backwards;
  }
}

.form-group {
  margin-bottom: var(--space-lg);
  
  // Form field animations
  .form-input {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    
    &:focus {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(34, 197, 94, 0.15);
      border-color: var(--primary);
    }
  }
  
  .form-label {
    transition: color 0.3s ease;
  }
  
  &:focus-within .form-label {
    color: var(--primary);
  }
}

.password-input {
  position: relative;
  
  .form-input {
    padding-right: 40px;
  }
  
  .password-toggle {
    position: absolute;
    right: var(--space-md);
    top: 50%;
    transform: translateY(-50%);
    border: none;
    background: none;
    color: var(--text-secondary);
    cursor: pointer;
    padding: var(--space-xs);
    border-radius: var(--radius);
    transition: all 0.3s ease;
    
    &:hover {
      color: var(--text-primary);
      background: var(--bg-secondary);
      transform: translateY(-50%) scale(1.1);
    }
    
    &:active {
      transform: translateY(-50%) scale(0.95);
    }
  }
}

.password-requirements {
  margin-top: var(--space-xs);
  
  small {
    color: var(--text-muted);
    font-size: 0.75rem;
    animation: fadeIn 0.3s ease-out;
  }
}

.field-error {
  margin-top: var(--space-xs);
  color: var(--error);
  font-size: 0.875rem;
  animation: shake 0.5s ease-out, fadeIn 0.3s ease-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: var(--space-sm);
  cursor: pointer;
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.6;
  padding: var(--space-sm);
  border-radius: var(--radius);
  transition: all 0.3s ease;
  border: 1px solid transparent;
  
  &:hover {
    color: var(--text-primary);
    background: var(--bg-secondary);
    border-color: var(--border);
    transform: translateX(4px);
  }
  
  .checkbox-input {
    display: none;
  }
  
  .checkbox-custom {
    width: 18px;
    height: 18px;
    border: 2px solid var(--border);
    border-radius: var(--radius-sm);
    position: relative;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    flex-shrink: 0;
    margin-top: 2px;
    background: var(--bg-primary);
    
    &::after {
      content: '';
      position: absolute;
      top: 2px;
      left: 5px;
      width: 5px;
      height: 9px;
      border: solid white;
      border-width: 0 2px 2px 0;
      transform: rotate(45deg) scale(0);
      transition: transform 0.2s ease-out 0.1s;
    }
  }
  
  .checkbox-input:checked + .checkbox-custom {
    background: var(--primary);
    border-color: var(--primary);
    transform: scale(1.1);
    
    &::after {
      transform: rotate(45deg) scale(1);
    }
  }
  
  // Spezielle Behandlung für Terms und Newsletter
  &:nth-child(1) {
    background: rgba(34, 197, 94, 0.05);
    border: 1px solid rgba(34, 197, 94, 0.2);
    
    &:hover {
      background: rgba(34, 197, 94, 0.1);
      border-color: var(--primary);
    }
  }
  
  a {
    color: var(--primary);
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
    position: relative;
    
    &::after {
      content: '';
      position: absolute;
      width: 0;
      height: 1px;
      bottom: 0;
      left: 0;
      background: var(--primary);
      transition: width 0.3s ease;
    }
    
    &:hover {
      color: var(--primary-dark);
      
      &::after {
        width: 100%;
      }
    }
  }
}

.btn-full {
  width: 100%;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(34, 197, 94, 0.25);
  }
  
  &:active:not(:disabled) {
    transform: translateY(0);
  }
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none !important;
    box-shadow: none !important;
  }
}

.divider {
  position: relative;
  text-align: center;
  margin: var(--space-xl) 0;
  
  &::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 1px;
    background: var(--border);
    animation: expandWidth 0.6s ease-out 0.8s backwards;
  }
  
  span {
    background: var(--bg-primary);
    padding: 0 var(--space-lg);
    color: var(--text-muted);
    font-size: 0.875rem;
    animation: fadeIn 0.4s ease-out 1s backwards;
  }
}

@keyframes expandWidth {
  from {
    transform: scaleX(0);
  }
  to {
    transform: scaleX(1);
  }
}

.social-login {
  margin-bottom: var(--space-xl);
}

.social-btn {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  opacity: 0.6;
  cursor: not-allowed;
  transition: all 0.3s ease;
  
  &:hover {
    opacity: 0.8;
    transform: translateY(-1px);
  }
}

.login-link {
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.875rem;
  animation: fadeIn 0.6s ease-out 1.2s backwards;
  
  a {
    color: var(--primary);
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
    position: relative;
    
    &::after {
      content: '';
      position: absolute;
      width: 0;
      height: 2px;
      bottom: -2px;
      left: 0;
      background: var(--primary);
      transition: width 0.3s ease;
    }
    
    &:hover::after {
      width: 100%;
    }
  }
}

.benefits-card {
  h3 {
    margin: 0 0 var(--space-lg) 0;
    color: var(--text-primary);
    text-align: center;
    animation: fadeIn 0.6s ease-out 1s backwards;
  }
}

.benefits-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  color: var(--text-secondary);
  font-size: 0.875rem;
  padding: var(--space-sm);
  border-radius: var(--radius);
  transition: all 0.3s ease;
  animation: fadeInLeft 0.6s ease-out backwards;
  
  &:nth-child(1) { animation-delay: 1.1s; }
  &:nth-child(2) { animation-delay: 1.2s; }
  &:nth-child(3) { animation-delay: 1.3s; }
  &:nth-child(4) { animation-delay: 1.4s; }
  
  &:hover {
    background: var(--bg-secondary);
    transform: translateX(8px);
    color: var(--text-primary);
  }
  
  svg {
    color: var(--primary);
    flex-shrink: 0;
    transition: transform 0.3s ease;
  }
  
  &:hover svg {
    transform: scale(1.2);
  }
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

// Form focus ring animation
.form-input {
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: var(--radius);
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
    box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
  }
  
  &:focus::after {
    opacity: 1;
  }
}

// Success animation für valide Formulareingaben
.form-group.valid .form-input {
  border-color: var(--success);
  
  &::before {
    content: '✓';
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--success);
    font-weight: bold;
    animation: checkmark 0.3s ease-out;
  }
}

@keyframes checkmark {
  0% {
    transform: translateY(-50%) scale(0);
    opacity: 0;
  }
  50% {
    transform: translateY(-50%) scale(1.2);
    opacity: 1;
  }
  100% {
    transform: translateY(-50%) scale(1);
    opacity: 1;
  }
}

// Progressive enhancement für bessere Interaktion
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

// Hover effects für interaktive Elemente
button, .checkbox-label, .login-link a {
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    transition: all 0.5s ease;
    transform: translate(-50%, -50%);
    pointer-events: none;
    z-index: 0;
  }
  
  &:active::before {
    width: 200px;
    height: 200px;
  }
  
  // Ensure content stays above the ripple effect
  * {
    position: relative;
    z-index: 1;
  }
}
</style>

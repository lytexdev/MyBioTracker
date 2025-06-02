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
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import Icon from '@/components/ui/Icon.vue'

const router = useRouter()
const userStore = useUserStore()
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
    
    await userStore.register({
      email: registerForm.email,
      password: registerForm.password,
      newsletter: registerForm.newsletter
    })
    
    toastStore.success('Account created successfully! Please check your email for verification.')
    router.push('/auth/login')
    
  } catch (error) {
    console.error('Registration failed:', error)
    
    if (error.response?.status === 409) {
      toastStore.error('An account with this email already exists')
    } else if (error.response?.data?.detail) {
      toastStore.error(error.response.data.detail)
    } else {
      toastStore.error('Registration failed. Please try again.')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary-light), var(--primary));
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-lg);
}

.register-container {
  width: 100%;
  max-width: 450px;
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
}

.register-header {
  text-align: center;
  color: white;
  
  h1 {
    margin: 0 0 var(--space-sm) 0;
    font-size: 2.5rem;
    font-weight: 700;
  }
  
  p {
    margin: 0;
    opacity: 0.9;
    font-size: 1.125rem;
  }
}

.register-card,
.benefits-card {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  padding: var(--space-2xl);
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--border);
}

.register-form {
  h2 {
    margin: 0 0 var(--space-xl) 0;
    text-align: center;
    color: var(--text-primary);
    font-size: 1.5rem;
  }
}

.form-group {
  margin-bottom: var(--space-lg);
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
    transition: var(--transition);
    
    &:hover {
      color: var(--text-primary);
      background: var(--bg-secondary);
    }
  }
}

.password-requirements {
  margin-top: var(--space-xs);
  
  small {
    color: var(--text-muted);
    font-size: 0.75rem;
  }
}

.field-error {
  margin-top: var(--space-xs);
  color: var(--error);
  font-size: 0.875rem;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: var(--space-sm);
  cursor: pointer;
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.5;
  
  .checkbox-input {
    display: none;
  }
  
  .checkbox-custom {
    width: 16px;
    height: 16px;
    border: 2px solid var(--border);
    border-radius: var(--radius-sm);
    position: relative;
    transition: var(--transition);
    flex-shrink: 0;
    margin-top: 2px;
    
    &::after {
      content: '';
      position: absolute;
      top: 1px;
      left: 4px;
      width: 4px;
      height: 8px;
      border: solid white;
      border-width: 0 2px 2px 0;
      transform: rotate(45deg);
      opacity: 0;
      transition: var(--transition);
    }
  }
  
  .checkbox-input:checked + .checkbox-custom {
    background: var(--primary);
    border-color: var(--primary);
    
    &::after {
      opacity: 1;
    }
  }
  
  a {
    color: var(--primary);
    text-decoration: none;
    
    &:hover {
      text-decoration: underline;
    }
  }
}

.btn-full {
  width: 100%;
  justify-content: center;
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
  }
  
  span {
    background: var(--bg-primary);
    padding: 0 var(--space-lg);
    color: var(--text-muted);
    font-size: 0.875rem;
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
}

.login-link {
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.875rem;
  
  a {
    color: var(--primary);
    text-decoration: none;
    font-weight: 500;
    
    &:hover {
      text-decoration: underline;
    }
  }
}

.benefits-card {
  h3 {
    margin: 0 0 var(--space-lg) 0;
    color: var(--text-primary);
    text-align: center;
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
  
  svg {
    color: var(--primary);
    flex-shrink: 0;
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>

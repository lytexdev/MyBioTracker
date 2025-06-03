<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <h1>MyBioTracker</h1>
        <p>Track your nutrition and caffeine intake</p>
      </div>

      <div class="login-card">
        <form @submit.prevent="handleLogin" class="login-form">
          <h2>Sign In</h2>
          
          <div class="form-group">
            <label for="email" class="form-label">Email</label>
            <input
              id="email"
              v-model="loginForm.email"
              type="email"
              class="form-input"
              placeholder="your@email.com"
              required
              autocomplete="email"
            >
          </div>

          <div class="form-group">
            <label for="password" class="form-label">Password</label>
            <div class="password-input">
              <input
                id="password"
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                placeholder="Enter your password"
                required
                autocomplete="current-password"
              >
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="password-toggle"
              >
                <Icon :name="showPassword ? 'eye-off' : 'eye'" size="18" />
              </button>
            </div>
          </div>

          <div class="form-options">
            <label class="checkbox-label">
              <input
                v-model="loginForm.remember"
                type="checkbox"
                class="checkbox-input"
              >
              <span class="checkbox-custom"></span>
              Remember me
            </label>
            
            <router-link to="/auth/forgot-password" class="forgot-link">
              Forgot password?
            </router-link>
          </div>

          <button
            type="submit"
            class="btn btn-primary btn-full"
            :disabled="loading"
          >
            <Icon v-if="loading" name="loader" class="animate-spin" />
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>

          <div class="divider">
            <span>or</span>
          </div>

          <div class="social-login">
            <button type="button" class="btn btn-outline btn-full social-btn" disabled>
              <Icon name="chrome" size="18" />
              Continue with Google
            </button>
          </div>

          <div class="signup-link">
            Don't have an account?
            <router-link to="/auth/register">Sign up</router-link>
          </div>
        </form>
      </div>

      <!-- Demo Account -->
      <div class="demo-card">
        <h3>Demo Account</h3>
        <p>Try the app with a demo account</p>
        <button @click="loginWithDemo" class="btn btn-outline" :disabled="loading">
          <Icon name="play" size="18" />
          Use Demo Account
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'
import Icon from '@/components/ui/Icon.vue'

const router = useRouter()
const authStore = useAuthStore()
const toastStore = useToastStore()

const loading = ref(false)
const showPassword = ref(false)

const loginForm = reactive({
  email: '',
  password: '',
  remember: false
})

const handleLogin = async () => {
  try {
    loading.value = true
    
    const success = await authStore.login({
      email: loginForm.email,
      password: loginForm.password,
      remember: loginForm.remember
    })
    
    if (success) {
      toastStore.success($t('auth.loginSuccessful'))
      router.push('/dashboard')
    } else {
      toastStore.error(authStore.error || $t('auth.invalidCredentials'))
    }
    
  } catch (error) {
    console.error('Login failed:', error)
    toastStore.error('Login failed. Please try again.')
  } finally {
    loading.value = false
  }
}

const loginWithDemo = async () => {
  try {
    loading.value = true
    
    // Use demo credentials
    const success = await authStore.login({
      email: 'demo@mybiotracker.com',
      password: 'demo123',
      remember: false
    })
    
    if (success) {
      toastStore.success('Welcome to the demo!')
      router.push('/dashboard')
    } else {
      toastStore.error('Demo login failed. Please try manual login.')
    }
    
  } catch (error) {
    console.error('Demo login failed:', error)
    toastStore.error('Demo login failed. Please try manual login.')
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.login-page {
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

.login-container {
  width: 100%;
  max-width: 400px;
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

.login-header {
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

.login-card,
.demo-card {
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

.login-form {
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

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-xl);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  cursor: pointer;
  font-size: 0.875rem;
  color: var(--text-secondary);
  transition: color 0.3s ease;
  
  &:hover {
    color: var(--text-primary);
  }
  
  .checkbox-input {
    display: none;
  }
  
  .checkbox-custom {
    width: 16px;
    height: 16px;
    border: 2px solid var(--border);
    border-radius: var(--radius-sm);
    position: relative;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    
    &::after {
      content: '';
      position: absolute;
      top: 1px;
      left: 4px;
      width: 4px;
      height: 8px;
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
}

.forgot-link {
  color: var(--primary);
  text-decoration: none;
  font-size: 0.875rem;
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

.signup-link {
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

.demo-card {
  text-align: center;
  
  h3 {
    margin: 0 0 var(--space-sm) 0;
    color: var(--text-primary);
    animation: fadeIn 0.6s ease-out 1s backwards;
  }
  
  p {
    margin: 0 0 var(--space-lg) 0;
    color: var(--text-secondary);
    font-size: 0.875rem;
    animation: fadeIn 0.6s ease-out 1.1s backwards;
  }
  
  button {
    animation: fadeIn 0.6s ease-out 1.2s backwards;
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

// Hover effects für interaktive Elemente
button, .checkbox-label, .forgot-link, .signup-link a {
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
  }
  
  &:active::before {
    width: 200px;
    height: 200px;
  }
}
</style>

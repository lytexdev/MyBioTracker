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
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import Icon from '@/components/ui/Icon.vue'

const router = useRouter()
const userStore = useUserStore()
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
    
    await userStore.login({
      email: loginForm.email,
      password: loginForm.password,
      remember: loginForm.remember
    })
    
    toastStore.success('Welcome back!')
    router.push('/dashboard')
    
  } catch (error) {
    console.error('Login failed:', error)
    
    if (error.response?.status === 401) {
      toastStore.error('Invalid email or password')
    } else if (error.response?.status === 429) {
      toastStore.error('Too many login attempts. Please try again later.')
    } else {
      toastStore.error('Login failed. Please try again.')
    }
  } finally {
    loading.value = false
  }
}

const loginWithDemo = async () => {
  try {
    loading.value = true
    
    // Use demo credentials
    await userStore.login({
      email: 'demo@mybiotracker.com',
      password: 'demo123',
      remember: false
    })
    
    toastStore.success('Welcome to the demo!')
    router.push('/dashboard')
    
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
  background: linear-gradient(135deg, var(--primary-light), var(--primary));
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-lg);
}

.login-container {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
}

.login-header {
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

.login-card,
.demo-card {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  padding: var(--space-2xl);
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--border);
}

.login-form {
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
}

.forgot-link {
  color: var(--primary);
  text-decoration: none;
  font-size: 0.875rem;
  transition: var(--transition);
  
  &:hover {
    text-decoration: underline;
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

.signup-link {
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

.demo-card {
  text-align: center;
  
  h3 {
    margin: 0 0 var(--space-sm) 0;
    color: var(--text-primary);
  }
  
  p {
    margin: 0 0 var(--space-lg) 0;
    color: var(--text-secondary);
    font-size: 0.875rem;
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Eye icons for password toggle */
.icon-eye::after,
.icon-eye-off::after {
  content: '';
  width: 18px;
  height: 18px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-eye::after {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'%3E%3Cpath d='M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z'/%3E%3Ccircle cx='12' cy='12' r='3'/%3E%3C/svg%3E");
}

.icon-eye-off::after {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'%3E%3Cpath d='M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24'/%3E%3Cline x1='1' y1='1' x2='23' y2='23'/%3E%3C/svg%3E");
}
</style>

<template>
  <div class="profile-page">
    <div class="page-header">
      <h1>Profile Settings</h1>
    </div>

    <div class="profile-content">
      <div class="profile-grid">
        <!-- Basic Information -->
        <div class="card">
          <div class="card-header">
            <h3>Basic Information</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="saveProfile">
              <div class="form-grid">
                <div class="form-group">
                  <label for="age" class="form-label">Age</label>
                  <input
                    id="age"
                    v-model.number="profile.age"
                    type="number"
                    min="13"
                    max="120"
                    class="form-input"
                    placeholder="25"
                  >
                </div>

                <div class="form-group">
                  <label for="gender" class="form-label">Gender</label>
                  <select id="gender" v-model="profile.gender" class="form-select">
                    <option value="">Select gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="height" class="form-label">Height (cm)</label>
                  <input
                    id="height"
                    v-model.number="profile.height_cm"
                    type="number"
                    min="100"
                    max="250"
                    class="form-input"
                    placeholder="175"
                  >
                </div>

                <div class="form-group">
                  <label for="weight" class="form-label">Weight (kg)</label>
                  <input
                    id="weight"
                    v-model.number="profile.weight_kg"
                    type="number"
                    min="30"
                    max="300"
                    step="0.1"
                    class="form-input"
                    placeholder="70"
                  >
                </div>

                <div class="form-group">
                  <label for="bodyFat" class="form-label">Body Fat % (Optional)</label>
                  <input
                    id="bodyFat"
                    v-model.number="profile.body_fat_percentage"
                    type="number"
                    min="3"
                    max="50"
                    step="0.1"
                    class="form-input"
                    placeholder="15"
                  >
                </div>

                <div class="form-group">
                  <label for="activityLevel" class="form-label">Activity Level</label>
                  <select id="activityLevel" v-model="profile.activity_level" class="form-select">
                    <option value="sedentary">Sedentary (little/no exercise)</option>
                    <option value="lightly_active">Lightly Active (light exercise 1-3 days/week)</option>
                    <option value="moderately_active">Moderately Active (moderate exercise 3-5 days/week)</option>
                    <option value="very_active">Very Active (hard exercise 6-7 days/week)</option>
                    <option value="extremely_active">Extremely Active (very hard exercise, physical job)</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="primaryGoal" class="form-label">Primary Goal</label>
                  <select id="primaryGoal" v-model="profile.primary_goal" class="form-select">
                    <option value="lose_weight">Lose Weight</option>
                    <option value="gain_weight">Gain Weight</option>
                    <option value="build_muscle">Build Muscle</option>
                    <option value="maintain">Maintain Current Weight</option>
                    <option value="improve_health">Improve Overall Health</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="timezone" class="form-label">Timezone</label>
                  <select id="timezone" v-model="profile.timezone" class="form-select">
                    <option value="UTC">UTC</option>
                    <option value="America/New_York">Eastern Time</option>
                    <option value="America/Chicago">Central Time</option>
                    <option value="America/Denver">Mountain Time</option>
                    <option value="America/Los_Angeles">Pacific Time</option>
                    <option value="Europe/London">London</option>
                    <option value="Europe/Berlin">Berlin</option>
                    <option value="Europe/Paris">Paris</option>
                    <option value="Asia/Tokyo">Tokyo</option>
                  </select>
                </div>
              </div>

              <div class="form-actions">
                <button type="submit" class="btn btn-primary" :disabled="saving">
                  <Icon v-if="saving" name="loader" class="animate-spin" />
                  {{ saving ? 'Saving...' : 'Save Profile' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Calculated Metrics -->
        <div class="card">
          <div class="card-header">
            <h3>Calculated Metrics</h3>
            <span class="help-text">Based on your profile information</span>
          </div>
          <div class="card-body">
            <div v-if="hasBasicInfo" class="metrics-grid">
              <div class="metric-item">
                <div class="metric-label">BMI</div>
                <div class="metric-value">{{ calculatedBMI }}</div>
                <div class="metric-status" :class="bmiStatus.class">{{ bmiStatus.label }}</div>
              </div>

              <div class="metric-item">
                <div class="metric-label">BMR</div>
                <div class="metric-value">{{ profile.bmr_calories || '--' }}</div>
                <div class="metric-unit">calories/day</div>
              </div>

              <div class="metric-item">
                <div class="metric-label">TDEE</div>
                <div class="metric-value">{{ profile.tdee_calories || '--' }}</div>
                <div class="metric-unit">calories/day</div>
              </div>

              <div class="metric-item">
                <div class="metric-label">Target Calories</div>
                <div class="metric-value">{{ profile.target_calories || '--' }}</div>
                <div class="metric-unit">per day</div>
              </div>
            </div>
            
            <div v-else class="no-metrics">
              <Icon name="calculator" size="48" />
              <p>Complete your profile to see calculated metrics</p>
              <small>We need your age, gender, height, and weight to calculate BMR, TDEE, and nutrition targets.</small>
            </div>
          </div>
        </div>

        <!-- Nutrition Targets -->
        <div class="card">
          <div class="card-header">
            <h3>Nutrition Targets</h3>
            <span class="help-text">Daily macro targets based on your goals</span>
          </div>
          <div class="card-body">
            <div v-if="hasNutritionTargets" class="targets-grid">
              <div class="target-item">
                <div class="target-circle calories">
                  <span class="target-value">{{ profile.target_calories || 0 }}</span>
                  <span class="target-unit">cal</span>
                </div>
                <div class="target-label">Calories</div>
              </div>

              <div class="target-item">
                <div class="target-circle protein">
                  <span class="target-value">{{ profile.target_protein_g || 0 }}</span>
                  <span class="target-unit">g</span>
                </div>
                <div class="target-label">Protein</div>
              </div>

              <div class="target-item">
                <div class="target-circle carbs">
                  <span class="target-value">{{ profile.target_carbs_g || 0 }}</span>
                  <span class="target-unit">g</span>
                </div>
                <div class="target-label">Carbs</div>
              </div>

              <div class="target-item">
                <div class="target-circle fat">
                  <span class="target-value">{{ profile.target_fat_g || 0 }}</span>
                  <span class="target-unit">g</span>
                </div>
                <div class="target-label">Fat</div>
              </div>
            </div>
            
            <div v-else class="no-targets">
              <Icon name="target" size="48" />
              <p>No nutrition targets calculated yet</p>
              <small>Save your profile to calculate personalized nutrition targets.</small>
            </div>
          </div>
        </div>

        <!-- Account Settings -->
        <div class="card">
          <div class="card-header">
            <h3>Account Settings</h3>
          </div>
          <div class="card-body">
            <div class="setting-item">
              <div class="setting-info">
                <h4>Email</h4>
                <p>{{ user?.email || 'Not set' }}</p>
              </div>
              <button class="btn btn-outline btn-sm">Change Email</button>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <h4>Password</h4>
                <p>Last changed: Never</p>
              </div>
              <button class="btn btn-outline btn-sm">Change Password</button>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <h4>Two-Factor Authentication</h4>
                <p>{{ user?.two_factor_enabled ? 'Enabled' : 'Disabled' }}</p>
              </div>
              <button class="btn btn-outline btn-sm">
                {{ user?.two_factor_enabled ? 'Disable' : 'Enable' }} 2FA
              </button>
            </div>

            <div class="setting-item danger">
              <div class="setting-info">
                <h4>Delete Account</h4>
                <p>Permanently delete your account and all data</p>
              </div>
              <button class="btn btn-danger btn-sm">Delete Account</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import Icon from '@/components/ui/Icon.vue'
import api from '@/services/api'

const userStore = useUserStore()
const toastStore = useToastStore()

const saving = ref(false)
const user = computed(() => userStore.user)

const profile = reactive({
  age: null,
  gender: '',
  height_cm: null,
  weight_kg: null,
  body_fat_percentage: null,
  activity_level: 'moderately_active',
  primary_goal: 'maintain',
  timezone: 'UTC',
  bmr_calories: null,
  tdee_calories: null,
  target_calories: null,
  target_protein_g: null,
  target_carbs_g: null,
  target_fat_g: null
})

const hasBasicInfo = computed(() => {
  return profile.age && profile.gender && profile.height_cm && profile.weight_kg
})

const hasNutritionTargets = computed(() => {
  return profile.target_calories && profile.target_protein_g && profile.target_carbs_g && profile.target_fat_g
})

const calculatedBMI = computed(() => {
  if (!profile.height_cm || !profile.weight_kg) return '--'
  const heightM = profile.height_cm / 100
  const bmi = profile.weight_kg / (heightM * heightM)
  return bmi.toFixed(1)
})

const bmiStatus = computed(() => {
  const bmi = parseFloat(calculatedBMI.value)
  if (isNaN(bmi)) return { label: '--', class: '' }
  
  if (bmi < 18.5) return { label: 'Underweight', class: 'underweight' }
  if (bmi < 25) return { label: 'Normal', class: 'normal' }
  if (bmi < 30) return { label: 'Overweight', class: 'overweight' }
  return { label: 'Obese', class: 'obese' }
})

const loadProfile = async () => {
  try {
    const response = await api.get('/profile')
    Object.assign(profile, response.data)
  } catch (error) {
    if (error.response?.status !== 404) {
      console.error('Failed to load profile:', error)
      toastStore.error('Failed to load profile')
    }
  }
}

const saveProfile = async () => {
  try {
    saving.value = true
    
    // Filter out null/undefined values
    const profileData = Object.fromEntries(
      Object.entries(profile).filter(([_, value]) => value !== null && value !== '')
    )
    
    const response = await api.post('/profile', profileData)
    Object.assign(profile, response.data)
    
    toastStore.success('Profile saved successfully!')
    
  } catch (error) {
    console.error('Failed to save profile:', error)
    toastStore.error('Failed to save profile')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadProfile()
})
</script>

<style lang="scss" scoped>
.profile-page {
  padding: var(--space-xl);
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: var(--space-2xl);
  
  h1 {
    margin: 0;
    color: var(--text-primary);
  }
}

.profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: var(--space-xl);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .help-text {
    font-size: 0.875rem;
    color: var(--text-muted);
  }
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-lg);
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.form-actions {
  margin-top: var(--space-xl);
  padding-top: var(--space-lg);
  border-top: 1px solid var(--border);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-lg);
}

.metric-item {
  text-align: center;
  padding: var(--space-lg);
  background: var(--bg-secondary);
  border-radius: var(--radius);
  
  .metric-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-bottom: var(--space-sm);
  }
  
  .metric-value {
    font-size: 2rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: var(--space-xs);
  }
  
  .metric-unit {
    font-size: 0.75rem;
    color: var(--text-muted);
  }
  
  .metric-status {
    font-size: 0.875rem;
    font-weight: 500;
    border-radius: var(--radius);
    margin-top: var(--space-sm);
    
    &.underweight {
      background: #fef3c7;
      color: #92400e;
    }
    
    &.normal {
      background: #d1fae5;
      color: #065f46;
    }
    
    &.overweight {
      background: #fed7aa;
      color: #9a3412;
    }
    
    &.obese {
      background: #fecaca;
      color: #991b1b;
    }
  }
}

.targets-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-lg);
}

.target-item {
  text-align: center;
  
  .target-circle {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 0 auto var(--space-md) auto;
    color: white;
    
    &.calories {
      background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    }
    
    &.protein {
      background: linear-gradient(135deg, #ef4444, #dc2626);
    }
    
    &.carbs {
      background: linear-gradient(135deg, #f59e0b, #d97706);
    }
    
    &.fat {
      background: linear-gradient(135deg, #8b5cf6, #7c3aed);
    }
    
    .target-value {
      font-size: 1.5rem;
      font-weight: 600;
      line-height: 1;
    }
    
    .target-unit {
      font-size: 0.75rem;
      opacity: 0.8;
    }
  }
  
  .target-label {
    font-weight: 500;
    color: var(--text-primary);
  }
}

.no-metrics,
.no-targets {
  text-align: center;
  padding: var(--space-2xl);
  color: var(--text-muted);
  
  p {
    margin: var(--space-lg) 0 var(--space-md) 0;
    font-weight: 500;
  }
  
  small {
    line-height: 1.5;
  }
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-lg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: var(--space-md);
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-secondary);
  }
  
  &.danger {
    border-color: var(--error);
    
    &:hover {
      background: #fef2f2;
    }
  }
  
  &:last-child {
    margin-bottom: 0;
  }
}

.setting-info {
  flex: 1;
  
  h4 {
    margin: 0 0 var(--space-xs) 0;
    color: var(--text-primary);
    font-size: 1rem;
  }
  
  p {
    margin: 0;
    font-size: 0.875rem;
    color: var(--text-secondary);
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

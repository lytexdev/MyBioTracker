<template>
  <div class="dashboard-page">
    <div class="page-header">
      <h1>{{ $t('dashboard.title') }}</h1>
      <div class="date-display">
        {{ formatDate(new Date()) }}
      </div>
    </div>

    <div class="dashboard-grid">
      <!-- Quick Stats -->
      <div class="stats-row">
        <div class="stat-card nutrition">
          <div class="stat-icon">
            <Icon name="utensils" size="24" />
          </div>
          <div class="stat-content">
            <h3>{{ todaysCalories }}</h3>
            <p>{{ $t('dashboard.todaysCalories') }}</p>
            <div class="stat-progress">
              <div 
                class="progress-bar"
                :style="{ width: Math.min(100, (todaysCalories / userTargets.calories) * 100) + '%' }"
              ></div>
            </div>
            <small class="target-text">{{ $t('dashboard.goal') }}: {{ userTargets.calories }}</small>
          </div>
        </div>
        
        <div class="stat-card caffeine">
          <div class="stat-icon">
            <Icon name="coffee" size="24" />
          </div>
          <div class="stat-content">
            <h3>{{ currentCaffeine }}mg</h3>
            <p>{{ $t('dashboard.currentCaffeine') }}</p>
            <div class="caffeine-status" :class="getCaffeineStatus(currentCaffeine)">
              {{ getCaffeineStatusText(currentCaffeine) }}
            </div>
          </div>
        </div>
        
        <div class="stat-card streak">
          <div class="stat-icon">
            <Icon name="target" size="24" />
          </div>
          <div class="stat-content">
            <h3>{{ trackingStreak }}</h3>
            <p>{{ $t('dashboard.dayStreak') }}</p>
            <div class="streak-info">
              {{ $t('dashboard.keepItUp') }}
            </div>
          </div>
        </div>
        
        <div class="stat-card protein">
          <div class="stat-icon">
            <Icon name="zap" size="24" />
          </div>
          <div class="stat-content">
            <h3>{{ todaysProtein }}g</h3>
            <p>{{ $t('dashboard.proteinToday') }}</p>
            <div class="stat-progress">
              <div 
                class="progress-bar protein"
                :style="{ width: Math.min(100, (todaysProtein / userTargets.protein) * 100) + '%' }"
              ></div>
            </div>
            <small class="target-text">{{ $t('dashboard.goal') }}: {{ userTargets.protein }}g</small>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="card">
        <div class="card-header">
          <h3>{{ $t('dashboard.quickActions') }}</h3>
        </div>
        <div class="card-body">
          <div class="quick-actions">
            <router-link to="/nutrition/add-meal" class="action-btn">
              <Icon name="plus" size="20" />
              <span>{{ $t('dashboard.addMeal') }}</span>
            </router-link>
            <router-link to="/caffeine/add" class="action-btn">
              <Icon name="coffee" size="20" />
              <span>{{ $t('dashboard.logCaffeine') }}</span>
            </router-link>
            <router-link to="/nutrition/scan" class="action-btn">
              <Icon name="camera" size="20" />
              <span>{{ $t('dashboard.scanBarcode') }}</span>
            </router-link>
            <router-link to="/reports" class="action-btn">
              <Icon name="trending-up" size="20" />
              <span>{{ $t('dashboard.viewReports') }}</span>
            </router-link>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="card">
        <div class="card-header">
          <h3>{{ $t('dashboard.recentActivity') }}</h3>
          <router-link to="/nutrition" class="view-all-link">{{ $t('common.viewAll') }}</router-link>
        </div>
        <div class="card-body">
          <div v-if="recentActivity.length > 0" class="activity-list">
            <div
              v-for="item in recentActivity"
              :key="item.id"
              class="activity-item"
            >
              <div class="activity-icon" :class="item.type">
                <Icon :name="getActivityIcon(item.type)" size="18" />
              </div>
              <div class="activity-content">
                <h4>{{ item.title }}</h4>
                <p>{{ item.description }}</p>
                <time>{{ formatTimeAgo(item.timestamp) }}</time>
              </div>
            </div>
          </div>
          
          <div v-else class="empty-activity">
            <Icon name="clock" size="48" />
            <p>{{ $t('dashboard.noRecentActivity') }}</p>
            <router-link to="/nutrition/add-meal" class="btn btn-primary btn-sm">
              {{ $t('common.getStarted') }}
            </router-link>
          </div>
        </div>
      </div>

      <!-- Today's Progress -->
      <div class="card">
        <div class="card-header">
          <h3>{{ $t('dashboard.todaysProgress') }}</h3>
        </div>
        <div class="card-body">
          <div class="progress-grid">
            <div class="progress-item">
              <div class="progress-header">
                <span>{{ $t('dashboard.calories') }}</span>
                <span>{{ todaysCalories }} / {{ userTargets.calories }}</span>
              </div>
              <div class="progress-track">
                <div 
                  class="progress-fill calories"
                  :style="{ width: Math.min(100, (todaysCalories / userTargets.calories) * 100) + '%' }"
                ></div>
              </div>
            </div>
            
            <div class="progress-item">
              <div class="progress-header">
                <span>{{ $t('dashboard.protein') }}</span>
                <span>{{ todaysProtein }}g / {{ userTargets.protein }}g</span>
              </div>
              <div class="progress-track">
                <div 
                  class="progress-fill protein"
                  :style="{ width: Math.min(100, (todaysProtein / userTargets.protein) * 100) + '%' }"
                ></div>
              </div>
            </div>
            
            <div class="progress-item">
              <div class="progress-header">
                <span>{{ $t('dashboard.carbs') }}</span>
                <span>{{ todaysCarbs }}g / {{ userTargets.carbs }}g</span>
              </div>
              <div class="progress-track">
                <div 
                  class="progress-fill carbs"
                  :style="{ width: Math.min(100, (todaysCarbs / userTargets.carbs) * 100) + '%' }"
                ></div>
              </div>
            </div>
            
            <div class="progress-item">
              <div class="progress-header">
                <span>{{ $t('dashboard.fat') }}</span>
                <span>{{ todaysFat }}g / {{ userTargets.fat }}g</span>
              </div>
              <div class="progress-track">
                <div 
                  class="progress-fill fat"
                  :style="{ width: Math.min(100, (todaysFat / userTargets.fat) * 100) + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Weekly Summary -->
      <div class="card">
        <div class="card-header">
          <h3>{{ $t('dashboard.weeklyOverview') }}</h3>
        </div>
        <div class="card-body">
          <div class="weekly-stats">
            <div class="weekly-stat">
              <div class="stat-value">{{ weeklyStats.avgCalories }}</div>
              <div class="stat-label">{{ $t('dashboard.avgCalories') }}</div>
            </div>
            <div class="weekly-stat">
              <div class="stat-value">{{ weeklyStats.mealsLogged }}</div>
              <div class="stat-label">{{ $t('dashboard.mealsLogged') }}</div>
            </div>
            <div class="weekly-stat">
              <div class="stat-value">{{ weeklyStats.avgCaffeine }}mg</div>
              <div class="stat-label">{{ $t('dashboard.avgCaffeine') }}</div>
            </div>
            <div class="weekly-stat">
              <div class="stat-value">{{ weeklyStats.activeDays }}</div>
              <div class="stat-label">{{ $t('dashboard.activeDays') }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToastStore } from '@/stores/toast'
import Icon from '@/components/ui/Icon.vue'
import api from '@/services/api'

const { t } = useI18n()
const toastStore = useToastStore()

const todaysCalories = ref(0)
const todaysProtein = ref(0)
const todaysCarbs = ref(0)
const todaysFat = ref(0)
const currentCaffeine = ref(0)
const trackingStreak = ref(0)

// User targets from profile
const userTargets = reactive({
  calories: 2000,
  protein: 150,
  carbs: 250,
  fat: 67
})

const recentActivity = ref([])

const weeklyStats = reactive({
  avgCalories: 0,
  mealsLogged: 0,
  avgCaffeine: 0,
  activeDays: 0
})

const loadDashboardData = async () => {
  try {
    // Load user profile targets
    const profileResponse = await api.get('/profile')
    if (profileResponse.data) {
      userTargets.calories = profileResponse.data.target_calories || 2000
      userTargets.protein = profileResponse.data.target_protein_g || 150
      userTargets.carbs = profileResponse.data.target_carbs_g || 250
      userTargets.fat = profileResponse.data.target_fat_g || 67
    }

    // Load today's nutrition summary
    const today = new Date().toISOString().split('T')[0]
    const nutritionResponse = await api.get(`/nutrition/summary/${today}`)
    const nutritionData = nutritionResponse.data
    
    todaysCalories.value = Math.round(nutritionData.calories || 0)
    todaysProtein.value = Math.round(nutritionData.protein || 0)
    todaysCarbs.value = Math.round(nutritionData.carbs || 0)
    todaysFat.value = Math.round(nutritionData.fat || 0)
    
    // Load current caffeine level
    try {
      const caffeineResponse = await api.get('/caffeine/current-level')
      currentCaffeine.value = Math.round(caffeineResponse.data.current_level_mg || 0)
    } catch (error) {
      // Caffeine endpoint might not exist yet
      currentCaffeine.value = 0
    }
    
    // Load recent activity (mock data for now)
    recentActivity.value = [
      {
        id: 1,
        type: 'nutrition',
        title: t('nutrition.breakfast') + ' ' + t('common.add').toLowerCase(),
        description: 'Oatmeal with berries - 350 cal',
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString()
      },
      {
        id: 2,
        type: 'caffeine',
        title: t('caffeine.coffee') + ' ' + t('common.add').toLowerCase(),
        description: 'Large coffee - 95mg caffeine',
        timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString()
      },
      {
        id: 3,
        type: 'nutrition',
        title: t('nutrition.snack') + ' ' + t('common.add').toLowerCase(),
        description: 'Apple with peanut butter - 180 cal',
        timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString()
      }
    ]
    
    // Load weekly stats (mock data)
    Object.assign(weeklyStats, {
      avgCalories: 1850,
      mealsLogged: 18,
      avgCaffeine: 120,
      activeDays: 6
    })
    
    trackingStreak.value = 12
    
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
    toastStore.error(t('errors.unknownError'))
  }
}

const formatDate = (date) => {
  return date.toLocaleDateString(getCurrentLocale(), { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}

const getCurrentLocale = () => {
  return localStorage.getItem('mybiote-locale') || 'de'
}

const formatTimeAgo = (timestamp) => {
  const now = new Date()
  const time = new Date(timestamp)
  const diffHours = Math.floor((now - time) / (1000 * 60 * 60))
  
  if (diffHours < 1) return t('time.now')
  if (diffHours === 1) return t('time.hourAgo')
  if (diffHours < 24) return t('time.hoursAgo', { count: diffHours })
  
  const diffDays = Math.floor(diffHours / 24)
  if (diffDays === 1) return t('time.dayAgo')
  return t('time.daysAgo', { count: diffDays })
}

const getCaffeineStatus = (level) => {
  if (level < 50) return 'low'
  if (level < 100) return 'moderate'
  if (level < 200) return 'high'
  return 'very-high'
}

const getCaffeineStatusText = (level) => {
  if (level < 50) return t('caffeine.low')
  if (level < 100) return t('caffeine.moderate')
  if (level < 200) return t('caffeine.high')
  return t('caffeine.veryHigh')
}

const getActivityIcon = (type) => {
  const icons = {
    nutrition: 'utensils',
    caffeine: 'coffee',
    goal: 'target'
  }
  return icons[type] || 'info'
}

onMounted(() => {
  loadDashboardData()
})
</script>

<style lang="scss" scoped>
.dashboard-page {
  padding: var(--space-xl);
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-2xl);
  
  h1 {
    margin: 0;
    color: var(--text-primary);
  }
  
  .date-display {
    color: var(--text-secondary);
    font-size: 0.875rem;
  }
}

.dashboard-grid {
  display: grid;
  gap: var(--space-xl);
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-lg);
}

.stat-card {
  display: flex;
  align-items: center;
  gap: var(--space-lg);
  padding: var(--space-lg);
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  transition: var(--transition);
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  &.nutrition .stat-icon {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  }
  
  &.caffeine .stat-icon {
    background: linear-gradient(135deg, #f59e0b, #d97706);
  }
  
  &.streak .stat-icon {
    background: linear-gradient(135deg, #10b981, #059669);
  }
  
  &.protein .stat-icon {
    background: linear-gradient(135deg, #ef4444, #dc2626);
  }
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
  
  h3 {
    margin: 0 0 var(--space-xs) 0;
    font-size: 1.75rem;
    font-weight: 600;
    color: var(--text-primary);
  }
  
  p {
    margin: 0 0 var(--space-sm) 0;
    color: var(--text-secondary);
    font-size: 0.875rem;
  }
  
  .target-text {
    display: block;
    margin-top: var(--space-xs);
    color: var(--text-muted);
    font-size: 0.75rem;
  }
}

.stat-progress {
  height: 4px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-sm);
  overflow: hidden;
  
  .progress-bar {
    height: 100%;
    background: linear-gradient(90deg, var(--primary), var(--primary-dark));
    border-radius: var(--radius-sm);
    transition: width var(--transition);
    
    &.protein {
      background: linear-gradient(90deg, #ef4444, #dc2626);
    }
  }
}

.caffeine-status {
  font-size: 0.75rem;
  font-weight: 500;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  
  &.low {
    color: #065f46;
    background: #d1fae5;
  }
  
  &.moderate {
    color: #92400e;
    background: #fef3c7;
  }
  
  &.high {
    color: #9a3412;
    background: #fed7aa;
  }
  
  &.very-high {
    color: #991b1b;
    background: #fecaca;
  }
}

.streak-info {
  font-size: 0.75rem;
  color: var(--success);
  font-weight: 500;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: var(--space-md);
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-lg);
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  text-decoration: none;
  color: var(--text-secondary);
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-tertiary);
    border-color: var(--primary);
    color: var(--text-primary);
    transform: translateY(-2px);
  }
  
  span {
    font-size: 0.875rem;
    font-weight: 500;
  }
}

.view-all-link {
  color: var(--primary);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  
  &:hover {
    text-decoration: underline;
  }
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-md);
  padding: var(--space-md);
  background: var(--bg-secondary);
  border-radius: var(--radius);
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-tertiary);
  }
}

.activity-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  
  &.nutrition {
    background: var(--primary);
  }
  
  &.caffeine {
    background: #f59e0b;
  }
  
  &.goal {
    background: #10b981;
  }
}

.activity-content {
  flex: 1;
  
  h4 {
    margin: 0 0 var(--space-xs) 0;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-primary);
  }
  
  p {
    margin: 0 0 var(--space-xs) 0;
    font-size: 0.75rem;
    color: var(--text-secondary);
  }
  
  time {
    font-size: 0.75rem;
    color: var(--text-muted);
  }
}

.empty-activity {
  text-align: center;
  padding: var(--space-2xl);
  color: var(--text-muted);
  
  p {
    margin: var(--space-lg) 0;
  }
}

.progress-grid {
  display: grid;
  gap: var(--space-lg);
}

.progress-item {
  .progress-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: var(--space-sm);
    font-size: 0.875rem;
    
    span:first-child {
      font-weight: 500;
      color: var(--text-primary);
    }
    
    span:last-child {
      color: var(--text-secondary);
    }
  }
}

.progress-track {
  height: 8px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: var(--radius-sm);
  transition: width var(--transition);
  
  &.calories {
    background: linear-gradient(90deg, var(--primary), var(--primary-dark));
  }
  
  &.protein {
    background: linear-gradient(90deg, #ef4444, #dc2626);
  }
  
  &.carbs {
    background: linear-gradient(90deg, #f59e0b, #d97706);
  }
  
  &.fat {
    background: linear-gradient(90deg, #8b5cf6, #7c3aed);
  }
}

.weekly-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: var(--space-lg);
  text-align: center;
}

.weekly-stat {
  .stat-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: var(--space-xs);
  }
  
  .stat-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
  }
}

@media (max-width: 768px) {
  .dashboard-page {
    padding: var(--space-lg);
  }
  
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .quick-actions {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .weekly-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>

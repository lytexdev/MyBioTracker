<template>
  <div class="nutrition-page">
    <div class="page-header">
      <h1>Nutrition Tracking</h1>
      <div class="header-actions">
        <router-link to="/nutrition/scan" class="btn btn-outline">
          <Icon name="camera" size="18" />
          Scan Barcode
        </router-link>
        <router-link to="/nutrition/add-meal" class="btn btn-primary">
          <Icon name="plus" size="18" />
          Add Meal
        </router-link>
      </div>
    </div>

    <div class="nutrition-grid">
      <!-- Today's Summary -->
      <div class="card summary-card">
        <div class="card-header">
          <h3>Today's Summary</h3>
          <span class="date">{{ formatDate(new Date()) }}</span>
        </div>
        <div class="card-body">
          <div v-if="todaysSummary" class="summary-stats">
            <div class="stat">
              <div class="stat-value">{{ Math.round(todaysSummary.calories) }}</div>
              <div class="stat-label">Calories</div>
              <div class="stat-target">Goal: {{ targetCalories }}</div>
            </div>
            <div class="stat">
              <div class="stat-value">{{ Math.round(todaysSummary.protein) }}g</div>
              <div class="stat-label">Protein</div>
              <div class="stat-target">Goal: {{ targetProtein }}g</div>
            </div>
            <div class="stat">
              <div class="stat-value">{{ Math.round(todaysSummary.carbs) }}g</div>
              <div class="stat-label">Carbs</div>
              <div class="stat-target">Goal: {{ targetCarbs }}g</div>
            </div>
            <div class="stat">
              <div class="stat-value">{{ Math.round(todaysSummary.fat) }}g</div>
              <div class="stat-label">Fat</div>
              <div class="stat-target">Goal: {{ targetFat }}g</div>
            </div>
          </div>
          <div v-else class="empty-summary">
            <Icon name="utensils" size="48" />
            <p>No meals logged today</p>
            <router-link to="/nutrition/add-meal" class="btn btn-primary btn-sm">
              Log Your First Meal
            </router-link>
          </div>
        </div>
      </div>

      <!-- Recent Meals -->
      <div class="card meals-card">
        <div class="card-header">
          <h3>Recent Meals</h3>
          <div class="filter-tabs">
            <button 
              v-for="filter in mealFilters" 
              :key="filter.value"
              @click="selectedFilter = filter.value"
              :class="['filter-tab', { active: selectedFilter === filter.value }]"
            >
              {{ filter.label }}
            </button>
          </div>
        </div>
        <div class="card-body">
          <div v-if="filteredMeals.length > 0" class="meals-list">
            <div 
              v-for="meal in filteredMeals" 
              :key="meal.id"
              class="meal-item"
            >
              <div class="meal-info">
                <h4>{{ meal.name }}</h4>
                <div class="meal-meta">
                  <span class="meal-type">{{ formatMealType(meal.meal_type) }}</span>
                  <span class="meal-time">{{ formatTime(meal.eaten_at) }}</span>
                </div>
              </div>
              <div class="meal-calories">
                <span class="calories">{{ calculateMealCalories(meal) }}</span>
                <small>cal</small>
              </div>
              <div class="meal-actions">
                <button @click="editMeal(meal)" class="btn-icon">
                  <Icon name="edit" size="16" />
                </button>
                <button @click="deleteMeal(meal)" class="btn-icon btn-danger">
                  <Icon name="trash" size="16" />
                </button>
              </div>
            </div>
          </div>
          <div v-else class="empty-state">
            <Icon name="utensils" size="48" />
            <p>No meals found</p>
            <router-link to="/nutrition/add-meal" class="btn btn-primary btn-sm">
              Add Meal
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Progress Charts -->
    <div class="card charts-card">
      <div class="card-header">
        <h3>Nutrition Progress</h3>
      </div>
      <div class="card-body">
        <div class="progress-grid">
          <div class="progress-item">
            <div class="progress-label">
              <span>Calories</span>
              <span>{{ Math.round(todaysSummary?.calories || 0) }} / {{ targetCalories }}</span>
            </div>
            <div class="progress-bar">
              <div 
                class="progress-fill calories"
                :style="{ width: Math.min(100, ((todaysSummary?.calories || 0) / targetCalories) * 100) + '%' }"
              ></div>
            </div>
          </div>
          
          <div class="progress-item">
            <div class="progress-label">
              <span>Protein</span>
              <span>{{ Math.round(todaysSummary?.protein || 0) }}g / {{ targetProtein }}g</span>
            </div>
            <div class="progress-bar">
              <div 
                class="progress-fill protein"
                :style="{ width: Math.min(100, ((todaysSummary?.protein || 0) / targetProtein) * 100) + '%' }"
              ></div>
            </div>
          </div>
          
          <div class="progress-item">
            <div class="progress-label">
              <span>Carbs</span>
              <span>{{ Math.round(todaysSummary?.carbs || 0) }}g / {{ targetCarbs }}g</span>
            </div>
            <div class="progress-bar">
              <div 
                class="progress-fill carbs"
                :style="{ width: Math.min(100, ((todaysSummary?.carbs || 0) / targetCarbs) * 100) + '%' }"
              ></div>
            </div>
          </div>
          
          <div class="progress-item">
            <div class="progress-label">
              <span>Fat</span>
              <span>{{ Math.round(todaysSummary?.fat || 0) }}g / {{ targetFat }}g</span>
            </div>
            <div class="progress-bar">
              <div 
                class="progress-fill fat"
                :style="{ width: Math.min(100, ((todaysSummary?.fat || 0) / targetFat) * 100) + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useToastStore } from '@/stores/toast'
import Icon from '@/components/ui/Icon.vue'
import api from '@/services/api'

const toastStore = useToastStore()

const todaysSummary = ref(null)
const meals = ref([])
const selectedFilter = ref('all')
const loading = ref(false)

// Mock targets - these should come from user profile
const targetCalories = ref(2000)
const targetProtein = ref(150)
const targetCarbs = ref(250)
const targetFat = ref(67)

const mealFilters = [
  { label: 'All', value: 'all' },
  { label: 'Today', value: 'today' },
  { label: 'Yesterday', value: 'yesterday' },
  { label: 'This Week', value: 'week' }
]

const filteredMeals = computed(() => {
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const yesterday = new Date(today.getTime() - 24 * 60 * 60 * 1000)
  const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000)

  return meals.value.filter(meal => {
    const mealDate = new Date(meal.eaten_at)
    
    switch (selectedFilter.value) {
      case 'today':
        return mealDate >= today
      case 'yesterday':
        return mealDate >= yesterday && mealDate < today
      case 'week':
        return mealDate >= weekAgo
      default:
        return true
    }
  })
})

const loadNutritionData = async () => {
  try {
    loading.value = true
    
    // Load today's summary
    const today = new Date().toISOString().split('T')[0]
    const summaryResponse = await api.get(`/nutrition/summary/${today}`)
    todaysSummary.value = summaryResponse.data
    
    // Load recent meals
    const mealsResponse = await api.get('/nutrition/meals')
    meals.value = mealsResponse.data
    
  } catch (error) {
    console.error('Failed to load nutrition data:', error)
    toastStore.error('Failed to load nutrition data')
  } finally {
    loading.value = false
  }
}

const formatDate = (date) => {
  return date.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}

const formatTime = (dateString) => {
  return new Date(dateString).toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}

const formatMealType = (type) => {
  const types = {
    breakfast: 'Breakfast',
    lunch: 'Lunch',
    dinner: 'Dinner',
    snack: 'Snack'
  }
  return types[type] || type
}

const calculateMealCalories = (meal) => {
  // This would calculate from meal entries
  // For now, return a placeholder
  return Math.floor(Math.random() * 400) + 200
}

const editMeal = (meal) => {
  // Navigate to edit meal page
  console.log('Edit meal:', meal)
}

const deleteMeal = async (meal) => {
  if (confirm('Are you sure you want to delete this meal?')) {
    try {
      await api.delete(`/nutrition/meals/${meal.id}`)
      meals.value = meals.value.filter(m => m.id !== meal.id)
      toastStore.success('Meal deleted successfully')
      
      // Reload summary
      await loadNutritionData()
    } catch (error) {
      console.error('Failed to delete meal:', error)
      toastStore.error('Failed to delete meal')
    }
  }
}

onMounted(() => {
  loadNutritionData()
})
</script>

<style lang="scss" scoped>
.nutrition-page {
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
  
  .header-actions {
    display: flex;
    gap: var(--space-md);
  }
}

.nutrition-grid {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: var(--space-xl);
  margin-bottom: var(--space-xl);
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.summary-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .date {
      font-size: 0.875rem;
      color: var(--text-muted);
    }
  }
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-lg);
}

.stat {
  text-align: center;
  
  .stat-value {
    font-size: 2rem;
    font-weight: 600;
    color: var(--primary);
    margin-bottom: var(--space-xs);
  }
  
  .stat-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-bottom: var(--space-xs);
  }
  
  .stat-target {
    font-size: 0.75rem;
    color: var(--text-muted);
  }
}

.filter-tabs {
  display: flex;
  gap: var(--space-xs);
}

.filter-tab {
  padding: var(--space-xs) var(--space-md);
  border: 1px solid var(--border);
  background: none;
  border-radius: var(--radius);
  font-size: 0.875rem;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-secondary);
  }
  
  &.active {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
  }
}

.meals-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.meal-item {
  display: flex;
  align-items: center;
  padding: var(--space-md);
  background: var(--bg-secondary);
  border-radius: var(--radius);
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-tertiary);
  }
}

.meal-info {
  flex: 1;
  
  h4 {
    margin: 0 0 var(--space-xs) 0;
    color: var(--text-primary);
  }
  
  .meal-meta {
    display: flex;
    gap: var(--space-md);
    font-size: 0.875rem;
    
    .meal-type {
      color: var(--primary);
      font-weight: 500;
    }
    
    .meal-time {
      color: var(--text-muted);
    }
  }
}

.meal-calories {
  margin-right: var(--space-lg);
  text-align: center;
  
  .calories {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
  }
  
  small {
    display: block;
    color: var(--text-muted);
    font-size: 0.75rem;
  }
}

.meal-actions {
  display: flex;
  gap: var(--space-sm);
}

.btn-icon {
  width: 32px;
  height: 32px;
  border: none;
  background: var(--bg-primary);
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-tertiary);
    color: var(--text-primary);
  }
  
  &.btn-danger {
    &:hover {
      background: var(--error);
      color: white;
    }
  }
}

.charts-card {
  grid-column: 1 / -1;
}

.progress-grid {
  display: grid;
  gap: var(--space-lg);
}

.progress-item {
  .progress-label {
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

.progress-bar {
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

.empty-state,
.empty-summary {
  text-align: center;
  padding: var(--space-2xl);
  color: var(--text-muted);
  
  p {
    margin: var(--space-lg) 0;
  }
}
</style>

<template>
  <div class="add-meal-page">
    <div class="page-header">
      <h1>Add Meal</h1>
      <router-link to="/nutrition" class="btn btn-outline">
        <Icon name="chevron-left" size="18" />
        Back to Nutrition
      </router-link>
    </div>

    <div class="add-meal-content">
      <form @submit.prevent="saveMeal" class="meal-form">
        <!-- Meal Info -->
        <div class="card">
          <div class="card-header">
            <h3>Meal Information</h3>
          </div>
          <div class="card-body">
            <div class="form-grid">
              <div class="form-group">
                <label for="mealName" class="form-label">Meal Name *</label>
                <input
                  id="mealName"
                  v-model="meal.name"
                  type="text"
                  class="form-input"
                  placeholder="e.g., Breakfast, Lunch, Protein Shake"
                  required
                >
              </div>

              <div class="form-group">
                <label for="mealType" class="form-label">Meal Type *</label>
                <select id="mealType" v-model="meal.meal_type" class="form-select" required>
                  <option value="">Select meal type</option>
                  <option value="breakfast">Breakfast</option>
                  <option value="lunch">Lunch</option>
                  <option value="dinner">Dinner</option>
                  <option value="snack">Snack</option>
                </select>
              </div>

              <div class="form-group">
                <label for="eatenAt" class="form-label">Date & Time *</label>
                <input
                  id="eatenAt"
                  v-model="meal.eaten_at"
                  type="datetime-local"
                  class="form-input"
                  required
                >
              </div>

              <div class="form-group full-width">
                <label for="notes" class="form-label">Notes (Optional)</label>
                <textarea
                  id="notes"
                  v-model="meal.notes"
                  class="form-textarea"
                  placeholder="Any additional notes about this meal..."
                  rows="3"
                ></textarea>
              </div>
            </div>
          </div>
        </div>

        <!-- Food Search & Add -->
        <div class="card">
          <div class="card-header">
            <h3>Add Foods</h3>
            <div class="header-actions">
              <router-link to="/nutrition/scan" class="btn btn-outline btn-sm">
                <Icon name="camera" size="16" />
                Scan Barcode
              </router-link>
            </div>
          </div>
          <div class="card-body">
            <!-- Food Search -->
            <div class="food-search">
              <div class="search-input-group">
                <input
                  v-model="searchQuery"
                  type="text"
                  class="form-input"
                  placeholder="Search for foods..."
                  @input="searchFoods"
                >
                <button type="button" class="search-btn" @click="searchFoods">
                  <Icon name="search" size="18" />
                </button>
              </div>

              <!-- Search Results -->
              <div v-if="searchResults.length > 0" class="search-results">
                <div
                  v-for="food in searchResults"
                  :key="food.id"
                  class="search-result-item"
                  @click="selectFood(food)"
                >
                  <div class="food-info">
                    <h4>{{ food.name }}</h4>
                    <p v-if="food.brand" class="food-brand">{{ food.brand }}</p>
                    <p class="food-calories">{{ food.calories_per_100g }} cal per 100g</p>
                  </div>
                  <button type="button" class="btn btn-sm btn-primary">
                    <Icon name="plus" size="16" />
                    Add
                  </button>
                </div>
              </div>

              <div v-else-if="searchQuery && !searching" class="no-results">
                <p>No foods found for "{{ searchQuery }}"</p>
                <button type="button" class="btn btn-outline btn-sm" @click="createCustomFood">
                  <Icon name="plus" size="16" />
                  Create Custom Food
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Selected Foods -->
        <div v-if="selectedFoods.length > 0" class="card">
          <div class="card-header">
            <h3>Selected Foods</h3>
            <div class="nutrition-summary">
              <span>Total: {{ totalCalories }} cal, {{ totalProtein }}g protein</span>
            </div>
          </div>
          <div class="card-body">
            <div class="selected-foods-list">
              <div
                v-for="(item, index) in selectedFoods"
                :key="index"
                class="selected-food-item"
              >
                <div class="food-details">
                  <h4>{{ item.food.name }}</h4>
                  <p v-if="item.food.brand" class="food-brand">{{ item.food.brand }}</p>
                </div>

                <div class="amount-input">
                  <label>Amount (g)</label>
                  <input
                    v-model.number="item.amount_grams"
                    type="number"
                    min="1"
                    class="form-input"
                    @input="updateNutrition"
                  >
                </div>

                <div class="food-nutrition">
                  <div class="nutrition-item">
                    <span class="value">{{ calculateCalories(item) }}</span>
                    <span class="label">cal</span>
                  </div>
                  <div class="nutrition-item">
                    <span class="value">{{ calculateProtein(item) }}g</span>
                    <span class="label">protein</span>
                  </div>
                </div>

                <button
                  type="button"
                  class="remove-btn"
                  @click="removeFood(index)"
                >
                  <Icon name="x" size="16" />
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Submit -->
        <div class="form-actions">
          <router-link to="/nutrition" class="btn btn-outline">Cancel</router-link>
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="loading || selectedFoods.length === 0"
          >
            <Icon v-if="loading" name="loader" class="animate-spin" />
            {{ loading ? 'Saving...' : 'Save Meal' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToastStore } from '@/stores/toast'
import Icon from '@/components/ui/Icon.vue'
import api from '@/services/api'

const router = useRouter()
const toastStore = useToastStore()

const loading = ref(false)
const searching = ref(false)
const searchQuery = ref('')
const searchResults = ref([])
const selectedFoods = ref([])

const meal = reactive({
  name: '',
  meal_type: '',
  eaten_at: new Date().toISOString().slice(0, 16),
  notes: ''
})

const totalCalories = computed(() => {
  return Math.round(selectedFoods.value.reduce((total, item) => {
    return total + calculateCalories(item)
  }, 0))
})

const totalProtein = computed(() => {
  return Math.round(selectedFoods.value.reduce((total, item) => {
    return total + calculateProtein(item)
  }, 0))
})

const searchFoods = async () => {
  if (!searchQuery.value.trim()) return

  try {
    searching.value = true
    const response = await api.get(`/nutrition/foods/search?q=${encodeURIComponent(searchQuery.value)}`)
    searchResults.value = response.data
  } catch (error) {
    console.error('Search failed:', error)
    toastStore.error('Failed to search foods')
  } finally {
    searching.value = false
  }
}

const selectFood = (food) => {
  selectedFoods.value.push({
    food: food,
    amount_grams: 100
  })
  searchResults.value = []
  searchQuery.value = ''
}

const removeFood = (index) => {
  selectedFoods.value.splice(index, 1)
}

const calculateCalories = (item) => {
  return Math.round((item.food.calories_per_100g * item.amount_grams) / 100)
}

const calculateProtein = (item) => {
  return Math.round((item.food.protein_per_100g * item.amount_grams) / 100)
}

const updateNutrition = () => {
  // Trigger reactivity update
}

const createCustomFood = () => {
  // Navigate to create custom food page or show modal
  toastStore.info('Custom food creation coming soon!')
}

const saveMeal = async () => {
  if (selectedFoods.value.length === 0) {
    toastStore.error('Please add at least one food item')
    return
  }

  try {
    loading.value = true

    // Create meal
    const mealResponse = await api.post('/nutrition/meals', meal)
    const createdMeal = mealResponse.data

    // Add food entries
    for (const item of selectedFoods.value) {
      await api.post('/nutrition/entries', {
        meal_id: createdMeal.id,
        food_item_id: item.food.id,
        amount_grams: item.amount_grams
      })
    }

    toastStore.success('Meal saved successfully!')
    router.push('/nutrition')

  } catch (error) {
    console.error('Failed to save meal:', error)
    toastStore.error('Failed to save meal')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // Set default meal name based on time
  const hour = new Date().getHours()
  if (hour < 11) {
    meal.meal_type = 'breakfast'
    meal.name = 'Breakfast'
  } else if (hour < 16) {
    meal.meal_type = 'lunch'
    meal.name = 'Lunch'
  } else {
    meal.meal_type = 'dinner'
    meal.name = 'Dinner'
  }
})
</script>

<style lang="scss" scoped>
.add-meal-page {
  padding: var(--space-xl);
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-2xl);
  
  h1 {
    margin: 0;
  }
}

.meal-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-lg);
  
  .full-width {
    grid-column: 1 / -1;
  }
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.header-actions {
  display: flex;
  gap: var(--space-sm);
}

.food-search {
  .search-input-group {
    display: flex;
    margin-bottom: var(--space-lg);
    
    .form-input {
    .search-btn {
      border: 1px solid var(--border);
      border-left: none;
      border-radius: 0 var(--radius) var(--radius) 0;
      background: var(--bg-secondary);
      color: var(--text-secondary);
      padding: 0 var(--space-lg);
      cursor: pointer;
      transition: var(--transition);
      
      &:hover {
        background: var(--bg-tertiary);
        color: var(--text-primary);
      }
    }
  }
}

.search-results {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--bg-primary);
}

.search-result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-md);
  border-bottom: 1px solid var(--border-light);
  cursor: pointer;
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-secondary);
  }
  
  &:last-child {
    border-bottom: none;
  }
}

.food-info {
  flex: 1;
  
  h4 {
    margin: 0 0 var(--space-xs) 0;
    font-size: 1rem;
    color: var(--text-primary);
  }
  
  .food-brand {
    margin: 0;
    font-size: 0.875rem;
    color: var(--text-secondary);
  }
  
  .food-calories {
    margin: var(--space-xs) 0 0 0;
    font-size: 0.75rem;
    color: var(--text-muted);
  }
}

.no-results {
  text-align: center;
  padding: var(--space-xl);
  color: var(--text-muted);
  
  p {
    margin-bottom: var(--space-lg);
  }
}

.nutrition-summary {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.selected-foods-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.selected-food-item {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr auto;
  gap: var(--space-lg);
  align-items: center;
  padding: var(--space-md);
  background: var(--bg-secondary);
  border-radius: var(--radius);
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: var(--space-md);
  }
}

.food-details {
  h4 {
    margin: 0 0 var(--space-xs) 0;
    font-size: 1rem;
    color: var(--text-primary);
  }
  
  .food-brand {
    margin: 0;
    font-size: 0.875rem;
    color: var(--text-secondary);
  }
}

.amount-input {
  label {
    display: block;
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-bottom: var(--space-xs);
  }
  
  .form-input {
    width: 100%;
  }
}

.food-nutrition {
  display: flex;
  gap: var(--space-md);
  
  @media (max-width: 768px) {
    justify-content: center;
  }
}

.nutrition-item {
  text-align: center;
  
  .value {
    display: block;
    font-weight: 600;
    color: var(--text-primary);
  }
  
  .label {
    font-size: 0.75rem;
    color: var(--text-muted);
  }
}

.remove-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: var(--error);
  color: white;
  border-radius: var(--radius);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  
  &:hover {
    background: #dc2626;
  }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-md);
  padding-top: var(--space-lg);
  border-top: 1px solid var(--border);
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
}
</style>
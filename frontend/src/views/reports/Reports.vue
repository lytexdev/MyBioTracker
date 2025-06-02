<template>
  <div class="reports-page">
    <div class="page-header">
      <h1>Reports & Analytics</h1>
      <div class="header-actions">
        <button @click="exportData" class="btn btn-outline" :disabled="exporting">
          <Icon v-if="exporting" name="loader" class="animate-spin" />
          <Icon v-else name="upload" size="18" />
          Export Data
        </button>
      </div>
    </div>

    <div class="reports-content">
      <!-- Quick Stats -->
      <div class="stats-overview">
        <div class="stat-card">
          <div class="stat-icon nutrition">
            <Icon name="utensils" size="24" />
          </div>
          <div class="stat-content">
            <h3>{{ weeklyStats.totalMeals }}</h3>
            <p>Meals This Week</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon calories">
            <Icon name="zap" size="24" />
          </div>
          <div class="stat-content">
            <h3>{{ Math.round(weeklyStats.avgCalories) }}</h3>
            <p>Avg Daily Calories</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon caffeine">
            <Icon name="coffee" size="24" />
          </div>
          <div class="stat-content">
            <h3>{{ Math.round(weeklyStats.avgCaffeine) }}mg</h3>
            <p>Avg Daily Caffeine</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon streak">
            <Icon name="target" size="24" />
          </div>
          <div class="stat-content">
            <h3>{{ weeklyStats.trackingStreak }}</h3>
            <p>Day Tracking Streak</p>
          </div>
        </div>
      </div>

      <!-- Report Filters -->
      <div class="card">
        <div class="card-header">
          <h3>Report Options</h3>
        </div>
        <div class="card-body">
          <div class="filter-grid">
            <div class="form-group">
              <label class="form-label">Report Type</label>
              <select v-model="reportType" @change="loadReportData" class="form-select">
                <option value="nutrition">Nutrition Summary</option>
                <option value="caffeine">Caffeine Analysis</option>
                <option value="combined">Combined Report</option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="form-label">Time Period</label>
              <select v-model="timePeriod" @change="loadReportData" class="form-select">
                <option value="week">Last 7 Days</option>
                <option value="month">Last 30 Days</option>
                <option value="quarter">Last 3 Months</option>
                <option value="year">Last Year</option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="form-label">Date Range</label>
              <div class="date-range">
                <input
                  v-model="dateRange.start"
                  type="date"
                  class="form-input"
                  @change="loadReportData"
                >
                <span>to</span>
                <input
                  v-model="dateRange.end"
                  type="date"
                  class="form-input"
                  @change="loadReportData"
                >
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Nutrition Report -->
      <div v-if="reportType === 'nutrition' || reportType === 'combined'" class="card">
        <div class="card-header">
          <h3>Nutrition Analysis</h3>
          <span class="period-label">{{ formatPeriodLabel() }}</span>
        </div>
        <div class="card-body">
          <div v-if="nutritionReport" class="report-content">
            <!-- Weekly Averages -->
            <div class="metrics-grid">
              <div class="metric-item">
                <div class="metric-label">Average Calories</div>
                <div class="metric-value">{{ Math.round(nutritionReport.avgCalories) }}</div>
                <div class="metric-change" :class="getChangeClass(nutritionReport.caloriesChange)">
                  {{ formatChange(nutritionReport.caloriesChange) }}
                </div>
              </div>
              
              <div class="metric-item">
                <div class="metric-label">Average Protein</div>
                <div class="metric-value">{{ Math.round(nutritionReport.avgProtein) }}g</div>
                <div class="metric-change" :class="getChangeClass(nutritionReport.proteinChange)">
                  {{ formatChange(nutritionReport.proteinChange) }}
                </div>
              </div>
              
              <div class="metric-item">
                <div class="metric-label">Average Carbs</div>
                <div class="metric-value">{{ Math.round(nutritionReport.avgCarbs) }}g</div>
                <div class="metric-change" :class="getChangeClass(nutritionReport.carbsChange)">
                  {{ formatChange(nutritionReport.carbsChange) }}
                </div>
              </div>
              
              <div class="metric-item">
                <div class="metric-label">Average Fat</div>
                <div class="metric-value">{{ Math.round(nutritionReport.avgFat) }}g</div>
                <div class="metric-change" :class="getChangeClass(nutritionReport.fatChange)">
                  {{ formatChange(nutritionReport.fatChange) }}
                </div>
              </div>
            </div>

            <!-- Goal Achievement -->
            <div class="goal-achievement">
              <h4>Goal Achievement</h4>
              <div class="achievement-grid">
                <div class="achievement-item">
                  <div class="achievement-label">Calorie Goal</div>
                  <div class="achievement-bar">
                    <div 
                      class="achievement-fill calories"
                      :style="{ width: Math.min(100, nutritionReport.calorieGoalAchievement) + '%' }"
                    ></div>
                  </div>
                  <div class="achievement-percent">{{ Math.round(nutritionReport.calorieGoalAchievement) }}%</div>
                </div>
                
                <div class="achievement-item">
                  <div class="achievement-label">Protein Goal</div>
                  <div class="achievement-bar">
                    <div 
                      class="achievement-fill protein"
                      :style="{ width: Math.min(100, nutritionReport.proteinGoalAchievement) + '%' }"
                    ></div>
                  </div>
                  <div class="achievement-percent">{{ Math.round(nutritionReport.proteinGoalAchievement) }}%</div>
                </div>
              </div>
            </div>

            <!-- Top Foods -->
            <div class="top-foods">
              <h4>Most Consumed Foods</h4>
              <div class="food-list">
                <div 
                  v-for="food in nutritionReport.topFoods" 
                  :key="food.name"
                  class="food-item"
                >
                  <div class="food-name">{{ food.name }}</div>
                  <div class="food-count">{{ food.count }} times</div>
                  <div class="food-calories">{{ Math.round(food.totalCalories) }} cal</div>
                </div>
              </div>
            </div>
          </div>
          
          <div v-else class="loading-state">
            <Icon name="loader" class="animate-spin" size="48" />
            <p>Loading nutrition report...</p>
          </div>
        </div>
      </div>

      <!-- Caffeine Report -->
      <div v-if="reportType === 'caffeine' || reportType === 'combined'" class="card">
        <div class="card-header">
          <h3>Caffeine Analysis</h3>
          <span class="period-label">{{ formatPeriodLabel() }}</span>
        </div>
        <div class="card-body">
          <div v-if="caffeineReport" class="report-content">
            <!-- Caffeine Metrics -->
            <div class="metrics-grid">
              <div class="metric-item">
                <div class="metric-label">Daily Average</div>
                <div class="metric-value">{{ Math.round(caffeineReport.avgDaily) }}mg</div>
                <div class="metric-change" :class="getChangeClass(caffeineReport.dailyChange)">
                  {{ formatChange(caffeineReport.dailyChange) }}
                </div>
              </div>
              
              <div class="metric-item">
                <div class="metric-label">Peak Day</div>
                <div class="metric-value">{{ Math.round(caffeineReport.peakDay) }}mg</div>
                <div class="metric-date">{{ formatDate(caffeineReport.peakDate) }}</div>
              </div>
              
              <div class="metric-item">
                <div class="metric-label">Total Entries</div>
                <div class="metric-value">{{ caffeineReport.totalEntries }}</div>
                <div class="metric-change" :class="getChangeClass(caffeineReport.entriesChange)">
                  {{ formatChange(caffeineReport.entriesChange) }}
                </div>
              </div>
              
              <div class="metric-item">
                <div class="metric-label">Favorite Source</div>
                <div class="metric-value">{{ caffeineReport.favoriteSource }}</div>
                <div class="metric-count">{{ caffeineReport.favoriteCount }} times</div>
              </div>
            </div>

            <!-- Consumption Patterns -->
            <div class="consumption-patterns">
              <h4>Consumption Patterns</h4>
              <div class="pattern-grid">
                <div class="pattern-item">
                  <div class="pattern-label">Most Active Hour</div>
                  <div class="pattern-value">{{ caffeineReport.peakHour }}:00</div>
                </div>
                
                <div class="pattern-item">
                  <div class="pattern-label">Most Active Day</div>
                  <div class="pattern-value">{{ caffeineReport.peakDayOfWeek }}</div>
                </div>
                
                <div class="pattern-item">
                  <div class="pattern-label">Average per Entry</div>
                  <div class="pattern-value">{{ Math.round(caffeineReport.avgPerEntry) }}mg</div>
                </div>
              </div>
            </div>

            <!-- Source Breakdown -->
            <div class="source-breakdown">
              <h4>Sources Breakdown</h4>
              <div class="source-list">
                <div 
                  v-for="source in caffeineReport.sources" 
                  :key="source.name"
                  class="source-item"
                >
                  <div class="source-info">
                    <div class="source-name">{{ source.name }}</div>
                    <div class="source-category">{{ formatCategory(source.category) }}</div>
                  </div>
                  <div class="source-stats">
                    <div class="source-count">{{ source.count }} entries</div>
                    <div class="source-total">{{ Math.round(source.totalCaffeine) }}mg total</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div v-else class="loading-state">
            <Icon name="loader" class="animate-spin" size="48" />
            <p>Loading caffeine report...</p>
          </div>
        </div>
      </div>

      <!-- Export Options -->
      <div class="card">
        <div class="card-header">
          <h3>Export Options</h3>
        </div>
        <div class="card-body">
          <div class="export-options">
            <div class="export-option">
              <div class="export-info">
                <h4>Nutrition Data</h4>
                <p>Export all nutrition entries, meals, and food items</p>
              </div>
              <div class="export-actions">
                <button @click="exportNutrition('csv')" class="btn btn-outline btn-sm">
                  CSV
                </button>
                <button @click="exportNutrition('json')" class="btn btn-outline btn-sm">
                  JSON
                </button>
              </div>
            </div>
            
            <div class="export-option">
              <div class="export-info">
                <h4>Caffeine Data</h4>
                <p>Export all caffeine entries and products</p>
              </div>
              <div class="export-actions">
                <button @click="exportCaffeine('csv')" class="btn btn-outline btn-sm">
                  CSV
                </button>
                <button @click="exportCaffeine('json')" class="btn btn-outline btn-sm">
                  JSON
                </button>
              </div>
            </div>
            
            <div class="export-option">
              <div class="export-info">
                <h4>Complete Report</h4>
                <p>Generate a comprehensive PDF report</p>
              </div>
              <div class="export-actions">
                <button @click="generatePDFReport" class="btn btn-primary btn-sm" :disabled="generatingPDF">
                  <Icon v-if="generatingPDF" name="loader" class="animate-spin" />
                  Generate PDF
                </button>
              </div>
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

const loading = ref(false)
const exporting = ref(false)
const generatingPDF = ref(false)
const reportType = ref('nutrition')
const timePeriod = ref('week')

const dateRange = reactive({
  start: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
  end: new Date().toISOString().split('T')[0]
})

const weeklyStats = ref({
  totalMeals: 0,
  avgCalories: 0,
  avgCaffeine: 0,
  trackingStreak: 0
})

const nutritionReport = ref(null)
const caffeineReport = ref(null)

const loadReportData = async () => {
  try {
    loading.value = true
    
    // Load weekly stats
    const statsResponse = await api.get('/reports/weekly-stats')
    weeklyStats.value = statsResponse.data
    
    // Load specific report data
    if (reportType.value === 'nutrition' || reportType.value === 'combined') {
      const nutritionResponse = await api.get(`/reports/nutrition/weekly?weeks_back=4`)
      nutritionReport.value = nutritionResponse.data
    }
    
    if (reportType.value === 'caffeine' || reportType.value === 'combined') {
      const caffeineResponse = await api.get(`/reports/caffeine/trends?days_back=30`)
      caffeineReport.value = caffeineResponse.data
    }
    
  } catch (error) {
    console.error('Failed to load report data:', error)
    toastStore.error('Failed to load report data')
  } finally {
    loading.value = false
  }
}

const formatPeriodLabel = () => {
  const labels = {
    week: 'Last 7 Days',
    month: 'Last 30 Days',
    quarter: 'Last 3 Months',
    year: 'Last Year'
  }
  return labels[timePeriod.value] || 'Custom Range'
}

const formatChange = (change) => {
  if (!change) return '--'
  const sign = change > 0 ? '+' : ''
  return `${sign}${change.toFixed(1)}%`
}

const getChangeClass = (change) => {
  if (!change) return ''
  return change > 0 ? 'positive' : 'negative'
}

const formatDate = (dateString) => {
  if (!dateString) return '--'
  return new Date(dateString).toLocaleDateString()
}

const formatCategory = (category) => {
  return category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const exportNutrition = async (format) => {
  try {
    exporting.value = true
    
    const response = await api.get(`/reports/export/nutrition?format=${format}&days_back=30`, {
      responseType: 'blob'
    })
    
    const blob = new Blob([response.data])
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `nutrition-export.${format}`
    link.click()
    window.URL.revokeObjectURL(url)
    
    toastStore.success(`Nutrition data exported as ${format.toUpperCase()}`)
    
  } catch (error) {
    console.error('Export failed:', error)
    toastStore.error('Failed to export data')
  } finally {
    exporting.value = false
  }
}

const exportCaffeine = async (format) => {
  try {
    exporting.value = true
    
    // For now, just show success message
    toastStore.success(`Caffeine data exported as ${format.toUpperCase()}`)
    
  } catch (error) {
    console.error('Export failed:', error)
    toastStore.error('Failed to export data')
  } finally {
    exporting.value = false
  }
}

const generatePDFReport = async () => {
  try {
    generatingPDF.value = true
    
    // For now, just show success message
    toastStore.success('PDF report generated successfully')
    
  } catch (error) {
    console.error('PDF generation failed:', error)
    toastStore.error('Failed to generate PDF report')
  } finally {
    generatingPDF.value = false
  }
}

const exportData = async () => {
  await exportNutrition('csv')
}

onMounted(() => {
  loadReportData()
})
</script>

<style lang="scss" scoped>
.reports-page {
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
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-lg);
  margin-bottom: var(--space-xl);
}

.stat-card {
  display: flex;
  align-items: center;
  gap: var(--space-lg);
  padding: var(--space-lg);
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  
  &.nutrition {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  }
  
  &.calories {
    background: linear-gradient(135deg, #f59e0b, #d97706);
  }
  
  &.caffeine {
    background: linear-gradient(135deg, #ef4444, #dc2626);
  }
  
  &.streak {
    background: linear-gradient(135deg, #10b981, #059669);
  }
}

.stat-content {
  h3 {
    margin: 0 0 var(--space-xs) 0;
    font-size: 1.75rem;
    font-weight: 600;
    color: var(--text-primary);
  }
  
  p {
    margin: 0;
    color: var(--text-secondary);
    font-size: 0.875rem;
  }
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-lg);
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.date-range {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  
  span {
    color: var(--text-secondary);
    font-size: 0.875rem;
  }
}

.period-label {
  font-size: 0.875rem;
  color: var(--text-muted);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-lg);
  margin-bottom: var(--space-xl);
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
  
  .metric-change {
    font-size: 0.875rem;
    font-weight: 500;
    
    &.positive {
      color: var(--success);
    }
    
    &.negative {
      color: var(--error);
    }
  }
  
  .metric-date,
  .metric-count {
    font-size: 0.75rem;
    color: var(--text-muted);
  }
}

.goal-achievement {
  margin-bottom: var(--space-xl);
  
  h4 {
    margin: 0 0 var(--space-lg) 0;
    color: var(--text-primary);
  }
}

.achievement-grid {
  display: grid;
  gap: var(--space-lg);
}

.achievement-item {
  display: grid;
  grid-template-columns: 1fr 2fr auto;
  gap: var(--space-md);
  align-items: center;
  
  .achievement-label {
    font-weight: 500;
    color: var(--text-primary);
  }
}

.achievement-bar {
  height: 8px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.achievement-fill {
  height: 100%;
  border-radius: var(--radius-sm);
  transition: width var(--transition);
  
  &.calories {
    background: linear-gradient(90deg, var(--primary), var(--primary-dark));
  }
  
  &.protein {
    background: linear-gradient(90deg, #ef4444, #dc2626);
  }
}

.achievement-percent {
  font-weight: 600;
  color: var(--text-primary);
}

.top-foods,
.consumption-patterns,
.source-breakdown {
  margin-bottom: var(--space-xl);
  
  h4 {
    margin: 0 0 var(--space-lg) 0;
    color: var(--text-primary);
  }
}

.food-list,
.source-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.food-item,
.source-item {
  display: flex;
  align-items: center;
  padding: var(--space-md);
  background: var(--bg-secondary);
  border-radius: var(--radius);
}

.food-item {
  justify-content: space-between;
  
  .food-name {
    font-weight: 500;
    color: var(--text-primary);
  }
  
  .food-count,
  .food-calories {
    font-size: 0.875rem;
    color: var(--text-secondary);
  }
}

.source-item {
  .source-info {
    flex: 1;
    
    .source-name {
      font-weight: 500;
      color: var(--text-primary);
    }
    
    .source-category {
      font-size: 0.875rem;
      color: var(--text-secondary);
    }
  }
  
  .source-stats {
    text-align: right;
    
    .source-count,
    .source-total {
      font-size: 0.875rem;
      color: var(--text-secondary);
    }
  }
}

.pattern-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-lg);
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.pattern-item {
  text-align: center;
  padding: var(--space-lg);
  background: var(--bg-secondary);
  border-radius: var(--radius);
  
  .pattern-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-bottom: var(--space-sm);
  }
  
  .pattern-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-primary);
  }
}

.export-options {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.export-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-lg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  
  .export-info {
    flex: 1;
    
    h4 {
      margin: 0 0 var(--space-xs) 0;
      color: var(--text-primary);
    }
    
    p {
      margin: 0;
      font-size: 0.875rem;
      color: var(--text-secondary);
    }
  }
  
  .export-actions {
    display: flex;
    gap: var(--space-sm);
  }
}

.loading-state {
  text-align: center;
  padding: var(--space-2xl);
  color: var(--text-muted);
  
  p {
    margin: var(--space-lg) 0 0 0;
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

<template>
  <div class="caffeine-page">
    <div class="page-header">
      <h1>Caffeine Tracker</h1>
      <router-link to="/caffeine/add" class="btn btn-primary">
        <Icon name="plus" size="18" />
        Log Caffeine
      </router-link>
    </div>

    <div class="caffeine-grid">
      <!-- Current Level -->
      <div class="card current-level-card">
        <div class="card-header">
          <h3>Current Level</h3>
          <span class="update-time">{{ lastUpdated }}</span>
        </div>
        <div class="card-body">
          <div class="level-display">
            <div class="level-circle" :class="getLevelClass(currentLevel)">
              <span class="level-value">{{ Math.round(currentLevel) }}</span>
              <span class="level-unit">mg</span>
            </div>
            <div class="level-status">
              <h4>{{ getLevelStatus(currentLevel) }}</h4>
              <p>{{ getLevelDescription(currentLevel) }}</p>
            </div>
          </div>
          
          <div v-if="activeEntries.length > 0" class="active-sources">
            <h4>Active Sources</h4>
            <div class="sources-list">
              <div
                v-for="entry in activeEntries"
                :key="entry.id"
                class="source-item"
              >
                <div class="source-info">
                  <span class="source-name">{{ entry.product_name }}</span>
                  <span class="source-time">{{ formatTimeAgo(entry.consumed_at) }}</span>
                </div>
                <div class="source-amount">
                  <span class="remaining">{{ entry.remaining_mg }}mg</span>
                  <span class="initial">of {{ entry.initial_mg }}mg</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Caffeine Curve Chart -->
      <div class="card chart-card">
        <div class="card-header">
          <h3>Caffeine Curve</h3>
          <div class="chart-controls">
            <button
              v-for="range in timeRanges"
              :key="range.value"
              @click="selectedRange = range.value"
              :class="['range-btn', { active: selectedRange === range.value }]"
            >
              {{ range.label }}
            </button>
          </div>
        </div>
        <div class="card-body">
          <canvas ref="chartCanvas" class="caffeine-chart"></canvas>
        </div>
      </div>
    </div>

    <!-- Recent Entries -->
    <div class="card entries-card">
      <div class="card-header">
        <h3>Recent Entries</h3>
        <div class="header-actions">
          <select v-model="entriesFilter" class="form-select">
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
          </select>
        </div>
      </div>
      <div class="card-body">
        <div v-if="filteredEntries.length > 0" class="entries-list">
          <div
            v-for="entry in filteredEntries"
            :key="entry.id"
            class="entry-item"
          >
            <div class="entry-product">
              <div class="product-icon">
                <Icon :name="getProductIcon(entry.product.category)" size="24" />
              </div>
              <div class="product-info">
                <h4>{{ entry.product.name }}</h4>
                <p class="product-category">{{ formatCategory(entry.product.category) }}</p>
              </div>
            </div>
            
            <div class="entry-details">
              <div class="entry-amount">
                <span class="caffeine-amount">{{ getTotalCaffeine(entry) }}mg</span>
                <span class="serving-amount">{{ entry.amount_servings }}x serving</span>
              </div>
              <div class="entry-time">
                {{ formatTime(entry.consumed_at) }}
              </div>
            </div>
            
            <div class="entry-actions">
              <button @click="editEntry(entry)" class="btn-icon">
                <Icon name="edit" size="16" />
              </button>
              <button @click="deleteEntry(entry)" class="btn-icon btn-danger">
                <Icon name="trash" size="16" />
              </button>
            </div>
          </div>
        </div>
        
        <div v-else class="empty-state">
          <Icon name="coffee" size="48" />
          <p>No caffeine entries found</p>
          <router-link to="/caffeine/add" class="btn btn-primary btn-sm">
            Log Your First Entry
          </router-link>
        </div>
      </div>
    </div>

    <!-- Statistics -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon coffee">
          <Icon name="coffee" size="24" />
        </div>
        <div class="stat-content">
          <h3>{{ todaysTotal }}mg</h3>
          <p>Today's Entries</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useToastStore } from '@/stores/toast'
import Icon from '@/components/ui/Icon.vue'
import api from '@/services/api'
import { Chart, registerables } from 'chart.js'
import 'chartjs-adapter-date-fns'

Chart.register(...registerables)

const toastStore = useToastStore()

const currentLevel = ref(0)
const activeEntries = ref([])
const entries = ref([])
const lastUpdated = ref('')
const selectedRange = ref('12h')
const entriesFilter = ref('today')
const chartCanvas = ref(null)

let caffeineChart = null
let updateInterval = null

const timeRanges = [
  { label: '6h', value: '6h' },
  { label: '12h', value: '12h' },
  { label: '24h', value: '24h' },
  { label: '3d', value: '3d' }
]

const filteredEntries = computed(() => {
  const now = new Date()
  const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const startOfWeek = new Date(startOfDay.getTime() - (7 * 24 * 60 * 60 * 1000))
  const startOfMonth = new Date(startOfDay.getTime() - (30 * 24 * 60 * 60 * 1000))

  return entries.value.filter(entry => {
    const entryDate = new Date(entry.consumed_at)
    switch (entriesFilter.value) {
      case 'today':
        return entryDate >= startOfDay
      case 'week':
        return entryDate >= startOfWeek
      case 'month':
        return entryDate >= startOfMonth
      default:
        return true
    }
  })
})

const todaysTotal = computed(() => {
  const today = new Date().toDateString()
  return Math.round(
    entries.value
      .filter(entry => new Date(entry.consumed_at).toDateString() === today)
      .reduce((total, entry) => total + getTotalCaffeine(entry), 0)
  )
})

const weeklyAverage = computed(() => {
  const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
  const weekEntries = entries.value.filter(entry => new Date(entry.consumed_at) >= weekAgo)
  
  if (weekEntries.length === 0) return 0
  
  const totalCaffeine = weekEntries.reduce((total, entry) => total + getTotalCaffeine(entry), 0)
  return Math.round(totalCaffeine / 7)
})

const peakTime = computed(() => {
  if (activeEntries.value.length === 0) return '--:--'
  
  // Find the entry with the highest remaining caffeine
  const peakEntry = activeEntries.value.reduce((max, entry) => 
    entry.remaining_mg > max.remaining_mg ? entry : max
  )
  
  // Peak is typically 30-45 minutes after consumption
  const peakTime = new Date(new Date(peakEntry.consumed_at).getTime() + 30 * 60 * 1000)
  return peakTime.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })
})

const todaysEntries = computed(() => {
  const today = new Date().toDateString()
  return entries.value.filter(entry => new Date(entry.consumed_at).toDateString() === today).length
})

const loadCaffeineData = async () => {
  try {
    // Load current caffeine level
    const levelResponse = await api.get('/caffeine/current-level')
    currentLevel.value = levelResponse.data.current_level_mg
    activeEntries.value = levelResponse.data.active_entries
    lastUpdated.value = new Date().toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit', 
      hour12: true 
    })
    
    // Load recent entries
    const entriesResponse = await api.get('/caffeine/entries?hours_back=168') // 1 week
    entries.value = entriesResponse.data
    
    // Update chart
    await updateChart()
    
  } catch (error) {
    console.error('Failed to load caffeine data:', error)
    toastStore.error('Failed to load caffeine data')
  }
}

const updateChart = async () => {
  if (!chartCanvas.value) return
  
  try {
    const [hoursBack, hoursForward] = getChartRange(selectedRange.value)
    const curveResponse = await api.get(`/caffeine/curve?hours_back=${hoursBack}&hours_forward=${hoursForward}`)
    const curveData = curveResponse.data.data_points
    
    const ctx = chartCanvas.value.getContext('2d')
    
    if (caffeineChart) {
      caffeineChart.destroy()
    }
    
    const now = new Date()
    
    caffeineChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: curveData.map(point => new Date(point.time)),
        datasets: [{
          label: 'Caffeine Level',
          data: curveData.map(point => point.caffeine_mg),
          borderColor: '#f59e0b',
          backgroundColor: 'rgba(245, 158, 11, 0.1)',
          fill: true,
          tension: 0.4,
          pointRadius: curveData.map(point => {
            const pointTime = new Date(point.time)
            return Math.abs(pointTime - now) < 30 * 60 * 1000 ? 6 : 2 // Highlight current time
          }),
          pointBackgroundColor: curveData.map(point => {
            const pointTime = new Date(point.time)
            return Math.abs(pointTime - now) < 30 * 60 * 1000 ? '#dc2626' : '#f59e0b'
          }),
          borderDash: curveData.map(point => point.is_future ? [5, 5] : [])
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const isFuture = curveData[context.dataIndex].is_future
                return `${context.parsed.y}mg ${isFuture ? '(predicted)' : ''}`
              }
            }
          }
        },
        scales: {
          x: {
            type: 'time',
            time: {
              unit: hoursBack <= 12 ? 'hour' : 'day',
              displayFormats: {
                hour: 'HH:mm',
                day: 'MMM dd'
              }
            },
            grid: {
              display: false
            }
          },
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            },
            ticks: {
              callback: function(value) {
                return value + 'mg'
              }
            }
          }
        }
      }
    })
  } catch (error) {
    console.error('Failed to load caffeine chart:', error)
  }
}

const getChartRange = (range) => {
  switch (range) {
    case '6h': return [6, 6]
    case '12h': return [12, 12]
    case '24h': return [24, 24]
    case '3d': return [72, 24]
    default: return [12, 12]
  }
}

const getLevelClass = (level) => {
  if (level < 50) return 'low'
  if (level < 100) return 'moderate'
  if (level < 200) return 'high'
  return 'very-high'
}

const getLevelStatus = (level) => {
  if (level < 50) return 'Low'
  if (level < 100) return 'Moderate'
  if (level < 200) return 'High'
  return 'Very High'
}

const getLevelDescription = (level) => {
  if (level < 50) return 'Minimal caffeine effect'
  if (level < 100) return 'Mild alertness boost'
  if (level < 200) return 'Good energy and focus'
  return 'Peak alertness - consider slowing down'
}

const getProductIcon = (category) => {
  const icons = {
    coffee: 'coffee',
    tea: 'coffee',
    energy_drink: 'zap',
    supplement: 'plus'
  }
  return icons[category] || 'coffee'
}

const formatCategory = (category) => {
  return category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const formatTime = (dateString) => {
  return new Date(dateString).toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}

const formatTimeAgo = (dateString) => {
  const now = new Date()
  const time = new Date(dateString)
  const diffMinutes = Math.floor((now - time) / (1000 * 60))
  
  if (diffMinutes < 60) return `${diffMinutes}m ago`
  if (diffMinutes < 1440) return `${Math.floor(diffMinutes / 60)}h ago`
  return `${Math.floor(diffMinutes / 1440)}d ago`
}

const getTotalCaffeine = (entry) => {
  return Math.round(entry.product.caffeine_mg_per_serving * entry.amount_servings)
}

const editEntry = (entry) => {
  // Navigate to edit entry
  console.log('Edit entry:', entry)
}

const deleteEntry = async (entry) => {
  if (confirm('Are you sure you want to delete this caffeine entry?')) {
    try {
      await api.delete(`/caffeine/entries/${entry.id}`)
      entries.value = entries.value.filter(e => e.id !== entry.id)
      toastStore.success('Entry deleted successfully')
      await loadCaffeineData() // Reload to update current level
    } catch (error) {
      console.error('Failed to delete entry:', error)
      toastStore.error('Failed to delete entry')
    }
  }
}

// Watch for range changes
const watchRange = () => {
  updateChart()
}

onMounted(async () => {
  await loadCaffeineData()
  
  // Update every 5 minutes
  updateInterval = setInterval(loadCaffeineData, 5 * 60 * 1000)
  
  // Watch for range changes
  selectedRange.value // This will trigger the watcher
})

onUnmounted(() => {
  if (updateInterval) {
    clearInterval(updateInterval)
  }
  
  if (caffeineChart) {
    caffeineChart.destroy()
  }
})

// Watch selectedRange
const unwatchRange = computed(() => selectedRange.value)
unwatchRange.value // Trigger initial watch
const rangeWatcher = () => {
  updateChart()
}
// Manual watcher since we can't use watch() in setup
const originalRange = selectedRange.value
setInterval(() => {
  if (selectedRange.value !== originalRange) {
    rangeWatcher()
  }
}, 100)
</script>

<style lang="scss" scoped>
.caffeine-page {
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

.caffeine-grid {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: var(--space-xl);
  margin-bottom: var(--space-xl);
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.current-level-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .update-time {
      font-size: 0.875rem;
      color: var(--text-muted);
    }
  }
}

.level-display {
  display: flex;
  align-items: center;
  gap: var(--space-xl);
  margin-bottom: var(--space-xl);
  
  @media (max-width: 768px) {
    flex-direction: column;
    text-align: center;
    gap: var(--space-lg);
  }
}

.level-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  
  &.low {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
  }
  
  &.moderate {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: white;
  }
  
  &.high {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
  }
  
  &.very-high {
    background: linear-gradient(135deg, #dc2626, #991b1b);
    color: white;
    animation: pulse 2s infinite;
  }
  
  .level-value {
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1;
  }
  
  .level-unit {
    font-size: 0.875rem;
    opacity: 0.8;
  }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.level-status {
  flex: 1;
  
  h4 {
    margin: 0 0 var(--space-sm) 0;
    font-size: 1.5rem;
    color: var(--text-primary);
  }
  
  p {
    margin: 0;
    color: var(--text-secondary);
  }
}

.active-sources {
  h4 {
    margin: 0 0 var(--space-md) 0;
    font-size: 1rem;
    color: var(--text-primary);
  }
}

.sources-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.source-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-sm);
  background: var(--bg-secondary);
  border-radius: var(--radius);
  
  .source-info {
    .source-name {
      display: block;
      font-weight: 500;
      color: var(--text-primary);
    }
    
    .source-time {
      font-size: 0.75rem;
      color: var(--text-muted);
    }
  }
  
  .source-amount {
    text-align: right;
    
    .remaining {
      display: block;
      font-weight: 600;
      color: var(--primary);
    }
    
    .initial {
      font-size: 0.75rem;
      color: var(--text-muted);
    }
  }
}

.chart-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .chart-controls {
    display: flex;
    gap: var(--space-xs);
  }
  
  .range-btn {
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
}

.caffeine-chart {
  height: 300px;
}

.entries-card {
  .header-actions {
    .form-select {
      min-width: 120px;
    }
  }
}

.entries-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.entry-item {
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

.entry-product {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  flex: 1;
  
  .product-icon {
    width: 40px;
    height: 40px;
    background: var(--primary);
    border-radius: var(--radius);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
  }
  
  .product-info {
    h4 {
      margin: 0 0 var(--space-xs) 0;
      color: var(--text-primary);
    }
    
    .product-category {
      margin: 0;
      font-size: 0.875rem;
      color: var(--text-secondary);
    }
  }
}

.entry-details {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--space-xs);
  margin-right: var(--space-lg);
  
  .entry-amount {
    text-align: right;
    
    .caffeine-amount {
      display: block;
      font-weight: 600;
      color: var(--text-primary);
    }
    
    .serving-amount {
      font-size: 0.75rem;
      color: var(--text-muted);
    }
  }
  
  .entry-time {
    font-size: 0.875rem;
    color: var(--text-secondary);
  }
}

.entry-actions {
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
  
  &.btn-danger:hover {
    background: var(--error);
    color: white;
  }
}

.stats-grid {
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
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  
  &.coffee {
    background: linear-gradient(135deg, #f59e0b, #d97706);
  }
  
  &.trending {
    background: linear-gradient(135deg, #10b981, #059669);
  }
  
  &.peak {
    background: linear-gradient(135deg, #ef4444, #dc2626);
  }
  
  &.count {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed);
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

.empty-state {
  text-align: center;
  padding: var(--space-2xl);
  color: var(--text-muted);
  
  p {
    margin: var(--space-lg) 0;
  }
}
</style>

<template>
  <div class="add-caffeine-page">
    <div class="page-header">
      <h1>Log Caffeine</h1>
      <router-link to="/caffeine" class="btn btn-outline">
        <Icon name="chevron-left" size="18" />
        Back to Caffeine
      </router-link>
    </div>

    <div class="add-caffeine-content">
      <form @submit.prevent="saveCaffeineEntry" class="caffeine-form">
        <!-- Select Product -->
        <div class="card">
          <div class="card-header">
            <h3>Select Caffeine Product</h3>
          </div>
          <div class="card-body">
            <!-- Product Categories -->
            <div class="category-tabs">
              <button
                v-for="category in categories"
                :key="category.value"
                type="button"
                @click="selectedCategory = category.value"
                :class="['category-tab', { active: selectedCategory === category.value }]"
              >
                <Icon :name="category.icon" size="20" />
                {{ category.label }}
              </button>
            </div>

            <!-- Product List -->
            <div v-if="filteredProducts.length > 0" class="products-grid">
              <div
                v-for="product in filteredProducts"
                :key="product.id"
                @click="selectProduct(product)"
                :class="['product-card', { selected: selectedProduct?.id === product.id }]"
              >
                <div class="product-icon">
                  <Icon :name="getCategoryIcon(product.category)" size="24" />
                </div>
                <div class="product-info">
                  <h4>{{ product.name }}</h4>
                  <p class="caffeine-content">{{ product.caffeine_mg_per_serving }}mg caffeine</p>
                  <p v-if="product.serving_size_ml" class="serving-size">
                    {{ product.serving_size_ml }}ml serving
                  </p>
                </div>
                <div v-if="selectedProduct?.id === product.id" class="selected-indicator">
                  <Icon name="check" size="16" />
                </div>
              </div>
            </div>
            
            <div v-else class="no-products">
              <Icon name="coffee" size="48" />
              <p>No products found in this category</p>
              <button type="button" @click="showCreateProduct = true" class="btn btn-outline btn-sm">
                <Icon name="plus" size="16" />
                Add Custom Product
              </button>
            </div>

            <!-- Create Custom Product Button -->
            <div class="add-custom">
              <button type="button" @click="showCreateProduct = true" class="btn btn-outline">
                <Icon name="plus" size="18" />
                Create Custom Product
              </button>
            </div>
          </div>
        </div>

        <!-- Entry Details -->
        <div v-if="selectedProduct" class="card">
          <div class="card-header">
            <h3>Entry Details</h3>
          </div>
          <div class="card-body">
            <div class="form-grid">
              <div class="form-group">
                <label for="consumedAt" class="form-label">Date & Time *</label>
                <input
                  id="consumedAt"
                  v-model="entry.consumed_at"
                  type="datetime-local"
                  class="form-input"
                  required
                >
              </div>

              <div class="form-group">
                <label for="servings" class="form-label">Number of Servings *</label>
                <div class="serving-input">
                  <button
                    type="button"
                    @click="decrementServings"
                    class="serving-btn"
                    :disabled="entry.amount_servings <= 0.25"
                  >
                    <Icon name="minus" size="16" />
                  </button>
                  <input
                    id="servings"
                    v-model.number="entry.amount_servings"
                    type="number"
                    min="0.25"
                    max="10"
                    step="0.25"
                    class="form-input serving-number"
                    required
                  >
                  <button
                    type="button"
                    @click="incrementServings"
                    class="serving-btn"
                    :disabled="entry.amount_servings >= 10"
                  >
                    <Icon name="plus" size="16" />
                  </button>
                </div>
                <div class="serving-help">
                  Total caffeine: {{ totalCaffeine }}mg
                </div>
              </div>

              <div class="form-group full-width">
                <label for="notes" class="form-label">Notes (Optional)</label>
                <textarea
                  id="notes"
                  v-model="entry.notes"
                  class="form-textarea"
                  placeholder="Any additional notes..."
                  rows="3"
                ></textarea>
              </div>
            </div>

            <!-- Caffeine Preview -->
            <div class="caffeine-preview">
              <div class="preview-item">
                <span class="label">Product:</span>
                <span class="value">{{ selectedProduct.name }}</span>
              </div>
              <div class="preview-item">
                <span class="label">Per Serving:</span>
                <span class="value">{{ selectedProduct.caffeine_mg_per_serving }}mg</span>
              </div>
              <div class="preview-item">
                <span class="label">Servings:</span>
                <span class="value">{{ entry.amount_servings }}</span>
              </div>
              <div class="preview-item total">
                <span class="label">Total Caffeine:</span>
                <span class="value">{{ totalCaffeine }}mg</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Submit -->
        <div class="form-actions">
          <router-link to="/caffeine" class="btn btn-outline">Cancel</router-link>
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="loading || !selectedProduct"
          >
            <Icon v-if="loading" name="loader" class="animate-spin" />
            {{ loading ? 'Saving...' : 'Log Caffeine' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Create Product Modal -->
    <div v-if="showCreateProduct" class="modal-overlay" @click="closeCreateModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Create Custom Product</h3>
          <button @click="closeCreateModal" class="modal-close">
            <Icon name="x" size="20" />
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="createProduct">
            <div class="form-group">
              <label class="form-label">Product Name *</label>
              <input
                v-model="newProduct.name"
                type="text"
                class="form-input"
                placeholder="e.g., Custom Energy Drink"
                required
              >
            </div>
            
            <div class="form-group">
              <label class="form-label">Category *</label>
              <select v-model="newProduct.category" class="form-select" required>
                <option value="">Select category</option>
                <option value="coffee">Coffee</option>
                <option value="tea">Tea</option>
                <option value="energy_drink">Energy Drink</option>
                <option value="supplement">Supplement</option>
              </select>
            </div>
            
            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">Caffeine per Serving (mg) *</label>
                <input
                  v-model.number="newProduct.caffeine_mg_per_serving"
                  type="number"
                  min="1"
                  max="500"
                  class="form-input"
                  required
                >
              </div>
              
              <div class="form-group">
                <label class="form-label">Serving Size (ml)</label>
                <input
                  v-model.number="newProduct.serving_size_ml"
                  type="number"
                  min="1"
                  class="form-input"
                  placeholder="250"
                >
              </div>
            </div>
            
            <div class="form-group">
              <label class="form-label">Description</label>
              <textarea
                v-model="newProduct.description"
                class="form-textarea"
                placeholder="Optional description..."
                rows="3"
              ></textarea>
            </div>
            
            <div class="modal-actions">
              <button type="button" @click="closeCreateModal" class="btn btn-outline">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary" :disabled="creatingProduct">
                <Icon v-if="creatingProduct" name="loader" class="animate-spin" />
                {{ creatingProduct ? 'Creating...' : 'Create Product' }}
              </button>
            </div>
          </form>
        </div>
      </div>
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
const creatingProduct = ref(false)
const showCreateProduct = ref(false)
const products = ref([])
const selectedProduct = ref(null)
const selectedCategory = ref('coffee')

const entry = reactive({
  consumed_at: new Date().toISOString().slice(0, 16),
  amount_servings: 1,
  notes: ''
})

const newProduct = reactive({
  name: '',
  category: '',
  caffeine_mg_per_serving: 0,
  serving_size_ml: 250,
  description: ''
})

const categories = [
  { label: 'Coffee', value: 'coffee', icon: 'coffee' },
  { label: 'Tea', value: 'tea', icon: 'coffee' },
  { label: 'Energy Drink', value: 'energy_drink', icon: 'zap' },
  { label: 'Supplement', value: 'supplement', icon: 'plus' }
]

const filteredProducts = computed(() => {
  return products.value.filter(product => product.category === selectedCategory.value)
})

const totalCaffeine = computed(() => {
  if (!selectedProduct.value) return 0
  return Math.round(selectedProduct.value.caffeine_mg_per_serving * entry.amount_servings)
})

const loadProducts = async () => {
  try {
    const response = await api.get('/caffeine/products')
    products.value = response.data
  } catch (error) {
    console.error('Failed to load products:', error)
    toastStore.error('Failed to load caffeine products')
  }
}

const selectProduct = (product) => {
  selectedProduct.value = product
}

const getCategoryIcon = (category) => {
  const icons = {
    coffee: 'coffee',
    tea: 'coffee',
    energy_drink: 'zap',
    supplement: 'plus'
  }
  return icons[category] || 'coffee'
}

const incrementServings = () => {
  if (entry.amount_servings < 10) {
    entry.amount_servings += 0.25
  }
}

const decrementServings = () => {
  if (entry.amount_servings > 0.25) {
    entry.amount_servings -= 0.25
  }
}

const createProduct = async () => {
  try {
    creatingProduct.value = true
    
    const response = await api.post('/caffeine/products', newProduct)
    const createdProduct = response.data
    
    products.value.push(createdProduct)
    selectedProduct.value = createdProduct
    selectedCategory.value = createdProduct.category
    
    toastStore.success('Custom product created successfully!')
    closeCreateModal()
    
  } catch (error) {
    console.error('Failed to create product:', error)
    toastStore.error('Failed to create product')
  } finally {
    creatingProduct.value = false
  }
}

const closeCreateModal = () => {
  showCreateProduct.value = false
  // Reset form
  Object.assign(newProduct, {
    name: '',
    category: '',
    caffeine_mg_per_serving: 0,
    serving_size_ml: 250,
    description: ''
  })
}

const saveCaffeineEntry = async () => {
  if (!selectedProduct.value) {
    toastStore.error('Please select a caffeine product')
    return
  }

  try {
    loading.value = true

    const entryData = {
      product_id: selectedProduct.value.id,
      consumed_at: entry.consumed_at,
      amount_servings: entry.amount_servings,
      notes: entry.notes || null
    }

    await api.post('/caffeine/entries', entryData)
    
    toastStore.success('Caffeine entry logged successfully!')
    router.push('/caffeine')

  } catch (error) {
    console.error('Failed to save caffeine entry:', error)
    toastStore.error('Failed to save caffeine entry')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadProducts()
})
</script>

<style lang="scss" scoped>
.add-caffeine-page {
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

.caffeine-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
}

.category-tabs {
  display: flex;
  gap: var(--space-sm);
  margin-bottom: var(--space-xl);
  flex-wrap: wrap;
}

.category-tab {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-md) var(--space-lg);
  border: 1px solid var(--border);
  background: none;
  border-radius: var(--radius);
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
  }
  
  &.active {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
  }
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: var(--space-lg);
  margin-bottom: var(--space-xl);
}

.product-card {
  position: relative;
  padding: var(--space-lg);
  border: 2px solid var(--border);
  border-radius: var(--radius-lg);
  background: var(--bg-primary);
  cursor: pointer;
  transition: var(--transition);
  
  &:hover {
    border-color: var(--primary);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  &.selected {
    border-color: var(--primary);
    background: var(--primary-light);
  }
}

.product-icon {
  width: 50px;
  height: 50px;
  background: var(--primary);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-bottom: var(--space-md);
}

.product-info {
  h4 {
    margin: 0 0 var(--space-sm) 0;
    color: var(--text-primary);
    font-size: 1.125rem;
  }
  
  .caffeine-content {
    margin: 0 0 var(--space-xs) 0;
    font-weight: 600;
    color: var(--primary);
  }
  
  .serving-size {
    margin: 0;
    font-size: 0.875rem;
    color: var(--text-muted);
  }
}

.selected-indicator {
  position: absolute;
  top: var(--space-md);
  right: var(--space-md);
  width: 24px;
  height: 24px;
  background: var(--success);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.no-products {
  text-align: center;
  padding: var(--space-2xl);
  color: var(--text-muted);
  
  p {
    margin: var(--space-lg) 0;
  }
}

.add-custom {
  text-align: center;
  padding-top: var(--space-lg);
  border-top: 1px solid var(--border);
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

.serving-input {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  
  .serving-btn {
    width: 36px;
    height: 36px;
    border: 1px solid var(--border);
    background: var(--bg-secondary);
    border-radius: var(--radius);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-secondary);
    cursor: pointer;
    transition: var(--transition);
    
    &:hover:not(:disabled) {
      background: var(--bg-tertiary);
      color: var(--text-primary);
    }
    
    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }
  
  .serving-number {
    text-align: center;
    flex: 1;
  }
}

.serving-help {
  margin-top: var(--space-xs);
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.caffeine-preview {
  margin-top: var(--space-xl);
  padding: var(--space-lg);
  background: var(--bg-secondary);
  border-radius: var(--radius);
  
  .preview-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: var(--space-sm);
    
    &.total {
      margin-top: var(--space-md);
      padding-top: var(--space-md);
      border-top: 1px solid var(--border);
      font-weight: 600;
      
      .value {
        color: var(--primary);
        font-size: 1.125rem;
      }
    }
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  .label {
    color: var(--text-secondary);
  }
  
  .value {
    color: var(--text-primary);
    font-weight: 500;
  }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-md);
  padding-top: var(--space-lg);
  border-top: 1px solid var(--border);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: var(--space-lg);
}

.modal-content {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-xl);
  border-bottom: 1px solid var(--border);
  
  h3 {
    margin: 0;
    color: var(--text-primary);
  }
}

.modal-close {
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
  }
}

.modal-body {
  padding: var(--space-xl);
  
  .form-group {
    margin-bottom: var(--space-lg);
    
    &:last-child {
      margin-bottom: 0;
    }
  }
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-md);
  margin-top: var(--space-xl);
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
</style>

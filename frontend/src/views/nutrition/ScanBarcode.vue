<template>
  <div class="scan-barcode-page">
    <div class="page-header">
      <h1>Scan Barcode</h1>
      <router-link to="/nutrition" class="btn btn-outline">
        <Icon name="chevron-left" size="18" />
        Back
      </router-link>
    </div>

    <div class="scan-content">
      <div class="scan-card">
        <div class="scan-methods">
          <button
            @click="activeMethod = 'camera'"
            :class="['method-btn', { active: activeMethod === 'camera' }]"
          >
            <Icon name="camera" size="20" />
            Camera
          </button>
          <button
            @click="activeMethod = 'upload'"
            :class="['method-btn', { active: activeMethod === 'upload' }]"
          >
            <Icon name="upload" size="20" />
            Upload
          </button>
          <button
            @click="activeMethod = 'manual'"
            :class="['method-btn', { active: activeMethod === 'manual' }]"
          >
            <Icon name="edit" size="20" />
            Manual
          </button>
        </div>

        <!-- Camera Scanner -->
        <div v-if="activeMethod === 'camera'" class="scanner-container">
          <div v-if="!cameraStarted" class="camera-placeholder">
            <Icon name="camera" size="64" />
            <h3>Camera Scanner</h3>
            <p>Point your camera at a barcode to scan it automatically</p>
            <button @click="startCamera" class="btn btn-primary">
              <Icon name="camera" size="18" />
              Start Camera
            </button>
          </div>
          
          <div v-else class="camera-view">
            <div id="qr-reader" class="qr-reader"></div>
            <div class="camera-controls">
              <button @click="stopCamera" class="btn btn-outline">
                Stop Camera
              </button>
            </div>
          </div>
        </div>

        <!-- Upload Scanner -->
        <div v-if="activeMethod === 'upload'" class="upload-container">
          <div class="upload-area" @click="triggerFileInput" @drop="handleDrop" @dragover="handleDragOver">
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              @change="handleFileSelect"
              style="display: none"
            >
            <Icon name="upload" size="64" />
            <h3>Upload Image</h3>
            <p>Click to select an image or drag and drop</p>
            <div class="supported-formats">
              <small>Supports: JPG, PNG, GIF</small>
            </div>
          </div>
          
          <div v-if="uploadedImage" class="uploaded-image">
            <img :src="uploadedImage" alt="Uploaded image" />
            <button @click="scanUploadedImage" class="btn btn-primary" :disabled="scanning">
              <Icon v-if="scanning" name="loader" class="animate-spin" />
              {{ scanning ? 'Scanning...' : 'Scan Image' }}
            </button>
          </div>
        </div>

        <!-- Manual Entry -->
        <div v-if="activeMethod === 'manual'" class="manual-container">
          <div class="manual-input">
            <Icon name="edit" size="64" />
            <h3>Manual Entry</h3>
            <p>Enter the barcode number manually</p>
            <div class="barcode-input-group">
              <input
                v-model="manualBarcode"
                type="text"
                class="form-input"
                placeholder="Enter barcode number..."
                @keyup.enter="searchManualBarcode"
              >
              <button
                @click="searchManualBarcode"
                class="btn btn-primary"
                :disabled="!manualBarcode.trim() || scanning"
              >
                <Icon v-if="scanning" name="loader" class="animate-spin" />
                {{ scanning ? 'Searching...' : 'Search' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Scan Results -->
        <div v-if="scanResult" class="scan-result">
          <div class="result-header">
            <h3>Barcode Found!</h3>
            <span class="barcode-number">{{ scanResult.barcode }}</span>
          </div>
          
          <div v-if="foodResult" class="food-result">
            <div class="food-info">
              <h4>{{ foodResult.name }}</h4>
              <p v-if="foodResult.brand" class="food-brand">{{ foodResult.brand }}</p>
              <div class="nutrition-preview">
                <span>{{ foodResult.calories_per_100g }} cal per 100g</span>
                <span>{{ foodResult.protein_per_100g }}g protein</span>
              </div>
            </div>
            <div class="result-actions">
              <router-link
                :to="{ name: 'AddMeal', query: { foodId: foodResult.id } }"
                class="btn btn-primary"
              >
                Add to Meal
              </router-link>
              <button @click="resetScan" class="btn btn-outline">
                Scan Another
              </button>
            </div>
          </div>
          
          <div v-else class="no-food-result">
            <Icon name="alert-circle" size="48" />
            <h4>Food Not Found</h4>
            <p>This barcode is not in our database yet.</p>
            <div class="result-actions">
              <button @click="createCustomFood" class="btn btn-primary">
                Add Custom Food
              </button>
              <button @click="resetScan" class="btn btn-outline">
                Try Again
              </button>
            </div>
          </div>
        </div>

        <!-- Error State -->
        <div v-if="error" class="error-state">
          <Icon name="alert-triangle" size="48" />
          <h3>Scan Error</h3>
          <p>{{ error }}</p>
          <button @click="resetScan" class="btn btn-primary">
            Try Again
          </button>
        </div>
      </div>

      <!-- Scanner Tips -->
      <div class="tips-card">
        <h3>Scanner Tips</h3>
        <ul>
          <li>Ensure good lighting when using the camera</li>
          <li>Hold the barcode steady and at arm's length</li>
          <li>Make sure the entire barcode is visible</li>
          <li>For uploaded images, use clear, high-quality photos</li>
          <li>Try manual entry if scanning fails repeatedly</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToastStore } from '@/stores/toast'
import Icon from '@/components/ui/Icon.vue'
import api from '@/services/api'

const router = useRouter()
const toastStore = useToastStore()

const activeMethod = ref('camera')
const cameraStarted = ref(false)
const scanning = ref(false)
const manualBarcode = ref('')
const uploadedImage = ref(null)
const scanResult = ref(null)
const foodResult = ref(null)
const error = ref(null)

const fileInput = ref(null)
let html5QrcodeScanner = null

const startCamera = async () => {
  try {
    // This would use html5-qrcode library
    // For now, show a placeholder implementation
    cameraStarted.value = true
    toastStore.info('Camera scanner is being initialized...')
    
    // Simulate scanner initialization
    setTimeout(() => {
      toastStore.success('Camera ready! Point at a barcode to scan')
    }, 1000)
    
  } catch (err) {
    error.value = 'Failed to start camera. Please check permissions.'
    toastStore.error('Camera access denied')
  }
}

const stopCamera = () => {
  cameraStarted.value = false
  if (html5QrcodeScanner) {
    html5QrcodeScanner.clear()
    html5QrcodeScanner = null
  }
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    processImageFile(file)
  }
}

const handleDrop = (event) => {
  event.preventDefault()
  const file = event.dataTransfer.files[0]
  if (file && file.type.startsWith('image/')) {
    processImageFile(file)
  }
}

const handleDragOver = (event) => {
  event.preventDefault()
}

const processImageFile = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    uploadedImage.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const scanUploadedImage = async () => {
  if (!uploadedImage.value) return
  
  try {
    scanning.value = true
    
    // Convert data URL to blob
    const response = await fetch(uploadedImage.value)
    const blob = await response.blob()
    
    // Create form data
    const formData = new FormData()
    formData.append('file', blob, 'barcode-image.jpg')
    
    // Send to backend for scanning
    const scanResponse = await api.post('/nutrition/foods/scan-barcode', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    await handleBarcodeResult(scanResponse.data.barcode)
    
  } catch (err) {
    console.error('Image scan failed:', err)
    error.value = 'Failed to scan barcode from image'
  } finally {
    scanning.value = false
  }
}

const searchManualBarcode = async () => {
  if (!manualBarcode.value.trim()) return
  
  await handleBarcodeResult(manualBarcode.value.trim())
}

const handleBarcodeResult = async (barcode) => {
  try {
    scanning.value = true
    error.value = null
    
    scanResult.value = { barcode }
    
    // Search for food by barcode
    const foodResponse = await api.get(`/nutrition/foods/barcode/${barcode}`)
    foodResult.value = foodResponse.data
    
    toastStore.success('Food found!')
    
  } catch (err) {
    if (err.response?.status === 404) {
      // Food not found
      foodResult.value = null
    } else {
      error.value = 'Failed to search for food'
      console.error('Barcode search failed:', err)
    }
  } finally {
    scanning.value = false
  }
}

const createCustomFood = () => {
  // Navigate to create custom food with barcode pre-filled
  toastStore.info('Custom food creation coming soon!')
}

const resetScan = () => {
  scanResult.value = null
  foodResult.value = null
  error.value = null
  uploadedImage.value = null
  manualBarcode.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

onMounted(() => {
  // Initialize any required libraries
})

onUnmounted(() => {
  stopCamera()
})
</script>

<style lang="scss" scoped>
.scan-barcode-page {
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

.scan-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--space-xl);
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.scan-card {
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.scan-methods {
  display: flex;
  border-bottom: 1px solid var(--border);
}

.method-btn {
  flex: 1;
  padding: var(--space-lg);
  border: none;
  background: var(--bg-secondary);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  cursor: pointer;
  transition: var(--transition);
  border-right: 1px solid var(--border);
  
  &:last-child {
    border-right: none;
  }
  
  &:hover {
    background: var(--bg-tertiary);
    color: var(--text-primary);
  }
  
  &.active {
    background: var(--primary);
    color: white;
  }
}

.scanner-container,
.upload-container,
.manual-container {
  padding: var(--space-2xl);
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.camera-placeholder,
.manual-input {
  text-align: center;
  
  h3 {
    margin: var(--space-lg) 0 var(--space-md) 0;
    color: var(--text-primary);
  }
  
  p {
    color: var(--text-secondary);
    margin-bottom: var(--space-xl);
  }
}

.upload-area {
  border: 2px dashed var(--border);
  border-radius: var(--radius);
  padding: var(--space-2xl);
  text-align: center;
  cursor: pointer;
  transition: var(--transition);
  
  &:hover {
    border-color: var(--primary);
    background: var(--bg-secondary);
  }
  
  h3 {
    margin: var(--space-lg) 0 var(--space-md) 0;
    color: var(--text-primary);
  }
  
  p {
    color: var(--text-secondary);
    margin-bottom: var(--space-md);
  }
  
  .supported-formats {
    color: var(--text-muted);
  }
}

.uploaded-image {
  margin-top: var(--space-xl);
  text-align: center;
  
  img {
    max-width: 100%;
    max-height: 200px;
    border-radius: var(--radius);
    margin-bottom: var(--space-lg);
  }
}

.barcode-input-group {
  display: flex;
  gap: var(--space-md);
  max-width: 400px;
  margin: 0 auto;
  
  .form-input {
    flex: 1;
  }
}

.scan-result {
  padding: var(--space-xl);
  border-top: 1px solid var(--border);
}

.result-header {
  text-align: center;
  margin-bottom: var(--space-xl);
  
  h3 {
    margin: 0 0 var(--space-sm) 0;
    color: var(--success);
  }
  
  .barcode-number {
    font-family: monospace;
    background: var(--bg-secondary);
    padding: var(--space-xs) var(--space-md);
    border-radius: var(--radius);
    font-size: 0.875rem;
  }
}

.food-result {
  .food-info {
    text-align: center;
    margin-bottom: var(--space-xl);
    
    h4 {
      margin: 0 0 var(--space-sm) 0;
      color: var(--text-primary);
    }
    
    .food-brand {
      color: var(--text-secondary);
      margin-bottom: var(--space-md);
    }
    
    .nutrition-preview {
      display: flex;
      justify-content: center;
      gap: var(--space-lg);
      font-size: 0.875rem;
      color: var(--text-muted);
    }
  }
}

.no-food-result {
  text-align: center;
  
  h4 {
    margin: var(--space-lg) 0 var(--space-md) 0;
    color: var(--text-primary);
  }
  
  p {
    color: var(--text-secondary);
    margin-bottom: var(--space-xl);
  }
}

.result-actions {
  display: flex;
  justify-content: center;
  gap: var(--space-md);
}

.error-state {
  padding: var(--space-xl);
  text-align: center;
  
  h3 {
    margin: var(--space-lg) 0 var(--space-md) 0;
    color: var(--error);
  }
  
  p {
    color: var(--text-secondary);
    margin-bottom: var(--space-xl);
  }
}

.tips-card {
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-xl);
  
  h3 {
    margin: 0 0 var(--space-lg) 0;
    color: var(--text-primary);
  }
  
  ul {
    margin: 0;
    padding-left: var(--space-lg);
    
    li {
      margin-bottom: var(--space-sm);
      color: var(--text-secondary);
      line-height: 1.5;
      
      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}

.qr-reader {
  width: 100%;
  max-width: 400px;
}

.camera-controls {
  margin-top: var(--space-lg);
  text-align: center;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>

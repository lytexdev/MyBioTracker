<template>
  <div class="qr-scanner">
    <div class="scanner-header">
      <h3>Barcode Scanner</h3>
      <button @click="$emit('close')" class="close-btn">
        <Icon name="plus" size="20" />
      </button>
    </div>

    <div class="scanner-content">
      <!-- Camera Scanner -->
      <div v-if="!showUpload" class="camera-scanner">
        <div class="camera-container">
          <div id="qr-reader" class="qr-reader"></div>
          <div class="scanner-overlay">
            <div class="scan-frame"></div>
            <p class="scan-instruction">Position the barcode within the frame</p>
          </div>
        </div>

        <div class="scanner-controls">
          <button @click="toggleUpload" class="upload-btn">
            <Icon name="plus" size="18" />
            Upload Image
          </button>
          <button @click="stopScanner" class="stop-btn">
            Stop Scanner
          </button>
        </div>
      </div>

      <!-- File Upload -->
      <div v-if="showUpload" class="upload-scanner">
        <div class="upload-area" @drop="handleDrop" @dragover.prevent @dragenter.prevent>
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            @change="handleFileSelect"
            class="file-input"
          />
          
          <div class="upload-content">
            <Icon name="qrcode" size="48" />
            <h4>Upload Barcode Image</h4>
            <p>Drag and drop an image or click to select</p>
            <button @click="$refs.fileInput.click()" class="select-file-btn">
              Select Image
            </button>
          </div>
        </div>

        <div class="upload-controls">
          <button @click="toggleUpload" class="camera-btn">
            <Icon name="plus" size="18" />
            Use Camera
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Processing barcode...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="error-state">
        <Icon name="plus" size="24" />
        <p>{{ error }}</p>
        <button @click="clearError" class="retry-btn">Try Again</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Html5QrcodeScanner } from 'html5-qrcode'
import Icon from '@/components/ui/Icon.vue'
import { nutritionService } from '@/services/nutritionService'

const emit = defineEmits(['close', 'barcode-scanned'])

const showUpload = ref(false)
const loading = ref(false)
const error = ref('')
const scanner = ref(null)

const toggleUpload = () => {
  showUpload.value = !showUpload.value
  if (showUpload.value) {
    stopScanner()
  } else {
    startScanner()
  }
}

const startScanner = () => {
  if (scanner.value) return

  scanner.value = new Html5QrcodeScanner(
    "qr-reader",
    {
      fps: 10,
      qrbox: { width: 250, height: 250 },
      aspectRatio: 1.0
    },
    false
  )

  scanner.value.render(onScanSuccess, onScanFailure)
}

const stopScanner = () => {
  if (scanner.value) {
    scanner.value.clear()
    scanner.value = null
  }
}

const onScanSuccess = async (decodedText) => {
  loading.value = true
  error.value = ''

  try {
    emit('barcode-scanned', decodedText)
    stopScanner()
  } catch (err) {
    error.value = 'Failed to process barcode'
  } finally {
    loading.value = false
  }
}

const onScanFailure = (err) => {
  // Ignore scan failures - they happen frequently
}

const handleFileSelect = async (event) => {
  const file = event.target.files[0]
  if (file) {
    await processImageFile(file)
  }
}

const handleDrop = async (event) => {
  event.preventDefault()
  const file = event.dataTransfer.files[0]
  if (file && file.type.startsWith('image/')) {
    await processImageFile(file)
  }
}

const processImageFile = async (file) => {
  loading.value = true
  error.value = ''

  try {
    const result = await nutritionService.scanBarcode(file)
    emit('barcode-scanned', result.barcode)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to scan barcode from image'
  } finally {
    loading.value = false
  }
}

const clearError = () => {
  error.value = ''
}

onMounted(() => {
  if (!showUpload.value) {
    startScanner()
  }
})

onUnmounted(() => {
  stopScanner()
})
</script>

<style lang="scss" scoped>
.qr-scanner {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
}

.scanner-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-lg);
  border-bottom: 1px solid var(--border);

  h3 {
    margin: 0;
    color: var(--text-primary);
  }

  .close-btn {
    background: none;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    padding: var(--space-sm);
    border-radius: var(--radius);
    transition: var(--transition);

    &:hover {
      background: var(--bg-secondary);
      color: var(--text-primary);
    }
  }
}

.scanner-content {
  padding: var(--space-lg);
}

.camera-scanner {
  .camera-container {
    position: relative;
    margin-bottom: var(--space-lg);

    .qr-reader {
      width: 100%;
      border-radius: var(--radius);
      overflow: hidden;
    }

    .scanner-overlay {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      pointer-events: none;

      .scan-frame {
        width: 200px;
        height: 200px;
        border: 2px solid var(--primary);
        border-radius: var(--radius);
        position: relative;

        &::before,
        &::after {
          content: '';
          position: absolute;
          width: 20px;
          height: 20px;
          border: 3px solid var(--primary);
        }

        &::before {
          top: -3px;
          left: -3px;
          border-right: none;
          border-bottom: none;
        }

        &::after {
          bottom: -3px;
          right: -3px;
          border-left: none;
          border-top: none;
        }
      }

      .scan-instruction {
        margin-top: var(--space-lg);
        color: var(--text-primary);
        background: rgba(0, 0, 0, 0.7);
        padding: var(--space-sm) var(--space-md);
        border-radius: var(--radius);
        font-size: 0.875rem;
      }
    }
  }

  .scanner-controls {
    display: flex;
    gap: var(--space-md);
    justify-content: center;

    button {
      display: flex;
      align-items: center;
      gap: var(--space-sm);
      padding: var(--space-md) var(--space-lg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--bg-primary);
      color: var(--text-primary);
      cursor: pointer;
      transition: var(--transition);

      &:hover {
        background: var(--bg-secondary);
      }

      &.upload-btn {
        background: var(--primary);
        color: white;
        border-color: var(--primary);

        &:hover {
          background: var(--primary-dark);
        }
      }
    }
  }
}

.upload-scanner {
  .upload-area {
    border: 2px dashed var(--border);
    border-radius: var(--radius-lg);
    padding: var(--space-3xl);
    text-align: center;
    margin-bottom: var(--space-lg);
    transition: var(--transition);
    cursor: pointer;

    &:hover {
      border-color: var(--primary);
      background: var(--bg-secondary);
    }

    .file-input {
      display: none;
    }

    .upload-content {
      h4 {
        margin: var(--space-lg) 0 var(--space-sm);
        color: var(--text-primary);
      }

      p {
        color: var(--text-secondary);
        margin-bottom: var(--space-lg);
      }

      .select-file-btn {
        background: var(--primary);
        color: white;
        border: none;
        padding: var(--space-md) var(--space-xl);
        border-radius: var(--radius);
        cursor: pointer;
        transition: var(--transition);

        &:hover {
          background: var(--primary-dark);
        }
      }
    }
  }

  .upload-controls {
    display: flex;
    justify-content: center;

    .camera-btn {
      display: flex;
      align-items: center;
      gap: var(--space-sm);
      padding: var(--space-md) var(--space-lg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--bg-primary);
      color: var(--text-primary);
      cursor: pointer;
      transition: var(--transition);

      &:hover {
        background: var(--bg-secondary);
      }
    }
  }
}

.loading-state,
.error-state {
  text-align: center;
  padding: var(--space-3xl);

  .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid var(--border);
    border-top: 3px solid var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto var(--space-lg);
  }

  p {
    color: var(--text-secondary);
    margin-bottom: var(--space-lg);
  }

  .retry-btn {
    background: var(--primary);
    color: white;
    border: none;
    padding: var(--space-md) var(--space-xl);
    border-radius: var(--radius);
    cursor: pointer;
    transition: var(--transition);

    &:hover {
      background: var(--primary-dark);
    }
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .qr-scanner {
    max-width: 100%;
    height: 100vh;
    border-radius: 0;
  }

  .scanner-content {
    padding: var(--space-md);
  }

  .camera-scanner .scanner-overlay .scan-frame {
    width: 150px;
    height: 150px;
  }
}
</style> 
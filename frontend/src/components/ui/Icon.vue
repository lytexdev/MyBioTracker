<template>
  <svg 
    :width="size" 
    :height="size" 
    :class="['icon', `icon-${name}`, className]"
    :style="{ color, fontSize: typeof size === 'number' ? `${size}px` : size }"
    viewBox="0 0 24 24"
    fill="none" 
    xmlns="http://www.w3.org/2000/svg"
    v-html="iconContent"
  />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  size: {
    type: [String, Number],
    default: 24
  },
  color: {
    type: String,
    default: 'currentColor'
  },
  className: {
    type: String,
    default: ''
  }
})

const iconContent = ref('')

const iconMap = {
  'home': () => import('@/assets/icons/home.svg?raw'),
  'user': () => import('@/assets/icons/user.svg?raw'),
  'settings': () => import('@/assets/icons/settings.svg?raw'),
  'chart-line': () => import('@/assets/icons/chart-line.svg?raw'),
  'coffee': () => import('@/assets/icons/coffee.svg?raw'),
  'apple': () => import('@/assets/icons/apple.svg?raw'),
  'logout': () => import('@/assets/icons/logout.svg?raw'),
  'moon': () => import('@/assets/icons/moon.svg?raw'),
  'sun': () => import('@/assets/icons/sun.svg?raw'),
  'qrcode': () => import('@/assets/icons/qrcode.svg?raw'),
  'plus': () => import('@/assets/icons/plus.svg?raw'),
  'check-circle': () => import('@/assets/icons/check-circle.svg?raw'),
  'alert-circle': () => import('@/assets/icons/alert-circle.svg?raw'),
  'alert-triangle': () => import('@/assets/icons/alert-triangle.svg?raw'),
  'info': () => import('@/assets/icons/info-circle.svg?raw'),
  'x': () => import('@/assets/icons/x.svg?raw'),
  'eye': () => import('@/assets/icons/eye.svg?raw'),
  'eye-off': () => import('@/assets/icons/eye-off.svg?raw'),
  'loader': () => import('@/assets/icons/loader.svg?raw'),
  'chrome': () => import('@/assets/icons/chrome.svg?raw'),
  'play': () => import('@/assets/icons/play.svg?raw'),
  'utensils': () => import('@/assets/icons/utensils.svg?raw'),
  'target': () => import('@/assets/icons/target.svg?raw'),
  'trending-up': () => import('@/assets/icons/trending-up.svg?raw'),
  'chevron-down': () => import('@/assets/icons/chevron-down.svg?raw'),
  'chevron-up': () => import('@/assets/icons/chevron-up.svg?raw'),
  'arrow-left': () => import('@/assets/icons/arrow-left.svg?raw'),
  'menu': () => import('@/assets/icons/menu.svg?raw'),
  'log-out': () => import('@/assets/icons/log-out.svg?raw'),
  'activity': () => import('@/assets/icons/activity.svg?raw'),
  'camera': () => import('@/assets/icons/camera.svg?raw'),
  'check': () => import('@/assets/icons/check.svg?raw'),
  'clock': () => import('@/assets/icons/clock.svg?raw'),
  'zap': () => import('@/assets/icons/zap.svg?raw')
}

onMounted(async () => {
  try {
    if (iconMap[props.name]) {
      const iconModule = await iconMap[props.name]()
      const svgContent = iconModule.default || iconModule
      
      const parser = new DOMParser()
      const doc = parser.parseFromString(svgContent, 'image/svg+xml')
      const svgElement = doc.querySelector('svg')
      
      if (svgElement) {
        iconContent.value = svgElement.innerHTML
      }
    }
  } catch (error) {
    console.warn(`Icon "${props.name}" could not be loaded:`, error)
  }
})
</script>

<style lang="scss" scoped>
.icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  flex-shrink: 0;
  
  // Ensure proper viewBox scaling
  width: 1em;
  height: 1em;
  
  // Better text alignment
  position: relative;
  top: -0.1em;
  
  // Prevent icon from being cut off
  overflow: visible;
  
  // Smooth rendering
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

// Specific sizes when size prop is used
.icon[width="16"],
.icon[height="16"] {
  width: 16px;
  height: 16px;
  top: -0.05em;
}

.icon[width="18"],
.icon[height="18"] {
  width: 18px;
  height: 18px;
  top: -0.075em;
}

.icon[width="20"],
.icon[height="20"] {
  width: 20px;
  height: 20px;
  top: -0.075em;
}

.icon[width="24"],
.icon[height="24"] {
  width: 24px;
  height: 24px;
  top: -0.1em;
}

.icon[width="32"],
.icon[height="32"] {
  width: 32px;
  height: 32px;
  top: -0.125em;
}

// Special positioning for buttons
button .icon,
.btn .icon {
  margin-right: 0.125em;
  top: 0;
  vertical-align: text-top;
}

// Special positioning for form inputs
.form-input + .icon,
.password-toggle .icon {
  top: 0;
  vertical-align: middle;
}
</style>

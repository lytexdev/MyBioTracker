<template>
  <svg 
    :width="size" 
    :height="size" 
    :viewBox="viewBox" 
    fill="none" 
    stroke="currentColor" 
    stroke-width="2" 
    stroke-linecap="round" 
    stroke-linejoin="round"
    :class="['icon', `icon-${name}`]"
  >
    <component :is="iconComponent" />
  </svg>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  size: {
    type: [String, Number],
    default: 24
  }
})

const viewBox = computed(() => `0 0 24 24`)

// Simple icon components using SVG paths
const icons = {
  // Navigation
  'chevron-left': () => h('path', { d: 'm15 18-6-6 6-6' }),
  'chevron-right': () => h('path', { d: 'm9 18 6-6-6-6' }),
  'chevron-up': () => h('path', { d: 'm18 15-6-6-6 6' }),
  'chevron-down': () => h('path', { d: 'm6 9 6 6 6-6' }),
  'arrow-left': () => h('path', { d: 'M19 12H5m7-7-7 7 7 7' }),
  'arrow-right': () => h('path', { d: 'M5 12h14m-7-7 7 7-7 7' }),
  
  // Actions
  'plus': () => h('path', { d: 'M12 5v14m-7-7h14' }),
  'minus': () => h('path', { d: 'M5 12h14' }),
  'x': () => h('path', { d: 'M18 6 6 18M6 6l12 12' }),
  'check': () => h('path', { d: 'M20 6 9 17l-5-5' }),
  'edit': () => h('path', { d: 'M12 20h9M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z' }),
  'trash': () => h('g', {}, [
    h('path', { d: 'M3 6h18' }),
    h('path', { d: 'M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6' }),
    h('path', { d: 'M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2' })
  ]),
  'search': () => h('g', {}, [
    h('circle', { cx: '11', cy: '11', r: '8' }),
    h('path', { d: 'm21 21-4.35-4.35' })
  ]),
  'filter': () => h('path', { d: 'M22 3H2l8 9.46V19l4 2v-8.54L22 3z' }),
  'settings': () => h('g', {}, [
    h('circle', { cx: '12', cy: '12', r: '3' }),
    h('path', { d: 'M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z' })
  ]),
  
  // Food & Nutrition
  'utensils': () => h('g', {}, [
    h('path', { d: 'M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2' }),
    h('path', { d: 'M7 2v20' }),
    h('path', { d: 'M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3z' })
  ]),
  'coffee': () => h('g', {}, [
    h('path', { d: 'M18 8h1a4 4 0 0 1 0 8h-1' }),
    h('path', { d: 'M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z' }),
    h('line', { x1: '6', y1: '1', x2: '6', y2: '4' }),
    h('line', { x1: '10', y1: '1', x2: '10', y2: '4' }),
    h('line', { x1: '14', y1: '1', x2: '14', y2: '4' })
  ]),
  
  // Camera & Scanning
  'camera': () => h('g', {}, [
    h('path', { d: 'M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z' }),
    h('circle', { cx: '12', cy: '13', r: '4' })
  ]),
  'upload': () => h('g', {}, [
    h('path', { d: 'M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4' }),
    h('polyline', { points: '7,10 12,5 17,10' }),
    h('line', { x1: '12', y1: '5', x2: '12', y2: '15' })
  ]),
  
  // Energy & Caffeine
  'zap': () => h('path', { d: 'M13 2 3 14h9l-1 8 10-12h-9l1-8z' }),
  'trending-up': () => h('g', {}, [
    h('polyline', { points: '22,7 13.5,15.5 8.5,10.5 2,17' }),
    h('polyline', { points: '16,7 22,7 22,13' })
  ]),
  
  // User & Profile
  'user': () => h('g', {}, [
    h('path', { d: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2' }),
    h('circle', { cx: '12', cy: '7', r: '4' })
  ]),
  'users': () => h('g', {}, [
    h('path', { d: 'M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2' }),
    h('circle', { cx: '9', cy: '7', r: '4' }),
    h('path', { d: 'M22 21v-2a4 4 0 0 0-3-3.87' }),
    h('path', { d: 'M16 3.13a4 4 0 0 1 0 7.75' })
  ]),
  
  // Status & Feedback
  'alert-circle': () => h('g', {}, [
    h('circle', { cx: '12', cy: '12', r: '10' }),
    h('line', { x1: '12', y1: '8', x2: '12', y2: '12' }),
    h('line', { x1: '12', y1: '16', x2: '12.01', y2: '16' })
  ]),
  'alert-triangle': () => h('g', {}, [
    h('path', { d: 'M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z' }),
    h('line', { x1: '12', y1: '9', x2: '12', y2: '13' }),
    h('line', { x1: '12', y1: '17', x2: '12.01', y2: '17' })
  ]),
  'info': () => h('g', {}, [
    h('circle', { cx: '12', cy: '12', r: '10' }),
    h('line', { x1: '12', y1: '16', x2: '12', y2: '12' }),
    h('line', { x1: '12', y1: '8', x2: '12.01', y2: '8' })
  ]),
  'check-circle': () => h('g', {}, [
    h('path', { d: 'M22 11.08V12a10 10 0 1 1-5.93-9.14' }),
    h('polyline', { points: '22,4 12,14.01 9,11.01' })
  ]),
  
  // Loading
  'loader': () => h('g', {}, [
    h('line', { x1: '12', y1: '2', x2: '12', y2: '6' }),
    h('line', { x1: '12', y1: '18', x2: '12', y2: '22' }),
    h('line', { x1: '4.93', y1: '4.93', x2: '7.76', y2: '7.76' }),
    h('line', { x1: '16.24', y1: '16.24', x2: '19.07', y2: '19.07' }),
    h('line', { x1: '2', y1: '12', x2: '6', y2: '12' }),
    h('line', { x1: '18', y1: '12', x2: '22', y2: '12' }),
    h('line', { x1: '4.93', y1: '19.07', x2: '7.76', y2: '16.24' }),
    h('line', { x1: '16.24', y1: '7.76', x2: '19.07', y2: '4.93' })
  ]),
  
  // Misc
  'hash': () => h('g', {}, [
    h('line', { x1: '4', y1: '9', x2: '20', y2: '9' }),
    h('line', { x1: '4', y1: '15', x2: '20', y2: '15' }),
    h('line', { x1: '10', y1: '3', x2: '8', y2: '21' }),
    h('line', { x1: '16', y1: '3', x2: '14', y2: '21' })
  ]),
  'target': () => h('g', {}, [
    h('circle', { cx: '12', cy: '12', r: '10' }),
    h('circle', { cx: '12', cy: '12', r: '6' }),
    h('circle', { cx: '12', cy: '12', r: '2' })
  ]),
  'calculator': () => h('g', {}, [
    h('rect', { x: '4', y: '2', width: '16', height: '20', rx: '2' }),
    h('line', { x1: '8', y1: '6', x2: '16', y2: '6' }),
    h('line', { x1: '8', y1: '10', x2: '8', y2: '10.01' }),
    h('line', { x1: '12', y1: '10', x2: '12', y2: '10.01' }),
    h('line', { x1: '16', y1: '10', x2: '16', y2: '10.01' }),
    h('line', { x1: '8', y1: '14', x2: '8', y2: '14.01' }),
    h('line', { x1: '12', y1: '14', x2: '12', y2: '14.01' }),
    h('line', { x1: '16', y1: '14', x2: '16', y2: '14.01' }),
    h('line', { x1: '8', y1: '18', x2: '8', y2: '18.01' }),
    h('line', { x1: '12', y1: '18', x2: '12', y2: '18.01' })
  ])
}

const iconComponent = computed(() => {
  const iconName = props.name
  const iconFn = icons[iconName]
  
  if (!iconFn) {
    console.warn(`Icon "${iconName}" not found`)
    return () => h('circle', { cx: '12', cy: '12', r: '2' }) // Fallback dot
  }
  
  return iconFn
})

// Helper function to create VNode (this would be imported from Vue in a real component)
function h(tag, props = {}, children = []) {
  return {
    tag,
    props,
    children: Array.isArray(children) ? children : [children]
  }
}
</script>

<style scoped>
.icon {
  display: inline-block;
  vertical-align: middle;
  flex-shrink: 0;
}
</style>

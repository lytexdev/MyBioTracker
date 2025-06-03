<template>
  <nav class="navbar">
    <div class="navbar-container">
      <!-- Logo and Brand -->
      <div class="navbar-brand">
        <router-link to="/dashboard" class="brand-link">
          <div class="brand-icon">
            <Icon name="home" size="24" />
          </div>
          <span class="brand-text">MyBioTracker</span>
        </router-link>
      </div>

      <!-- Desktop Navigation -->
      <div class="navbar-nav desktop-nav">
        <router-link to="/dashboard" class="nav-link">
          <Icon name="home" size="18" />
          <span>Dashboard</span>
        </router-link>
        
        <router-link to="/nutrition" class="nav-link">
          <Icon name="apple" size="18" />
          <span>Nutrition</span>
        </router-link>
        
        <router-link to="/caffeine" class="nav-link">
          <Icon name="coffee" size="18" />
          <span>Caffeine</span>
        </router-link>
        
        <router-link to="/reports" class="nav-link">
          <Icon name="chart-line" size="18" />
          <span>Reports</span>
        </router-link>
      </div>

      <!-- Right Side Actions -->
      <div class="navbar-actions">
        <!-- Theme Toggle -->
        <ThemeToggle />

        <!-- User Dropdown -->
        <div class="user-dropdown" ref="dropdownRef">
          <button @click="toggleDropdown" class="user-button">
            <div class="user-avatar">
              {{ userInitials }}
            </div>
            <Icon name="plus" size="16" :class="{ 'rotate': showDropdown }" />
          </button>

          <div v-if="showDropdown" class="dropdown-menu">
            <div class="dropdown-header">
              <div class="user-info">
                <div class="user-name">{{ authStore.user?.email }}</div>
                <div class="user-role">{{ authStore.user?.is_admin ? 'Admin' : 'User' }}</div>
              </div>
            </div>

            <div class="dropdown-divider"></div>

            <router-link to="/profile" class="dropdown-item" @click="closeDropdown">
              <Icon name="user" size="16" />
              <span>Profile</span>
            </router-link>

            <router-link 
              v-if="authStore.user?.is_admin" 
              to="/admin" 
              class="dropdown-item" 
              @click="closeDropdown"
            >
              <Icon name="settings" size="16" />
              <span>Admin Panel</span>
            </router-link>

            <div class="dropdown-divider"></div>

            <button @click="handleLogout" class="dropdown-item logout">
              <Icon name="logout" size="16" />
              <span>Logout</span>
            </button>
          </div>
        </div>

        <!-- Mobile Menu Toggle -->
        <button @click="toggleMobileMenu" class="mobile-menu-toggle">
          <Icon :name="showMobileMenu ? 'plus' : 'plus'" size="20" />
        </button>
      </div>
    </div>

    <!-- Mobile Navigation -->
    <div v-if="showMobileMenu" class="mobile-nav">
      <router-link to="/dashboard" class="mobile-nav-link" @click="closeMobileMenu">
        <Icon name="home" size="18" />
        <span>Dashboard</span>
      </router-link>
      
      <router-link to="/nutrition" class="mobile-nav-link" @click="closeMobileMenu">
        <Icon name="apple" size="18" />
        <span>Nutrition</span>
      </router-link>
      
      <router-link to="/caffeine" class="mobile-nav-link" @click="closeMobileMenu">
        <Icon name="coffee" size="18" />
        <span>Caffeine</span>
      </router-link>
      
      <router-link to="/reports" class="mobile-nav-link" @click="closeMobileMenu">
        <Icon name="chart-line" size="18" />
        <span>Reports</span>
      </router-link>

      <div class="mobile-nav-divider"></div>

      <!-- Theme Toggle for Mobile -->
      <div class="mobile-theme-toggle">
        <ThemeToggle />
        <span>Dark Mode</span>
      </div>

      <router-link to="/profile" class="mobile-nav-link" @click="closeMobileMenu">
        <Icon name="user" size="18" />
        <span>Profile</span>
      </router-link>

      <router-link 
        v-if="authStore.user?.is_admin" 
        to="/admin" 
        class="mobile-nav-link" 
        @click="closeMobileMenu"
      >
        <Icon name="settings" size="18" />
        <span>Admin Panel</span>
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import Icon from '@/components/ui/Icon.vue'
import ThemeToggle from '@/components/ThemeToggle.vue'

const authStore = useAuthStore()
const themeStore = useThemeStore()

const showDropdown = ref(false)
const showMobileMenu = ref(false)
const dropdownRef = ref(null)

const userInitials = computed(() => {
  const email = authStore.user?.email || ''
  return email.substring(0, 2).toUpperCase()
})

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const closeDropdown = () => {
  showDropdown.value = false
}

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const closeMobileMenu = () => {
  showMobileMenu.value = false
}

const handleLogout = async () => {
  closeDropdown()
  await authStore.logout()
}

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style lang="scss" scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(10px);
  box-shadow: var(--shadow-sm);
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--space-lg);
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-brand {
  .brand-link {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    text-decoration: none;
    color: var(--text-primary);
    font-weight: 600;
    font-size: 1.25rem;
    
    &:hover {
      text-decoration: none;
    }
  }
  
  .brand-icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    border-radius: var(--radius);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
  }
  
  .brand-text {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
}

.desktop-nav {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  
  @media (max-width: 768px) {
    display: none;
  }
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius);
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  transition: var(--transition);
  
  &:hover {
    color: var(--primary);
    background: var(--bg-secondary);
    text-decoration: none;
  }
  
  &.router-link-active {
    color: var(--primary);
    background: var(--primary-light);
    background: rgba(34, 197, 94, 0.1);
  }
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.theme-toggle {
  width: 40px;
  height: 40px;
  border: none;
  background: var(--bg-secondary);
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-tertiary);
    color: var(--primary);
  }
}

.user-dropdown {
  position: relative;
}

.user-button {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-xs) var(--space-sm);
  background: none;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-secondary);
  }
}

.user-avatar {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
}

.rotate {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + var(--space-xs));
  right: 0;
  min-width: 200px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  padding: var(--space-sm);
  z-index: 1000;
  animation: fadeIn var(--transition-fast) ease-out;
}

.dropdown-header {
  padding: var(--space-sm);
}

.user-info {
  .user-name {
    font-weight: 500;
    color: var(--text-primary);
    font-size: 0.875rem;
  }
  
  .user-role {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: var(--space-xs);
  }
}

.dropdown-divider {
  height: 1px;
  background: var(--border);
  margin: var(--space-sm) 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  width: 100%;
  padding: var(--space-sm);
  border: none;
  background: none;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: var(--radius);
  cursor: pointer;
  transition: var(--transition);
  font-size: 0.875rem;
  
  &:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
    text-decoration: none;
  }
  
  &.logout {
    color: var(--error);
    
    &:hover {
      background: rgba(239, 68, 68, 0.1);
      color: var(--error);
    }
  }
}

.mobile-menu-toggle {
  display: none;
  width: 40px;
  height: 40px;
  border: none;
  background: var(--bg-secondary);
  border-radius: var(--radius);
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-tertiary);
    color: var(--primary);
  }
  
  @media (max-width: 768px) {
    display: flex;
  }
}

.mobile-nav {
  display: none;
  background: var(--bg-primary);
  border-top: 1px solid var(--border);
  padding: var(--space-md);
  
  @media (max-width: 768px) {
    display: block;
  }
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-md);
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: var(--radius);
  margin-bottom: var(--space-xs);
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-secondary);
    color: var(--primary);
    text-decoration: none;
  }
  
  &.router-link-active {
    background: rgba(34, 197, 94, 0.1);
    color: var(--primary);
  }
}

.mobile-nav-divider {
  height: 1px;
  background: var(--border);
  margin: var(--space-md) 0;
}

.mobile-theme-toggle {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm);
  border-radius: var(--radius);
  background: var(--bg-secondary);
  cursor: pointer;
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-tertiary);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

<template>
  <div class="dashboard-layout">
    <!-- Header -->
    <header class="app-header">
      <div class="header-content">
        <div class="header-left">
          <router-link to="/dashboard" class="logo">
            <h1>MyBioTracker</h1>
          </router-link>
        </div>
        
        <nav class="main-nav">
          <router-link to="/dashboard" class="nav-link">
            <Icon name="target" size="20" />
            Dashboard
          </router-link>
          <router-link to="/nutrition" class="nav-link">
            <Icon name="utensils" size="20" />
            Nutrition
          </router-link>
          <router-link to="/caffeine" class="nav-link">
            <Icon name="coffee" size="20" />
            Caffeine
          </router-link>
          <router-link to="/reports" class="nav-link">
            <Icon name="trending-up" size="20" />
            Reports
          </router-link>
        </nav>
        
        <div class="header-right">
          <!-- Language Switcher -->
          <LanguageSwitcher />
          
          <button @click="showUserMenu = !showUserMenu" class="user-menu-trigger">
            <Icon name="user" size="20" />
            <span>{{ user?.email || 'User' }}</span>
            <Icon name="chevron-down" size="16" />
          </button>
          
          <div v-if="showUserMenu" class="user-menu" @click.stop>
            <div class="user-menu-content">
              <router-link to="/profile" class="menu-item" @click="showUserMenu = false">
                <Icon name="settings" size="16" />
                Profile Settings
              </router-link>
              <button @click="handleLogout" class="menu-item logout">
                <Icon name="log-out" size="16" />
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Mobile Navigation -->
    <nav class="mobile-nav">
      <router-link to="/dashboard" class="mobile-nav-link">
        <Icon name="target" size="20" />
        <span>Dashboard</span>
      </router-link>
      <router-link to="/nutrition" class="mobile-nav-link">
        <Icon name="utensils" size="20" />
        <span>Nutrition</span>
      </router-link>
      <router-link to="/caffeine" class="mobile-nav-link">
        <Icon name="coffee" size="20" />
        <span>Caffeine</span>
      </router-link>
      <router-link to="/reports" class="mobile-nav-link">
        <Icon name="trending-up" size="20" />
        <span>Reports</span>
      </router-link>
    </nav>

    <!-- Main Content -->
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'
import Icon from '@/components/ui/Icon.vue'
import LanguageSwitcher from '@/components/ui/LanguageSwitcher.vue'

const router = useRouter()
const authStore = useAuthStore()
const toastStore = useToastStore()

const showUserMenu = ref(false)

const user = computed(() => authStore.user)

const handleLogout = async () => {
  await authStore.logout()
  toastStore.info('You have been signed out')
}

const closeUserMenu = (event) => {
  if (!event.target.closest('.user-menu-trigger') && !event.target.closest('.user-menu')) {
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', closeUserMenu)
})

onUnmounted(() => {
  document.removeEventListener('click', closeUserMenu)
})
</script>

<style lang="scss" scoped>
.dashboard-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
  
  @media (max-width: 768px) {
    display: none;
  }
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-xl);
  height: 64px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.header-left {
  .logo {
    text-decoration: none;
    color: var(--text-primary);
    
    h1 {
      margin: 0;
      font-size: 1.5rem;
      font-weight: 700;
      background: linear-gradient(135deg, var(--primary), var(--primary-dark));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
  }
}

.main-nav {
  display: flex;
  align-items: center;
  gap: var(--space-lg);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius);
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 500;
  transition: var(--transition);
  
  &:hover {
    color: var(--text-primary);
    background: var(--bg-secondary);
  }
  
  &.router-link-active {
    color: var(--primary);
    background: var(--primary-light);
  }
}

.header-right {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.user-menu-trigger {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  border: 1px solid var(--border);
  background: var(--bg-primary);
  border-radius: var(--radius);
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-secondary);
    border-color: var(--primary);
  }
  
  span {
    font-size: 0.875rem;
    font-weight: 500;
  }
}

.user-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: var(--space-sm);
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  min-width: 200px;
  z-index: 1000;
}

.user-menu-content {
  padding: var(--space-sm);
}

.menu-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  width: 100%;
  padding: var(--space-md);
  border: none;
  background: none;
  border-radius: var(--radius);
  color: var(--text-secondary);
  text-decoration: none;
  cursor: pointer;
  transition: var(--transition);
  font-size: 0.875rem;
  
  &:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
  }
  
  &.logout {
    color: var(--error);
    
    &:hover {
      background: #fef2f2;
      color: var(--error);
    }
  }
}

.mobile-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--bg-primary);
  border-top: 1px solid var(--border);
  padding: var(--space-sm);
  z-index: 100;
  
  @media (max-width: 768px) {
    display: flex;
    justify-content: space-around;
  }
}

.mobile-nav-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-sm);
  border-radius: var(--radius);
  text-decoration: none;
  color: var(--text-secondary);
  font-size: 0.75rem;
  font-weight: 500;
  transition: var(--transition);
  min-width: 60px;
  
  &:hover {
    color: var(--text-primary);
    background: var(--bg-secondary);
  }
  
  &.router-link-active {
    color: var(--primary);
    background: var(--primary-light);
  }
}

.app-main {
  flex: 1;
  
  @media (max-width: 768px) {
    padding-bottom: 80px; // Space for mobile nav
  }
}
</style>

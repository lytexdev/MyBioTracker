<template>
  <div class="admin-page">
    <div class="page-header">
      <h1>Admin Panel</h1>
      <p>Verwaltung und Übersicht der MyBioTracker-Anwendung</p>
    </div>

    <div class="admin-grid">
      <!-- User Management -->
      <div class="admin-card">
        <div class="card-header">
          <Icon name="users" size="24" />
          <h2>Benutzerverwaltung</h2>
        </div>
        <div class="card-content">
          <div class="stat">
            <span class="stat-value">{{ userStats.total }}</span>
            <span class="stat-label">Gesamte Benutzer</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ userStats.active }}</span>
            <span class="stat-label">Aktive Benutzer</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ userStats.newToday }}</span>
            <span class="stat-label">Neue heute</span>
          </div>
        </div>
        <div class="card-actions">
          <button class="btn btn-outline" @click="loadUsers">
            Benutzer anzeigen
          </button>
        </div>
      </div>

      <!-- System Health -->
      <div class="admin-card">
        <div class="card-header">
          <Icon name="activity" size="24" />
          <h2>System Status</h2>
        </div>
        <div class="card-content">
          <div class="health-item">
            <span class="health-label">API Status</span>
            <span class="health-status" :class="systemHealth.api">
              {{ systemHealth.api }}
            </span>
          </div>
          <div class="health-item">
            <span class="health-label">Datenbank</span>
            <span class="health-status" :class="systemHealth.database">
              {{ systemHealth.database }}
            </span>
          </div>
          <div class="health-item">
            <span class="health-label">Redis Cache</span>
            <span class="health-status" :class="systemHealth.redis">
              {{ systemHealth.redis }}
            </span>
          </div>
        </div>
        <div class="card-actions">
          <button class="btn btn-outline" @click="checkSystemHealth">
            Status prüfen
          </button>
        </div>
      </div>

      <!-- Database Stats -->
      <div class="admin-card">
        <div class="card-header">
          <Icon name="database" size="24" />
          <h2>Datenbank Statistiken</h2>
        </div>
        <div class="card-content">
          <div class="stat">
            <span class="stat-value">{{ dbStats.nutritionEntries }}</span>
            <span class="stat-label">Ernährungseinträge</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ dbStats.caffeineEntries }}</span>
            <span class="stat-label">Koffein-Einträge</span>
          </div>
          <div class="stat">
            <span class="stat-value">{{ dbStats.foodItems }}</span>
            <span class="stat-label">Lebensmittel</span>
          </div>
        </div>
        <div class="card-actions">
          <button class="btn btn-outline" @click="loadDatabaseStats">
            Aktualisieren
          </button>
        </div>
      </div>

      <!-- Application Settings -->
      <div class="admin-card">
        <div class="card-header">
          <Icon name="settings" size="24" />
          <h2>Anwendungseinstellungen</h2>
        </div>
        <div class="card-content">
          <div class="setting-item">
            <label class="setting-label">
              <input 
                type="checkbox" 
                v-model="settings.allowRegistration"
                @change="updateSetting('allowRegistration', $event.target.checked)"
              />
              Registrierung erlauben
            </label>
          </div>
          <div class="setting-item">
            <label class="setting-label">
              <input 
                type="checkbox" 
                v-model="settings.maintenanceMode"
                @change="updateSetting('maintenanceMode', $event.target.checked)"
              />
              Wartungsmodus
            </label>
          </div>
          <div class="setting-item">
            <label class="setting-label">
              <input 
                type="checkbox" 
                v-model="settings.require2FA"
                @change="updateSetting('require2FA', $event.target.checked)"
              />
              2FA erforderlich
            </label>
          </div>
        </div>
      </div>

      <!-- Logs -->
      <div class="admin-card full-width">
        <div class="card-header">
          <Icon name="file-text" size="24" />
          <h2>System Logs</h2>
        </div>
        <div class="card-content">
          <div class="log-container">
            <div v-if="logs.length === 0" class="no-logs">
              Keine Logs verfügbar
            </div>
            <div v-else class="log-entries">
              <div 
                v-for="log in logs" 
                :key="log.id"
                class="log-entry"
                :class="log.level"
              >
                <span class="log-time">{{ formatTime(log.timestamp) }}</span>
                <span class="log-level">{{ log.level.toUpperCase() }}</span>
                <span class="log-message">{{ log.message }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="card-actions">
          <button class="btn btn-outline" @click="loadLogs">
            Logs laden
          </button>
          <button class="btn btn-outline" @click="clearLogs">
            Logs löschen
          </button>
        </div>
      </div>
    </div>

    <!-- User List Modal -->
    <div v-if="showUserModal" class="modal-overlay" @click="showUserModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>Benutzerliste</h3>
          <button @click="showUserModal = false" class="modal-close">
            <Icon name="x" size="20" />
          </button>
        </div>
        <div class="modal-content">
          <div v-if="users.length === 0" class="no-users">
            Keine Benutzer gefunden
          </div>
          <div v-else class="user-list">
            <div 
              v-for="user in users" 
              :key="user.id"
              class="user-item"
            >
              <div class="user-info">
                <span class="user-email">{{ user.email }}</span>
                <span class="user-status" :class="{ active: user.is_active }">
                  {{ user.is_active ? 'Aktiv' : 'Inaktiv' }}
                </span>
              </div>
              <div class="user-actions">
                <button 
                  class="btn btn-sm btn-outline"
                  @click="toggleUserStatus(user)"
                >
                  {{ user.is_active ? 'Deaktivieren' : 'Aktivieren' }}
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
import { ref, onMounted } from 'vue'
import { useToastStore } from '@/stores/toast'
import Icon from '@/components/ui/Icon.vue'

const toastStore = useToastStore()

// State
const userStats = ref({
  total: 0,
  active: 0,
  newToday: 0
})

const systemHealth = ref({
  api: 'healthy',
  database: 'healthy',
  redis: 'healthy'
})

const dbStats = ref({
  nutritionEntries: 0,
  caffeineEntries: 0,
  foodItems: 0
})

const settings = ref({
  allowRegistration: true,
  maintenanceMode: false,
  require2FA: false
})

const logs = ref([])
const users = ref([])
const showUserModal = ref(false)
const loading = ref(false)

// Methods
const loadUsers = async () => {
  try {
    loading.value = true
    // TODO: Implement API call
    // const response = await fetch('/api/admin/users')
    // users.value = await response.json()
    
    // Mock data for now
    users.value = [
      { id: 1, email: 'admin@example.com', is_active: true },
      { id: 2, email: 'user@example.com', is_active: true },
    ]
    
    showUserModal.value = true
  } catch (error) {
    toastStore.error('Fehler beim Laden der Benutzer')
  } finally {
    loading.value = false
  }
}

const checkSystemHealth = async () => {
  try {
    loading.value = true
    // TODO: Implement API call
    // const response = await fetch('/api/admin/health')
    // systemHealth.value = await response.json()
    
    toastStore.success('System Status geprüft')
  } catch (error) {
    toastStore.error('Fehler beim Prüfen des System Status')
  } finally {
    loading.value = false
  }
}

const loadDatabaseStats = async () => {
  try {
    loading.value = true
    // TODO: Implement API call
    // const response = await fetch('/api/admin/stats')
    // dbStats.value = await response.json()
    
    // Mock data for now
    dbStats.value = {
      nutritionEntries: 1234,
      caffeineEntries: 567,
      foodItems: 8901
    }
    
    toastStore.success('Statistiken aktualisiert')
  } catch (error) {
    toastStore.error('Fehler beim Laden der Statistiken')
  } finally {
    loading.value = false
  }
}

const updateSetting = async (key, value) => {
  try {
    // TODO: Implement API call
    // await fetch('/api/admin/settings', {
    //   method: 'PUT',
    //   body: JSON.stringify({ [key]: value })
    // })
    
    toastStore.success('Einstellung gespeichert')
  } catch (error) {
    toastStore.error('Fehler beim Speichern der Einstellung')
  }
}

const loadLogs = async () => {
  try {
    loading.value = true
    // TODO: Implement API call
    // const response = await fetch('/api/admin/logs')
    // logs.value = await response.json()
    
    // Mock data for now
    logs.value = [
      {
        id: 1,
        timestamp: new Date(),
        level: 'info',
        message: 'Benutzer hat sich angemeldet'
      },
      {
        id: 2,
        timestamp: new Date(Date.now() - 60000),
        level: 'warning',
        message: 'Fehlgeschlagener Login-Versuch'
      },
      {
        id: 3,
        timestamp: new Date(Date.now() - 120000),
        level: 'error',
        message: 'Datenbankverbindung unterbrochen'
      }
    ]
    
    toastStore.success('Logs geladen')
  } catch (error) {
    toastStore.error('Fehler beim Laden der Logs')
  } finally {
    loading.value = false
  }
}

const clearLogs = async () => {
  try {
    // TODO: Implement API call
    // await fetch('/api/admin/logs', { method: 'DELETE' })
    
    logs.value = []
    toastStore.success('Logs gelöscht')
  } catch (error) {
    toastStore.error('Fehler beim Löschen der Logs')
  }
}

const toggleUserStatus = async (user) => {
  try {
    // TODO: Implement API call
    // await fetch(`/api/admin/users/${user.id}/toggle`, { method: 'PUT' })
    
    user.is_active = !user.is_active
    toastStore.success(`Benutzer ${user.is_active ? 'aktiviert' : 'deaktiviert'}`)
  } catch (error) {
    toastStore.error('Fehler beim Ändern des Benutzerstatus')
  }
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleString('de-DE')
}

const loadInitialData = async () => {
  // Load initial stats
  userStats.value = {
    total: 42,
    active: 38,
    newToday: 3
  }
  
  await loadDatabaseStats()
}

onMounted(() => {
  loadInitialData()
})
</script>

<style lang="scss" scoped>
.admin-page {
  padding: var(--space-xl);
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: var(--space-2xl);
  
  h1 {
    margin-bottom: var(--space-sm);
    color: var(--text-primary);
    font-size: 2rem;
    font-weight: 700;
  }
  
  p {
    color: var(--text-secondary);
    font-size: 1.125rem;
  }
}

.admin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: var(--space-xl);
}

.admin-card {
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  
  &.full-width {
    grid-column: 1 / -1;
  }
}

.card-header {
  padding: var(--space-lg);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: var(--space-md);
  
  h2 {
    margin: 0;
    color: var(--text-primary);
    font-size: 1.25rem;
    font-weight: 600;
  }
  
  svg {
    color: var(--primary);
  }
}

.card-content {
  padding: var(--space-lg);
}

.card-actions {
  padding: var(--space-lg);
  border-top: 1px solid var(--border);
  display: flex;
  gap: var(--space-md);
}

.stat {
  display: flex;
  flex-direction: column;
  margin-bottom: var(--space-md);
  
  &:last-child {
    margin-bottom: 0;
  }
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary);
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: var(--space-xs);
}

.health-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-md);
  
  &:last-child {
    margin-bottom: 0;
  }
}

.health-label {
  color: var(--text-primary);
  font-weight: 500;
}

.health-status {
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  
  &.healthy {
    background: rgba(34, 197, 94, 0.1);
    color: var(--success);
  }
  
  &.warning {
    background: rgba(245, 158, 11, 0.1);
    color: var(--warning);
  }
  
  &.error {
    background: rgba(239, 68, 68, 0.1);
    color: var(--error);
  }
}

.setting-item {
  margin-bottom: var(--space-md);
  
  &:last-child {
    margin-bottom: 0;
  }
}

.setting-label {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  color: var(--text-primary);
  cursor: pointer;
  
  input[type="checkbox"] {
    width: 16px;
    height: 16px;
    accent-color: var(--primary);
  }
}

.log-container {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.no-logs {
  padding: var(--space-xl);
  text-align: center;
  color: var(--text-muted);
}

.log-entries {
  display: flex;
  flex-direction: column;
}

.log-entry {
  padding: var(--space-sm) var(--space-md);
  border-bottom: 1px solid var(--border);
  display: flex;
  gap: var(--space-md);
  font-family: var(--font-mono);
  font-size: 0.875rem;
  
  &:last-child {
    border-bottom: none;
  }
  
  &.error {
    background: rgba(239, 68, 68, 0.05);
  }
  
  &.warning {
    background: rgba(245, 158, 11, 0.05);
  }
  
  &.info {
    background: rgba(59, 130, 246, 0.05);
  }
}

.log-time {
  color: var(--text-muted);
  white-space: nowrap;
}

.log-level {
  font-weight: 600;
  min-width: 60px;
  
  .log-entry.error & {
    color: var(--error);
  }
  
  .log-entry.warning & {
    color: var(--warning);
  }
  
  .log-entry.info & {
    color: var(--info);
  }
}

.log-message {
  color: var(--text-primary);
  flex: 1;
}

// Modal styles
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
}

.modal {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: var(--shadow-xl);
}

.modal-header {
  padding: var(--space-lg);
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  h3 {
    margin: 0;
    color: var(--text-primary);
    font-size: 1.25rem;
    font-weight: 600;
  }
}

.modal-close {
  border: none;
  background: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: var(--space-xs);
  border-radius: var(--radius);
  transition: var(--transition);
  
  &:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
  }
}

.modal-content {
  padding: var(--space-lg);
  max-height: 60vh;
  overflow-y: auto;
}

.no-users {
  text-align: center;
  color: var(--text-muted);
  padding: var(--space-xl);
}

.user-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.user-item {
  padding: var(--space-md);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.user-email {
  color: var(--text-primary);
  font-weight: 500;
}

.user-status {
  font-size: 0.75rem;
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius);
  
  &.active {
    background: rgba(34, 197, 94, 0.1);
    color: var(--success);
  }
  
  &:not(.active) {
    background: rgba(156, 163, 175, 0.1);
    color: var(--text-muted);
  }
}

// Mobile responsiveness
@media (max-width: 768px) {
  .admin-page {
    padding: var(--space-lg);
  }
  
  .admin-grid {
    grid-template-columns: 1fr;
    gap: var(--space-lg);
  }
  
  .card-actions {
    flex-direction: column;
  }
  
  .user-item {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-md);
  }
}
</style> 
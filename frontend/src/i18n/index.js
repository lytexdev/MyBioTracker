import { createI18n } from 'vue-i18n'
import de from './locales/de.json'
import en from './locales/en.json'

// Verfügbare Sprachen
export const availableLocales = [
  { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
  { code: 'en', name: 'English', flag: '🇺🇸' }
]

// Standard-Sprache aus localStorage oder fallback auf Deutsch
const getDefaultLocale = () => {
  const stored = localStorage.getItem('mybiote-locale')
  if (stored && availableLocales.find(l => l.code === stored)) {
    return stored
  }
  
  // Browser-Sprache erkennen
  const browserLang = navigator.language.split('-')[0]
  if (availableLocales.find(l => l.code === browserLang)) {
    return browserLang
  }
  
  return 'de' // Default zu Deutsch
}

// i18n-Instanz erstellen
const i18n = createI18n({
  legacy: false, // Composition API verwenden
  locale: getDefaultLocale(),
  fallbackLocale: 'de',
  globalInjection: true,
  messages: {
    de,
    en
  }
})

// Sprache wechseln Funktion
export const setLocale = (locale) => {
  if (availableLocales.find(l => l.code === locale)) {
    i18n.global.locale.value = locale
    localStorage.setItem('mybiote-locale', locale)
    document.documentElement.lang = locale
  }
}

// Aktuelle Sprache abrufen
export const getCurrentLocale = () => {
  return i18n.global.locale.value
}

// i18n Instanz exportieren
export default i18n 
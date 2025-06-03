import axios from 'axios'

const API_BASE = '/api/nutrition'

class NutritionService {
  async searchFoods(query, limit = 20) {
    const response = await axios.get(`${API_BASE}/foods/search`, {
      params: { q: query, limit }
    })
    return response.data
  }

  async getFoodByBarcode(barcode) {
    const response = await axios.get(`${API_BASE}/foods/barcode/${barcode}`)
    return response.data
  }

  async scanBarcode(imageFile) {
    const formData = new FormData()
    formData.append('file', imageFile)
    
    const response = await axios.post(`${API_BASE}/foods/scan-barcode`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  }

  async createFood(foodData) {
    const response = await axios.post(`${API_BASE}/foods`, foodData)
    return response.data
  }

  async createMeal(mealData) {
    const response = await axios.post(`${API_BASE}/meals`, mealData)
    return response.data
  }

  async getMeals(dateFrom = null, dateTo = null) {
    const params = {}
    if (dateFrom) params.date_from = dateFrom
    if (dateTo) params.date_to = dateTo

    const response = await axios.get(`${API_BASE}/meals`, { params })
    return response.data
  }

  async createNutritionEntry(entryData) {
    const response = await axios.post(`${API_BASE}/entries`, entryData)
    return response.data
  }

  async getDailyNutritionSummary(date) {
    const response = await axios.get(`${API_BASE}/summary/${date}`)
    return response.data
  }
}

export const nutritionService = new NutritionService() 
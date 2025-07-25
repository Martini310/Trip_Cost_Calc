// API Configuration
// Update this URL when deploying to production
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001'

export const API_ENDPOINTS = {
  calculateTrip: `${API_BASE_URL}/calculate-trip`,
  mapImage: `${API_BASE_URL}/map-image`,
  health: `${API_BASE_URL}/health`,
} 
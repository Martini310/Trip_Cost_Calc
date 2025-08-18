// API Configuration
// Update this URL when deploying to production
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001'

export const API_ENDPOINTS = {
  geocode: `${API_BASE_URL}/geocode`,
  calculateTrip: `${API_BASE_URL}/calculate-trip`,
  mapImage: `${API_BASE_URL}/map-image`,
  health: `${API_BASE_URL}/health`,
}

// Google Maps API Key for reverse geocoding
export const GOOGLE_MAPS_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY

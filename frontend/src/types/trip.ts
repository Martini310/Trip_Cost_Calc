export interface TripResult {
  trip_cost: number
  distance_text: string
  distance_value: number
  duration_text: string
  duration_value: number
  price: number
  weather_description: [string, number]
  origin: string
  destination: string
  fuel_type: string | number
  consumption: number
  map_url: string
}

export interface TripData {
  origin: string
  destination: string
  fuelType: string | number
  consumption: number
  userLocation?: { lat: number; lng: number }
}

export type FuelType = 'PB95' | 'PB98' | 'ON' | 'ON+' | 'LPG' 
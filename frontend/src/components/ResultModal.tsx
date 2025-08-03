'use client'

import { TripResult } from '@/types/trip'
import { useState } from 'react'
import { API_ENDPOINTS } from '@/config/api'

interface ResultModalProps {
  result: TripResult
  onClose: () => void
}

export default function ResultModal({ result, onClose }: ResultModalProps) {
  const [mapLoaded, setMapLoaded] = useState(false)
  const [mapError, setMapError] = useState(false)

  const formatDuration = (duration: string) => {
    return duration.replace('hours', 'godz.').replace('mins', 'min.')
  }

  const handleMapLoad = () => {
    setMapLoaded(true)
  }

  const handleMapError = () => {
    setMapError(true)
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Szczegóły podróży</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="space-y-6">
            {/* Route Information */}
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="flex items-center space-x-3 mb-3">
                <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                <span className="font-medium text-gray-900">{result.origin}</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <span className="font-medium text-gray-900">{result.destination}</span>
              </div>
            </div>

            {/* Cost Information */}
            <div className="bg-green-50 rounded-lg p-4">
              <div className="text-center">
                <p className="text-sm text-gray-600 mb-1">Całkowity Koszt</p>
                <p className="text-3xl font-bold text-green-600">
                  {result.trip_cost.toFixed(2)} zł
                </p>
              </div>
            </div>

            {/* Trip Details */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-50 rounded-lg p-4 text-center">
                <p className="text-sm text-gray-600 mb-1">Odległość</p>
                <p className="text-xl font-semibold text-gray-900">
                  {(result.distance_value / 1000).toFixed(1)} km
                </p>
              </div>
              <div className="bg-gray-50 rounded-lg p-4 text-center">
                <div className="text-sm text-gray-600 mb-1">Czas podróży</div>
                <p className="text-xl font-semibold text-gray-900">
                  {formatDuration(result.duration_text)}
                </p>
              </div>
            </div>

            {/* Fuel Information */}
            <div className="bg-yellow-50 rounded-lg p-4">
              <div className="text-center">
                <p className="text-sm text-gray-600 mb-1">Cena paliwa</p>
                <p className="text-xl font-semibold text-yellow-700">
                  {result.price} zł/l
                </p>
                <p className="text-sm text-gray-600 mt-1">
                  {typeof result.fuel_type === 'string' ? result.fuel_type : 'Cena Własna'}
                </p>
              </div>
            </div>

            {/* Weather Information */}
            <div className="bg-indigo-50 rounded-lg p-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center">
                  <p className="text-sm text-gray-600 mb-1">Pogoda</p>
                  <p className="text-sm font-medium text-gray-900 capitalize">
                    {result.weather_description[0]}
                  </p>
                </div>
                <div className="text-center">
                  <p className="text-sm text-gray-600 mb-1">Widoczność</p>
                  <p className="text-sm font-medium text-gray-900">
                    {result.weather_description[1]}m
                  </p>
                </div>
              </div>
            </div>

            {/* Map Display */}
            <div className="bg-gray-100 rounded-lg p-4">
              <div className="text-center mb-3">
                <p className="text-sm font-medium text-gray-700">Mapa Trasy</p>
              </div>
              <div className="relative">
                {!mapLoaded && !mapError && (
                  <div className="w-full h-32 bg-gray-200 rounded-lg flex items-center justify-center">
                    <div className="flex items-center space-x-2">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                      <p className="text-gray-500 text-sm">Ładowanie mapy...</p>
                    </div>
                  </div>
                )}
                {mapError && (
                  <div className="w-full h-32 bg-gray-200 rounded-lg flex items-center justify-center">
                    <p className="text-gray-500 text-sm">Mapa niedostępna</p>
                  </div>
                )}
                <img
                  src={`${API_ENDPOINTS.mapImage}`}
                  alt="Mapa trasy podróży"
                  className={`w-full rounded-lg ${mapLoaded ? 'block' : 'hidden'}`}
                  onLoad={handleMapLoad}
                  onError={handleMapError}
                />
              </div>
            </div>
          </div>

          {/* Close Button */}
          <button
            onClick={onClose}
            className="w-full mt-6 bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Zamknij
          </button>
        </div>
      </div>
    </div>
  )
} 
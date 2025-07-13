'use client'

import { useState } from 'react'
import { FuelType } from '@/types/trip'

interface TripCalculatorProps {
  onCalculate: (data: {
    origin: string
    destination: string
    fuelType: string | number
    consumption: number
  }) => void
  isLoading: boolean
}

export default function TripCalculator({ onCalculate, isLoading }: TripCalculatorProps) {
  const [origin, setOrigin] = useState('')
  const [destination, setDestination] = useState('')
  const [fuelMode, setFuelMode] = useState<'type' | 'price'>('type')
  const [fuelType, setFuelType] = useState<FuelType>('PB95')
  const [fuelPrice, setFuelPrice] = useState(5.0)
  const [consumption, setConsumption] = useState(7.0)

  const fuelTypes: { value: FuelType; label: string }[] = [
    { value: 'PB95', label: 'PB95' },
    { value: 'PB98', label: 'PB98' },
    { value: 'ON', label: 'Diesel' },
    { value: 'ON+', label: 'Diesel+' },
    { value: 'LPG', label: 'LPG' },
  ]

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!origin.trim() || !destination.trim()) {
      return
    }

    const fuelValue = fuelMode === 'type' ? fuelType : fuelPrice
    
    onCalculate({
      origin: origin.trim(),
      destination: destination.trim(),
      fuelType: fuelValue,
      consumption,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Origin */}
      <div>
        <label htmlFor="origin" className="block text-sm font-medium text-gray-700 mb-2">
          Start Address
        </label>
        <input
          type="text"
          id="origin"
          value={origin}
          onChange={(e) => setOrigin(e.target.value)}
          placeholder="Enter start location"
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          required
        />
      </div>

      {/* Destination */}
      <div>
        <label htmlFor="destination" className="block text-sm font-medium text-gray-700 mb-2">
          Destination
        </label>
        <input
          type="text"
          id="destination"
          value={destination}
          onChange={(e) => setDestination(e.target.value)}
          placeholder="Enter destination"
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          required
        />
      </div>

      {/* Fuel Consumption */}
      <div>
        <label htmlFor="consumption" className="block text-sm font-medium text-gray-700 mb-2">
          Fuel Consumption (L/100km): {consumption.toFixed(1)}
        </label>
        <input
          type="range"
          id="consumption"
          min="1"
          max="20"
          step="0.1"
          value={consumption}
          onChange={(e) => setConsumption(parseFloat(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
        />
      </div>

      {/* Fuel Type/Price Selection */}
      <div className="space-y-4">
        <div className="flex space-x-4">
          <label className="flex items-center">
            <input
              type="radio"
              name="fuelMode"
              value="type"
              checked={fuelMode === 'type'}
              onChange={(e) => setFuelMode(e.target.value as 'type' | 'price')}
              className="mr-2"
            />
            <span className="text-sm font-medium text-gray-700">Select Fuel Type</span>
          </label>
          <label className="flex items-center">
            <input
              type="radio"
              name="fuelMode"
              value="price"
              checked={fuelMode === 'price'}
              onChange={(e) => setFuelMode(e.target.value as 'type' | 'price')}
              className="mr-2"
            />
            <span className="text-sm font-medium text-gray-700">Set Price</span>
          </label>
        </div>

        {fuelMode === 'type' ? (
          <div className="grid grid-cols-2 gap-2">
            {fuelTypes.map((type) => (
              <button
                key={type.value}
                type="button"
                onClick={() => setFuelType(type.value)}
                className={`px-4 py-2 rounded-lg border text-sm font-medium transition-colors ${
                  fuelType === type.value
                    ? 'bg-blue-500 text-white border-blue-500'
                    : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                }`}
              >
                {type.label}
              </button>
            ))}
          </div>
        ) : (
          <div>
            <label htmlFor="fuelPrice" className="block text-sm font-medium text-gray-700 mb-2">
              Fuel Price (PLN/L): {fuelPrice.toFixed(2)}
            </label>
            <input
              type="range"
              id="fuelPrice"
              min="1"
              max="10"
              step="0.01"
              value={fuelPrice}
              onChange={(e) => setFuelPrice(parseFloat(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
          </div>
        )}
      </div>

      {/* Calculate Button */}
      <button
        type="submit"
        disabled={isLoading || !origin.trim() || !destination.trim()}
        className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {isLoading ? (
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            Calculating...
          </div>
        ) : (
          'Calculate Trip Cost'
        )}
      </button>
    </form>
  )
} 
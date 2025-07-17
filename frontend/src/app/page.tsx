'use client'

import { useState } from 'react'
import TripCalculator from '@/components/TripCalculator'
import ResultModal from '@/components/ResultModal'
import { TripResult } from '@/types/trip'

export default function Home() {
  const [result, setResult] = useState<TripResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleCalculate = async (tripData: {
    origin: string
    destination: string
    fuelType: string | number
    consumption: number
  }) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await fetch('/api/calculate-trip', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(tripData),
      })

      if (!response.ok) {
        throw new Error('Failed to calculate trip cost')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-md mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Trip Cost Calculator
            </h1>
            <p className="text-gray-600">
              Oblicz koszt podróży na podstawie aktualnych cen paliwa
            </p>
          </div>

          <div className="bg-white rounded-2xl shadow-xl p-6">
            <TripCalculator 
              onCalculate={handleCalculate}
              isLoading={isLoading}
            />
          </div>

          {error && (
            <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}
        </div>
      </div>

      {result && (
        <ResultModal 
          result={result} 
          onClose={() => setResult(null)}
        />
      )}
    </div>
  )
}

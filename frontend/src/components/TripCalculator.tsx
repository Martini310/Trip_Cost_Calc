'use client'

import { useState, useEffect } from 'react'
import { FuelType } from '@/types/trip'
import { GOOGLE_MAPS_API_KEY } from '@/config/api'
import GooglePlaceAutocomplete from '@/components/LocationInput'

interface TripCalculatorProps {
  onCalculate: (data: {
    origin: string
    destination: string
    fuelType: string | number
    consumption: number
    userLocation?: { lat: number; lng: number }
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
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | null>(null)
  const [locationPermission, setLocationPermission] = useState<'granted' | 'denied' | 'pending'>('pending')
  const [isGettingAddress, setIsGettingAddress] = useState(false)

  const fuelTypes: { value: FuelType; label: string }[] = [
    { value: 'PB95', label: 'PB95' },
    { value: 'PB98', label: 'PB98' },
    { value: 'ON', label: 'Diesel' },
    { value: 'ON+', label: 'Diesel+' },
    { value: 'LPG', label: 'LPG' },
  ]

  // Get user location on component mount
  useEffect(() => {
    const getUserLocation = () => {
      if (!navigator.geolocation) {
        console.log('Geolocation is not supported by this browser')
        setLocationPermission('denied')
        return
      }

      setLocationPermission('pending')
      
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          })
          setLocationPermission('granted')
          console.log('User location obtained:', position.coords)
        },
        (error) => {
          console.log('Error getting location:', error)
          setLocationPermission('denied')
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 60000
        }
      )
    }

    getUserLocation()
  }, [])

  // Function to get address from coordinates
  const getAddressFromCoordinates = async (lat: number, lng: number): Promise<string> => {
    if (!GOOGLE_MAPS_API_KEY) {
      console.error('Google Maps API key not found')
      return ''
    }

    try {
      const response = await fetch(
        `https://maps.googleapis.com/maps/api/geocode/json?latlng=${lat},${lng}&region=pl&key=${GOOGLE_MAPS_API_KEY}`
      )
      const data = await response.json()
      
      if (data.status === 'OK' && data.results.length > 0) {
        return data.results[0].formatted_address
      }
      return ''
    } catch (error) {
      console.error('Error getting address:', error)
      return ''
    }
  }

  // Function to get current address
  const getCurrentAddress = async () => {
    if (!userLocation) {
      alert('Lokalizacja niedostępna. Proszę zezwolić na dostęp do lokalizacji.')
      return
    }

    if (!GOOGLE_MAPS_API_KEY) {
      alert('Klucz API Google Maps nie jest skonfigurowany. Proszę skontaktować się z pomocą techniczną.')
      return
    }

    function updateGMPAutocompleteValue(id: string, address: string) {
      const el = document.getElementById(id) as HTMLElement | null;
      if (el && el.shadowRoot) {
        const input = el.shadowRoot.querySelector('input') as HTMLInputElement | null;
        if (input) {
          input.value = address;
          input.dispatchEvent(new Event('input', { bubbles: true }));
          input.dispatchEvent(new Event('change', { bubbles: true }));
        }
        el.blur()
        setTimeout(() => {
          document.body.click(); // symulujemy kliknięcie poza polem
        }, 50);
      }
    }

    setIsGettingAddress(true)
    try {
      const address = await getAddressFromCoordinates(userLocation.lat, userLocation.lng)
      if (address) {
        setOrigin(address)
        updateGMPAutocompleteValue('origin', address);

      } else {
        alert('Nie można pobrać aktualnego adresu. Proszę wprowadzić go ręcznie.')
      }
    } catch (error) {
      console.error('Error getting current address:', error)
      alert('Błąd podczas pobierania aktualnego adresu. Proszę wprowadzić go ręcznie.')
    } finally {
      setIsGettingAddress(false)
    }
  }

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
      userLocation: userLocation || undefined
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Location Status */}
      <div className="bg-blue-50 rounded-lg p-3">
        <div className="flex items-center space-x-2">
          <div className={`m-1 p-1 w-3 h-3 rounded-full ${
            locationPermission === 'granted' ? 'bg-green-500' :
            locationPermission === 'denied' ? 'bg-red-500' : 'bg-yellow-500'
          }`}></div>
          <span className="text-xs text-gray-700">
            {locationPermission === 'granted' ? 'Dostęp do lokalizacji przyznany - ceny paliwa będą oparte na średniej cenie paliwa w Twoim województwie' :
             locationPermission === 'denied' ? 'Dostęp do lokalizacji odmówiony - używanie średniej krajowej ceny paliwa' :
             'Żądanie dostępu do lokalizacji...'}
          </span>
        </div>
      </div>

      {/* Origin with Auto-fill Button */}
      <div>
        <label htmlFor="origin" className="block text-sm font-medium text-gray-700 mb-2">
          Skąd ruszasz
        </label>
        <div className="flex space-x-2">
          <GooglePlaceAutocomplete
            id="origin"
            onSelect={setOrigin}
          />
        </div>
        <div className='flex space-x-2' >
          <button
            type="button"
            onClick={getCurrentAddress}
            disabled={locationPermission !== 'granted' || isGettingAddress}
            className="flex-1 px-3 py-2 my-2 text-xs bg-green-600 text-white justify-center rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
          >
            {isGettingAddress ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Pobieram...</span>
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span>Moja Lokalizacja</span>
              </>
            )}
          </button>
          {locationPermission === 'denied' && (
            <p className="flex-2 py-2 text-xs text-gray-500 mt-1">
              Włącz dostęp do lokalizacji, aby automatycznie wypełnić aktualny adres
            </p>
          )}
        </div>
      </div>

      {/* Destination */}
      <div>
        <label htmlFor="destination" className="block text-sm font-medium text-gray-700 mb-2">
          Dokąd jedziesz
        </label>
      <GooglePlaceAutocomplete
        id="destination"
        onSelect={setDestination}
      />
      </div>

      {/* Fuel Consumption */}
      <div>
        <label htmlFor="consumption" className="block text-sm font-medium text-gray-700 mb-2">
          Zużycie paliwa (L/100km): {consumption.toFixed(1)}
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
            <span className="text-sm font-medium text-gray-700">Wybierz rodzaj paliwa</span>
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
            <span className="text-sm font-medium text-gray-700">Ustaw cenę</span>
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
              Cena (ZŁ/L): {fuelPrice.toFixed(2)}
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
            Obliczam...
          </div>
        ) : (
          'Oblicz koszt podróży'
        )}
      </button>
    </form>
  )
} 
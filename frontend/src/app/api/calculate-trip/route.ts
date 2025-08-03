import { NextRequest, NextResponse } from 'next/server'
import { API_ENDPOINTS } from '@/config/api'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { origin, destination, fuelType, consumption, userLocation } = body

    // Validate input
    if (!origin || !destination || consumption === undefined) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      )
    }

    // Call Python backend
    const response = await fetch(API_ENDPOINTS.calculateTrip, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        origin,
        destination,
        fuel_type: fuelType,
        consumption,
        user_location: userLocation, // Pass user location to backend
      }),
    })

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`)
    }

    const result = await response.json()
    return NextResponse.json(result)
  } catch (error) {
    console.error('API Error:', error)
    return NextResponse.json(
      { error: 'Failed to calculate trip cost' },
      { status: 500 }
    )
  }
} 
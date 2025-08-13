'use client'

import { useEffect } from 'react'

interface GooglePlaceAutocompleteProps {
  id: string
  placeholder?: string
  onSelect: (address: string) => void
}

export default function GooglePlaceAutocomplete({ id, placeholder, onSelect }: GooglePlaceAutocompleteProps) {
  useEffect(() => {
    const init = async () => {
      try {
        // Wait for Google Maps API to be available
        const waitForGoogle = () => {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          const google = (window as any).google
          if (!google?.maps) {
            setTimeout(waitForGoogle, 100)
            return
          }
          
          // Import Google Maps Places library
          google.maps.importLibrary('places').then(() => {
            const el = document.getElementById(id)
            if (!el) return

            el.addEventListener('gmp-select', async (event: unknown) => {
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              const customEvent = event as any
              const prediction = customEvent?.placePrediction;
              if (!prediction) {
                return;
              }
          
              const place = prediction.toPlace();
              await place.fetchFields({ fields: ['formattedAddress'] });
          
              const address = place.formattedAddress;
          
              if (address) {
                onSelect(address);
              }
            })
          }).catch((error: unknown) => {
            console.error('Error importing places library:', error)
          })
        }

        waitForGoogle()
      } catch (error) {
        console.error('Google Maps Web Component init error:', error)
      }
    }

    init()
  }, [id, onSelect])

  return (
    // @ts-expect-error - gmp-place-autocomplete is a custom element not recognized by TypeScript
    <gmp-place-autocomplete
      id={id}
      placeholder={placeholder || 'Wpisz lokalizację'}
      includedRegionCodes={['pl']}
      style={{
        backgroundColor:"white",
        border:"1px solid gray",
        borderRadius:"8px"
      }}
      className="w-full"
    />
  )
}


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
        // Import Google Maps Places library
        await google.maps.importLibrary('places')

        const el = document.getElementById(id)
        if (!el) return

        el.addEventListener('gmp-select', async ( event: any) => {
            const prediction = event?.placePrediction;
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
      } catch (e) {
        console.error('Google Maps Web Component init error:', e)
      }
    }

    init()
  }, [id, onSelect])

  return (
    // @ts-ignore
    <gmp-place-autocomplete
      id={id}
      placeholder={placeholder || 'Wpisz lokalizację'}
      includedRegionCodes={['pl']}
      style={{
        backgroundColor:"white",
        border:"1px solid gray",
        borderRadius:"8px"
      }}
      class="w-full"
    />
  )
}

'use client'

import { useEffect } from 'react'

interface GooglePlaceAutocompleteProps {
  id: string
  placeholder?: string
  onSelect: (address: string) => void
}

export default function GooglePlaceAutocomplete({ id, onSelect }: GooglePlaceAutocompleteProps) {
  useEffect(() => {
    const init = async () => {
      try {
        // Import Google Maps Places library
        await google.maps.importLibrary('places')

        const el = document.getElementById(id)
        if (!el) return

        el.addEventListener('gmp-select', async ( event: Event) => {
            const customEvent = event as CustomEvent;
            const prediction = (customEvent as any)?.placePrediction;

            if (!prediction) {
              return;
            }
        
            const place = prediction.toPlace();
            await place.fetchFields({ fields: ['formattedAddress'] });
        
            const address = place.formattedAddress;
            console.log(address)
        
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
    // @ts-expect-error: Web Component is not typed
    <gmp-place-autocomplete
      id={id}
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

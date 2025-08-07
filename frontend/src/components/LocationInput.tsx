'use client'

import { useEffect } from 'react'

interface Props {
    id: string
    onSelect: (address: string) => void
}

export default function GooglePlaceAutocomplete({ id, onSelect }: Props) {
    useEffect(() => {
        const waitForGoogle = () => {
            if (typeof window === 'undefined' || !(window as any).google?.maps) {
                setTimeout(waitForGoogle, 100)
                return
            }

            const el = document.getElementById(id)
            if (!el) return

            el.addEventListener('gmp-select', async (event: unknown) => {
                const customEvent = event as CustomEvent
                const prediction = (customEvent as any)?.placePrediction
                if (!prediction) return

                const place = prediction.toPlace()
                await place.fetchFields({ fields: ['formattedAddress'] })

                const address = place.formattedAddress
                if (address) {
                    onSelect(address)
                }
            })
        }

        waitForGoogle()
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
      className="w-full"
    />
  )
}

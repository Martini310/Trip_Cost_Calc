# Trip Cost Calculator PWA

A modern Progressive Web App (PWA) for calculating trip costs based on fuel prices and distance. Built with Next.js frontend and Python Flask backend.

## Features

- **Progressive Web App**: Installable on mobile and desktop devices
- **Real-time Fuel Prices**: Automatic fuel price detection based on location
- **Route Calculation**: Distance and duration calculation using Google Maps API
- **Interactive Map**: Generated route map with start and destination markers
- **Weather Information**: Current weather conditions along the route
- **Modern UI**: Beautiful, responsive design with Tailwind CSS
- **Offline Capable**: Works offline with service worker caching

## Technology Stack

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **PWA**: Progressive Web App capabilities
- **next-pwa**: PWA configuration and service worker

### Backend
- **Python**: Core calculation logic
- **Flask**: REST API server
- **Google Maps API**: Route calculation, geocoding, and map generation
- **OpenWeatherMap API**: Weather data
- **Beautiful Soup**: Web scraping for fuel prices

## Quick Start

### Prerequisites

1. **Node.js** (v18 or higher)
2. **Python** (v3.8 or higher)
3. **Google Maps API Key**
4. **OpenWeatherMap API Key**

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Trip_Cost_Calc
   ```

2. **Install dependencies**
   ```bash
   npm run install:all
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   API_KEY=your_google_maps_api_key
   WEATHER_API=your_openweathermap_api_key
   ```

4. **Start the development servers**
   ```bash
   npm run dev
   ```

This will start both the frontend (Next.js) on `http://localhost:3000` and the backend (Flask) on `http://localhost:5001`.

## API Endpoints

### POST /api/calculate-trip
Calculate trip cost and details.

**Request Body:**
```json
{
  "origin": "Warsaw, Poland",
  "destination": "Krakow, Poland",
  "fuel_type": "PB95",
  "consumption": 7.5
}
```

**Response:**
```json
{
  "trip_cost": 45.67,
  "distance_text": "295 km",
  "distance_value": 295000,
  "duration_text": "3 hours 15 mins",
  "duration_value": 11700,
  "price": 6.23,
  "weather_description": ["partly cloudy", 10000],
  "origin": "Warsaw, Poland",
  "destination": "Krakow, Poland",
  "fuel_type": "PB95",
  "consumption": 7.5,
  "map_url": "/map-image"
}
```

### GET /map-image
Serve the generated route map image.

## PWA Features

### Installation
- **Android**: Add to home screen via browser menu
- **iOS**: Add to home screen via Safari share button
- **Desktop**: Install via browser address bar

### Offline Support
- Service worker caches static assets
- App shell available offline
- API calls cached for offline viewing

### Map Display
- **Interactive Route Map**: Shows the calculated route with start and destination markers
- **Real-time Generation**: Map is generated on-demand for each trip calculation
- **Responsive Design**: Map adapts to different screen sizes
- **Loading States**: Smooth loading animation while map generates

## Development

### Frontend Development
```bash
cd frontend
npm run dev
```

### Backend Development
```bash
python api_server.py
```

### Building for Production
```bash
npm run build
npm start
```

## Project Structure

```
Trip_Cost_Calc/
├── frontend/                 # Next.js PWA frontend
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # React components
│   │   └── types/           # TypeScript types
│   ├── public/              # Static assets
│   └── package.json
├── backend.py               # Original Python backend logic
├── api_server.py            # Flask API server
├── main.py                  # Original Kivy app
├── package.json             # Root package.json
└── README_PWA.md           # This file
```

## Configuration

### PWA Configuration
- **Manifest**: `frontend/public/manifest.json`
- **Service Worker**: Auto-generated by next-pwa
- **Icons**: Place in `frontend/public/`

### Environment Variables
- `API_KEY`: Google Maps API key
- `WEATHER_API`: OpenWeatherMap API key
- `PORT`: Backend server port (default: 5001)

## Deployment

### Frontend (Vercel/Netlify)
```bash
cd frontend
npm run build
```

### Backend (Heroku/Railway)
```bash
pip install -r requirements.txt
python api_server.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub. 
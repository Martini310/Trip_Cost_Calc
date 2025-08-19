# Trip Cost Calculator - PWA & Deployment Guide

This repository contains the documentation for the **Trip Cost Calculator**, a modern Progressive Web App (PWA) built with a Next.js frontend and a Python Flask backend. It also includes details about the original Kivy application and comprehensive deployment instructions.

---

## 🚀 About the Project

The Trip Cost Calculator is designed to help users estimate the cost of their car trips. It leverages real-time data and powerful APIs to provide accurate calculations and route information.

### Key Highlights:

*   **Modern PWA**: Installable on various devices, offering a native-like experience.
*   **Comprehensive Calculation**: Provides trip cost, distance, duration, fuel price, weather, and route maps.
*   **Dockerized Backend**: Ready for deployment on platforms like mikr.us.
*   **Vercel Frontend**: Easy deployment for the Next.js PWA.

---

## ✨ Features

The application offers a rich set of features for trip planning:

- :white_check_mark: **Progressive Web App (PWA)**: Installable on mobile and desktop devices.
- :white_check_mark: **Real-time Fuel Prices**: Automatic fuel price detection based on location (via web scraping and geolocation) or manual input.
- :white_check_mark: **Location Autocomplete**: Start typing and select location from hints.
- :white_check_mark: **Auto-fill User Location**: Filling user location is a one-click.
- :white_check_mark: **Route Calculation**: Distance and duration calculation using Google Maps API.
- :white_check_mark: **Interactive Map**: Displays the calculated route with start and destination markers.
- :white_check_mark: **Weather Information**: Current weather conditions along the route obtained from OpenWeatherMap API.
- :white_check_mark: **Modern UI**: Beautiful, responsive design powered by Tailwind CSS.
- :white_check_mark: **Cost Estimation**: Calculates trip cost based on fuel consumption and price.

---

## 🛠️ Technology Stack

### Progressive Web App (PWA)

*   **Frontend**:
    *   **Next.js 14**: React framework with App Router.
    *   **TypeScript**: For type-safe development.
    *   **Tailwind CSS**: Utility-first CSS framework for styling.
    *   **PWA**: Progressive Web App capabilities.
    *   **next-pwa**: PWA configuration and service worker management.
*   **Backend**:
    *   **Python**: Core calculation logic.
    *   **Flask**: Lightweight REST API server.
    *   **Google Maps API**: Route calculation, geocoding, and map generation.
    *   **OpenWeatherMap API**: Weather data retrieval.
    *   **Beautiful Soup (bs4)**: Web scraping for fuel prices.

### Original Kivy Application (Legacy)

*   **Core**:
    *   **Python 3.10.5**
    *   **Kivy 2.1.0**: GUI framework.
    *   **Dotenv 0.21.0**: For managing environment variables.
    *   **Requests 2.28.1**: For making HTTP requests.
    *   **Beautiful Soup 4.11.0**: For web scraping.
*   **External APIs**:
    *   **Google Maps API**: For route and map data.
    *   **OpenWeatherMap API**: For weather data.

---

## 🏁 Quick Start (PWA Version)

Follow these steps to get the PWA version running locally.

### Prerequisites

1.  **Node.js**: Version 18 or higher.
2.  **Python**: Version 3.8 or higher.
3.  **Google Maps API Key**: Required for route calculation, geocoding, and map generation.
4.  **OpenWeatherMap API Key**: Required for fetching weather data.

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Martini310/Trip_Cost_Calc.git
    cd Trip_Cost_Calc
    ```

2.  **Install dependencies**:
    ```bash
    npm run install:all
    ```
    *(This command installs both frontend and backend dependencies.)*

3.  **Set up environment variables**:
    Create a `.env` file in the root directory of the project:
    ```env
    # .env file
    API_KEY=your_google_maps_api_key
    WEATHER_API=your_openweathermap_api_key
    ```

    Create a `.env.local` file in the `/frontend` directory of the project:
    ```env
    # .env.local file
    NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
    ```
    *Note: For the frontend's "My Location" feature, there should be the Google Maps API Key configured as `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY` in the frontend's environment setup or Vercel deployment settings.*

4.  **Start the development servers**:
    ```bash
    npm run dev
    ```
    This command starts both the Next.js frontend (typically on `http://localhost:3000`) and the Flask backend (typically on `http://localhost:5001`).

---

## 📈 API Endpoints (Backend)

The Flask backend exposes the following endpoints:

### `POST /calculate-trip`

Calculates trip cost and details based on provided parameters.

**Request Body Example:**
```json
{
  "origin": "Warsaw, Poland",
  "destination": "Krakow, Poland",
  "fuel_type": "PB95",
  "consumption": 7.5
}
```

**Response Example:**
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

### `GET /map-image`

Serves the generated route map image used in the response of `/calculate-trip`.

### `GET /geocode`
Performs reverse geocoding to convert geographic coordinates (latitude and longitude) into a human-readable address. This is primarily used by the "My Location" feature on the frontend.

**Query Parameters:**
```
lat (required): The latitude of the location.
lng (required): The longitude of the location.
```

**Example Request:**
```
/geocode?lat=52.2297&lng=21.0122
```
**Response Example:**

*Returns the JSON response directly from the Google Maps Geocoding API.*
```
{
  "results": [
    {
      "formatted_address": "Warsaw, Poland",
      ...
    }
  ],
  "status": "OK"
}
```

### `GET /health`
A simple health check endpoint used for monitoring to confirm that the API server is running and responsive.

**Response Example:**
```
{
  "status": "healthy"
}
```

### `GET /`
Root endpoint. Returns API info and available endpoints.

```
{
  "message": "Trip Cost Calculator API",
  "version": "1.0.0",
  "endpoints": {
    "geocode": "/geocode",
    "calculate_trip": "/calculate-trip",
    "map_image": "/map-image",
    "health": "/health"
  }
}
```
---

## 📱 PWA Features & Installation

### Installation Guide

*   **Android**: Open the app in a compatible browser (like Chrome), tap the menu, and select "Add to Home screen".
*   **iOS**: Open the app in Safari, tap the Share button, and select "Add to Home Screen".
*   **Desktop**: Install via the browser's address bar prompt (often shows an install icon).

### Map Display

*   **Interactive Route Map**: Visually displays the calculated route between the start and destination points.
*   **Real-time Generation**: The map image is generated dynamically for each trip calculation request.
*   **Responsive Design**: Adapts seamlessly to different screen sizes across devices.
*   **Loading States**: Includes smooth loading animations while the map is being generated.

---

## ⚙️ Project Structure

```
Trip_Cost_Calc/
├── frontend/                 # Next.js PWA frontend
│   ├── public/               # Static assets (manifest.json, icons)
│   ├── src/                  # Frontend source code
│   │   ├── app/              # App Router pages & layouts
│   │   ├── components/       # Reusable React components
│   │   └── types/            # TypeScript type definitions
│   ├── next.config.js        # Next.js configuration (incl. PWA settings)
│   └── package.json          # Frontend dependencies
├── backend.py                # Original Python backend logic
├── api_server.py             # Flask API server for PWA backend
├── main.py                   # Original Kivy app entry point
├── requirements.txt          # Backend Python dependencies
├── package.json              # Root package.json (for managing scripts like install:all)
├── .env.example              # Example environment file
├── Dockerfile                # Dockerfile to run backend
├── docker-compose.yml        # Docker-compose to deploy on server
├── VERSION.txt               # Version control
├── tripcostcalc.kv           # Kivy styling file
└── README.md                 # Main README (this file)

```

---

## 🚀 Development Setup

### Frontend Development

Navigate to the `frontend` directory and run:
```bash
cd frontend
npm run dev
```
This starts the Next.js development server.

### Backend Development

Run the Flask API server:
```bash
python api_server.py
```
This starts the Flask backend server.

### Building for Production

To build the PWA frontend for production:
```bash
npm run build
```
To start the production server (after building):
```bash
npm start
```

---

## 🔑 API Key Configuration Details

A single Google Maps API key is required for both the frontend and backend.

### Google Maps API Key

*   **Purpose**: Used for backend (directions, geocoding, static maps) and frontend (geolocation, reverse geocoding).
*   **Required APIs to Enable**:
    *   Maps JavaScript API
    *   Geocoding API
    *   Directions API
    *   Static Maps API
    *   Geolocation API


### OpenWeatherMap API Key

*   **Purpose**: Used by the backend to fetch weather data.
*   **Obtaining**: Sign up on the [OpenWeatherMap website](https://openweathermap.org/api).

---

## 🔍 Monitoring and Maintenance

### Health Checks

The backend includes a `/health` endpoint for monitoring:
```bash
curl https://your-backend/health
# Expected response: {"status": "healthy"}
```

---

## ⚠️ Troubleshooting

### Common Issues

1.  **CORS Errors**: Ensure the Flask backend is configured to handle Cross-Origin Resource Sharing (CORS) requests.
2.  **Map Images Not Loading**: Verify the backend is running, accessible, and serving the `/map-image` endpoint correctly. Check network requests in the browser's developer console. Ensure HTTPS is used consistently.
3.  **"My Location" Button Not Working**: Confirm `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY` is correctly set in environment variables. Check the browser console for specific API errors and ensure the user has granted location permissions.
4.  **API Key Issues**: Double-check that API keys are correctly set in environment variables for both backend and frontend. Ensure all required Google Maps APIs are enabled and quotas are not exceeded.
5.  **Port Conflicts**: Make sure port `5001` is available and correctly exposed in your mikr.us container configuration.

### Debug Commands

```bash
# Test backend connectivity and response
curl -v https://your-backend/health

# Test POST request to the calculation endpoint
curl -X POST https://your-backend/calculate-trip \
  -H "Content-Type: application/json" \
  -d '{"origin":"Warsaw","destination":"Krakow","fuel_type":"PB95","consumption":7.0}'

# View Docker container logs (replace 'your-container-name' if different)
docker logs trip_calculator_api
```

---

## 🔒 Security Considerations

*   **API Keys**: **Never** commit sensitive API keys directly into your code or version control. Use `.env` files and environment variables securely.
*   **HTTPS**: Always use HTTPS for communication in production environments.
*   **CORS**: Configure Cross-Origin Resource Sharing (CORS) strictly, allowing requests only from your frontend's domain.
*   **Rate Limiting**: Consider implementing rate limiting on your API endpoints to prevent abuse.
*   **Input Validation**: Sanitize and validate all user inputs on the backend to prevent security vulnerabilities.

---

## 💰 Cost Optimization

*   **Container Resources**: Monitor resource usage (CPU, Memory) and adjust container settings if necessary.
*   **API Usage**: Keep track of your Google Maps and OpenWeatherMap API usage to manage costs and stay within free tier limits where possible.
*   **Caching**: Implement caching strategies for frequently accessed data or calculations to reduce redundant API calls.
*   **CDN**: Utilize a Content Delivery Network (CDN) for serving static frontend assets if needed, though Vercel handles this efficiently by default.

---

## 🤝 Contributing

1.  Fork the repository.
2.  Create a new feature branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes and commit them (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/your-feature-name`).
5.  Submit a Pull Request.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ❓ Support & Contact

For issues, questions, or suggestions regarding the PWA version, please open an issue on GitHub.

*   **Inspiration & Sources**:
    *   Tutorial by Kacper Sieradziński on YouTube: [link](https://www.youtube.com/watch?v=Yt6TrXT-ZH4)
    *   Kivy documentation and series by Codemy.com on YouTube.
*   **Contact**: [brzezinski.ovh](https://brzezinski.ovh)
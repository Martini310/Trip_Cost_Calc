# Deployment Guide

This guide covers deploying the Trip Cost Calculator backend to mikr.us and frontend to Vercel.

## Backend Deployment (mikr.us)

### Prerequisites

1. **mikr.us Account**: Sign up at [mikr.us](https://mikr.us)
2. **Docker**: Ensure Docker is installed on your local machine
3. **Environment Variables**: Prepare your API keys

### Step 1: Prepare Environment Variables

Create a `.env` file in the root directory:

```env
API_KEY=your_google_maps_api_key
WEATHER_API=your_openweathermap_api_key
```

### Step 2: Build and Push Docker Image

```bash
# Build the Docker image
docker build -t trip-calculator-api .

# Tag the image for your mikr.us registry
docker tag trip-calculator-api your-mikrus-registry/trip-calculator-api:latest

# Push to mikr.us registry
docker push your-mikrus-registry/trip-calculator-api:latest
```

### Step 3: Deploy on mikr.us

1. **Login to mikr.us Dashboard**
2. **Create New Container**:
   - Image: `your-mikrus-registry/trip-calculator-api:latest`
   - Port: `5001`
   - Environment Variables:
     - `API_KEY`: Your Google Maps API key
     - `WEATHER_API`: Your OpenWeatherMap API key
     - `FLASK_ENV`: `production`
     - `HOST`: `0.0.0.0`
     - `PORT`: `5001`

3. **Configure Networking**:
   - Expose port 5001
   - Enable public access
   - Set up SSL certificate (recommended)

### Step 4: Test Backend Deployment

```bash
# Test health endpoint
curl https://your-mikrus-domain.com/health

# Test API endpoint
curl -X POST https://your-mikrus-domain.com/calculate-trip \
  -H "Content-Type: application/json" \
  -d '{"origin":"Warsaw","destination":"Krakow","fuel_type":"PB95","consumption":7.0}'
```

## Frontend Deployment (Vercel)

### Step 1: Prepare Frontend Configuration

1. **Update API URL**: Set the environment variable in Vercel:
   - `NEXT_PUBLIC_API_URL`: `https://your-mikrus-domain.com`

2. **Add Google Maps API Key**: For the "My Location" feature:
   - `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`: Your Google Maps API key (same as backend)

3. **Build Configuration**: Ensure `next.config.js` is properly configured for PWA

### Step 2: Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from frontend directory
cd frontend
vercel --prod
```

### Step 3: Configure Environment Variables in Vercel

1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Add:
   - `NEXT_PUBLIC_API_URL`: `https://your-mikrus-domain.com`
   - `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`: Your Google Maps API key

### Step 4: Test Complete Deployment

1. Visit your Vercel domain
2. Test trip calculation functionality
3. Test the "My Location" button to auto-fill start address
4. Verify map images are loading correctly

## Production Configuration

### Backend (mikr.us)

**Docker Compose for Production:**

```yaml
version: '3.8'

services:
  trip-calculator-api:
    image: your-mikrus-registry/trip-calculator-api:latest
    ports:
      - "5001:5001"
    environment:
      - API_KEY=${API_KEY}
      - WEATHER_API=${WEATHER_API}
      - FLASK_ENV=production
      - HOST=0.0.0.0
      - PORT=5001
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Environment Variables:**
- `API_KEY`: Google Maps API key
- `WEATHER_API`: OpenWeatherMap API key
- `FLASK_ENV`: `production`
- `HOST`: `0.0.0.0`
- `PORT`: `5001`

### Frontend (Vercel)

**Environment Variables:**
- `NEXT_PUBLIC_API_URL`: Your mikr.us backend URL
- `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`: Google Maps API key for reverse geocoding

**Build Settings:**
- Framework Preset: Next.js
- Build Command: `npm run build`
- Output Directory: `.next`
- Install Command: `npm install`

## API Key Configuration

### Google Maps API Key

You need **one Google Maps API key** that will be used for both:
1. **Backend**: Trip calculations, directions, map generation
2. **Frontend**: Reverse geocoding for "My Location" feature

**Required APIs to enable:**
- Maps JavaScript API
- Geocoding API
- Directions API
- Static Maps API
- Geolocation API

**API Key Restrictions:**
- HTTP referrers: Your Vercel domain
- API restrictions: Only the required APIs listed above

## Monitoring and Maintenance

### Health Checks

The backend includes health checks:

```bash
# Check backend health
curl https://your-mikrus-domain.com/health

# Expected response:
{"status": "healthy"}
```

### Logs

Monitor logs in mikr.us dashboard:
- Application logs
- Error logs
- Performance metrics

### SSL Configuration

Ensure SSL is enabled on mikr.us:
1. Go to your container settings
2. Enable SSL certificate
3. Update frontend API URL to use HTTPS

## Troubleshooting

### Common Issues

1. **CORS Errors**:
   - Ensure CORS is properly configured in backend
   - Check that frontend URL is allowed

2. **Map Images Not Loading**:
   - Verify backend is accessible
   - Check map file permissions
   - Ensure HTTPS is used for production

3. **"My Location" Button Not Working**:
   - Verify `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY` is set in Vercel
   - Check browser console for API errors
   - Ensure user grants location permission

4. **API Key Issues**:
   - Verify API keys are correctly set in environment variables
   - Check API key quotas and billing
   - Ensure all required APIs are enabled

5. **Port Conflicts**:
   - Ensure port 5001 is available and exposed
   - Check mikr.us container configuration

### Debug Commands

```bash
# Test backend connectivity
curl -v https://your-mikrus-domain.com/health

# Test API endpoint
curl -X POST https://your-mikrus-domain.com/calculate-trip \
  -H "Content-Type: application/json" \
  -d '{"origin":"Warsaw","destination":"Krakow","fuel_type":"PB95","consumption":7.0}'

# Check Docker logs
docker logs your-container-name
```

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **HTTPS**: Always use HTTPS in production
3. **CORS**: Configure CORS to only allow your frontend domain
4. **Rate Limiting**: Consider implementing rate limiting for API endpoints
5. **Input Validation**: Ensure all inputs are properly validated

## Cost Optimization

1. **Container Resources**: Monitor and adjust container resources as needed
2. **API Usage**: Monitor API usage to stay within quotas
3. **Caching**: Consider implementing caching for frequently requested routes
4. **CDN**: Use CDN for static assets if needed

## Updates and Maintenance

### Backend Updates

```bash
# Build new image
docker build -t trip-calculator-api:new .

# Push to registry
docker push your-mikrus-registry/trip-calculator-api:new

# Update container on mikr.us
# Use mikr.us dashboard to update image tag
```

### Frontend Updates

```bash
# Deploy updates to Vercel
cd frontend
vercel --prod
```

## Support

For deployment issues:
1. Check mikr.us documentation
2. Review Vercel deployment logs
3. Test locally with Docker before deploying
4. Monitor application logs for errors 
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from backend import TripCost
import os
from dotenv import load_dotenv
import logging
import requests

# Load environment variables
load_dotenv()

GOOGLE_MAPS_API_KEY = os.environ.get("API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
api = os.environ.get('API_KEY')
logger.info(f'API_KEY={api}')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/geocode', methods=['GET'])
def geocode():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    if not GOOGLE_MAPS_API_KEY:
        return jsonify({"error": "Google Maps API key not configured on the server."}), 500
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&region=pl&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/calculate-trip', methods=['POST'])
def calculate_trip():
    try:
        data = request.get_json()
        
        # Extract data from request
        origin = data.get('origin')
        destination = data.get('destination')
        fuel_type = data.get('fuel_type')
        consumption = data.get('consumption')
        user_location = data.get('user_location')  # New: user location from frontend

        # Validate required fields
        if not all([origin, destination, fuel_type, consumption]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        logger.info(f"Calculating trip from {origin} to {destination}")
        if user_location:
            logger.info(f"Using user location: {user_location}")
        else:
            logger.info("No user location provided, using server location")
        # Create TripCost instance with user location
        trip = TripCost(origin, destination, fuel_type, consumption, user_location)
        # Prepare response
        result = {
            'trip_cost': trip.trip_cost,
            'distance_text': trip.distance_text,
            'distance_value': trip.distance_value,
            'duration_text': trip.duration_text,
            'duration_value': trip.duration_value,
            'price': trip.price,
            'weather_description': trip.weather_description,
            'origin': origin,
            'destination': destination,
            'fuel_type': fuel_type,
            'consumption': consumption,
            'map_url': '/map-image'
        }
        
        logger.info(f"Trip calculated successfully: {result['trip_cost']:.2f} PLN")
        return jsonify(result)
        
    except KeyError as e:
        logger.error(f"Invalid address error: {str(e)}")
        return jsonify({'error': f'Invalid address: {str(e)}'}), 400
    except Exception as e:
        logger.info(e)
        logger.error(f"Server error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/map-image')
def get_map_image():
    """Serve the generated map image"""
    try:
        return send_file('map.jpg', mimetype='image/jpeg')
    except FileNotFoundError:
        logger.error("Map file not found")
        return jsonify({'error': 'Map not found'}), 404

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'Trip Cost Calculator API',
        'version': '1.0.0',
        'endpoints': {
            'geocode': '/geocode',
            'calculate_trip': '/calculate-trip',
            'map_image': '/map-image',
            'health': '/health'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting server on {host}:{port}")
    app.run(host=host, port=port, debug=debug) 
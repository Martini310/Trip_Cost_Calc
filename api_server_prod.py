from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from backend import TripCost
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/calculate-trip', methods=['POST'])
def calculate_trip():
    try:
        data = request.get_json()
        
        # Extract data from request
        origin = data.get('origin')
        destination = data.get('destination')
        fuel_type = data.get('fuel_type')
        consumption = data.get('consumption')
        
        # Validate required fields
        if not all([origin, destination, fuel_type, consumption]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        logger.info(f"Calculating trip from {origin} to {destination}")
        
        # Create TripCost instance
        trip = TripCost(origin, destination, fuel_type, consumption)
        
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
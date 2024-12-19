from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle
import os
from flask_cors import CORS
import logging

# Import functions from utils.py
from utils import process_text, extract_entities, filter_laptops_by_entities

app = Flask(__name__)

# Configure CORS
CORS(app, resources={r"/recommend": {"origins": "http://127.0.0.1:8000"}})

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

# Path to project directory
project_dir = r'C:\xampp\htdocs\Quell-KCB\python_api'
csv_path = os.path.join(project_dir, 'laptop_price.csv')

# Read laptop data from CSV
try:
    data = pd.read_csv(csv_path, encoding='latin1')
    logging.info("CSV file successfully loaded.")
except UnicodeDecodeError:
    data = pd.read_csv(csv_path, encoding='cp1252')
    logging.info("CSV loaded using fallback encoding cp1252.")

# Load trained model
model_path = os.path.join(project_dir, 'model.pkl')
try:
    with open(model_path, 'rb') as f:
        pipeline = pickle.load(f)
    logging.info("Model successfully loaded.")
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    raise e

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend_laptop():
    try:
        # Get JSON data from request
        data_request = request.get_json()
        if not data_request:
            return jsonify({"error": "No JSON data received."}), 400

        description = data_request.get('description', '').strip()
        if not description:
            return jsonify({"error": "Description is required."}), 400

        logging.info(f"Received description: {description}")

        # Process the description using functions from utils.py
        processed_description = process_text(description)
        entities = extract_entities(description)
        logging.info(f"Extracted entities: {entities}")

        # Predict category from description using the trained model
        predicted = pipeline.predict([processed_description])[0]
        predicted_category, predicted_processor, predicted_price, _, _ = predicted

        # Use predicted results to filter laptops
        entities["price"] = predicted_price
        entities["gpu"] = predicted_processor

        # Filter laptops based on extracted entities
        filtered_laptops = filter_laptops_by_entities(entities)
        logging.info(f"Filtered laptops count: {len(filtered_laptops)}")

        # Convert the result to a list of dictionaries
        laptops = filtered_laptops.to_dict(orient='records')

        # Sort the laptops by price in descending order
        sorted_laptops = sorted(laptops, key=lambda x: x['Price_in_IDR'], reverse=True)

        # Get the top 10 laptops
        top_10_laptops = sorted_laptops[:10]

        if top_10_laptops:
            return jsonify(top_10_laptops), 200
        else:
            return jsonify({"message": "No laptops match your description."}), 200

    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True)

import webbrowser
from flask import Flask, jsonify, request
import json
from datetime import datetime

app = Flask(__name__)

# Root route
@app.route('/')
def home():
    return "Welcome to the Docker Image Tracker API! Access /api/images to see all images."

# Load the data from the saved JSON file
def load_image_data(filename='docker_images.json'):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

# Filter images by date
def filter_by_date(data, start_date=None, end_date=None):
    if start_date:
        data = [img for img in data if datetime.strptime(img['created'], "%Y-%m-%dT%H:%M:%SZ") >= start_date]
    if end_date:
        data = [img for img in data if datetime.strptime(img['created'], "%Y-%m-%dT%H:%M:%SZ") <= end_date]
    return data

# Filter images by size
def filter_by_size(data, min_size=None, max_size=None):
    if min_size:
        data = [img for img in data if img['size_bytes'] >= min_size]
    if max_size:
        data = [img for img in data if img['size_bytes'] <= max_size]
    return data

# Filter images by labels
def filter_by_labels(data, labels=None):
    if labels:
        data = [img for img in data if any(label in img['labels'] for label in labels)]
    return data

@app.route('/api/images', methods=['GET'])
def get_images():
    data = load_image_data()

    # Get filter parameters from query string
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    min_size = request.args.get('min_size', type=int)
    max_size = request.args.get('max_size', type=int)
    labels = request.args.getlist('labels')

    # Parse start and end date if they are provided
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None

    # Apply filters
    if start_date or end_date:
        data = filter_by_date(data, start_date, end_date)
    if min_size or max_size:
        data = filter_by_size(data, min_size, max_size)
    if labels:
        data = filter_by_labels(data, labels)

    return jsonify(data)

@app.route('/api/images/<string:image_tag>', methods=['GET'])
def get_image_by_tag(image_tag):
    data = load_image_data()
    filtered_data = [image for image in data if image['tag'] == image_tag]
    if filtered_data:
        return jsonify(filtered_data)
    else:
        return jsonify({"error": "Image not found"}), 404

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    
    # Run the Flask app
    app.run(debug=True)

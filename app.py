from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64

app = Flask(__name__)

cap = cv2.VideoCapture('video.mp4')
# Initialize background subtractor
bg_subtractor = cv2.createBackgroundSubtractorMOG2()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.get_json()
    image_data = data['image_data'].split(',')[1]  # Extract base64 image data
    decoded_data = base64.b64decode(image_data)
    np_data = np.fromstring(decoded_data, np.uint8)
    frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
    
    # Process frame (vehicle detection and counting)
    processed_frame = detect_vehicles(frame)
    
    # Convert processed frame back to base64
    retval, buffer = cv2.imencode('.jpg', processed_frame)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    
    return jsonify(vehicle_count=calculate_vehicle_count())

def detect_vehicles(frame):
    # Example function to detect vehicles using OpenCV
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    fg_mask = bg_subtractor.apply(blur)
    
    # Example code to detect contours and count vehicles
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return frame

def calculate_vehicle_count():
    # Example function to calculate vehicle count
    # Implement logic to count vehicles based on detection results
    return 0

if __name__ == '__main__':
    app.run(debug=True)

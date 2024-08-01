from flask import Flask, request, jsonify
from PIL import Image, ImageOps
import io
import numpy as np
import tensorflow as tf
import math
import logging
from logging.handlers import RotatingFileHandler
import time
import cv2

# Configure logging to file and console
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Set logging level to DEBUG

# File handler
file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=3)
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))

# Console handler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

app = Flask(__name__)


model_path = "model.tflite"
model = tf.lite.Interpreter(model_path=model_path)
model.allocate_tensors()


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


results = []

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'picture' not in request.files:
        logger.warning("No image file provided.")
        return jsonify({'message': 'No image provided', 'status': 'error'}), 400

    image_file = request.files['picture']
    if not image_file:
        logger.warning("Empty image file provided.")
        return jsonify({'message': 'Empty image provided', 'status': 'error'}), 400

    try:
        image = Image.open(io.BytesIO(image_file.read()))
        image = detect_and_crop_face(image)
        if image is None:
            logger.warning("No face detected in the image.")
            return jsonify({'message': 'No face detected', 'status': 'error'}), 400
        image = image.resize((128, 128))
        image_array = prepare_image(image)
        result = run_model(image_array)[0]
        results.append(result)
        if len(results) > 5:
            results.pop(0)

        log_average = calculate_log_average(results)
        percentage = log_average * 100
        decision = 'Real' if log_average > 0.5 else 'Fake'
        percentage_text = f"{percentage:.2f}% Real" if decision == 'Real' else f"{100 - percentage:.2f}% Fake"
        logger.info(f"Decision made: {decision}, Log Average: {log_average}, Percentage: {percentage_text}")
        return jsonify({'message': 'Image received', 'status': 'success', 'decision': decision, 'percentage': percentage_text})
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}", exc_info=True)
        return jsonify({'message': 'Error processing image', 'status': 'error'}), 500

def detect_and_crop_face(image):
    
    image = ImageOps.exif_transpose(image)
    
    
    image_cv = np.array(image)
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=15)
    
    if len(faces) == 0:
        logger.debug("The face was not detected and was not processed.")
        return None
    else:
        logger.debug(f"Number of faces detected: {len(faces)}")
    
    
    x, y, w, h = faces[0]
    face_image = image_cv[y:y+h, x:x+w]
    logger.debug(f"Face detected and cropped successfully: {x}, {y}, {w}, {h}")
    
    return Image.fromarray(face_image)


def prepare_image(image):
    image = image.convert('RGB')
    image_array = np.array(image).astype(np.float32) / 255.0  
    image_array = image_array[np.newaxis, :, :, :]  
    return image_array

def run_model(image_array):
    try:
        input_details = model.get_input_details()
        output_details = model.get_output_details()
        model.set_tensor(input_details[0]['index'], image_array)
        start_time = time.time()
        model.invoke()
        inference_time = time.time() - start_time
        output_data = model.get_tensor(output_details[0]['index'])
        logger.info(f"Inference Time: {inference_time:.6f} seconds")
        return output_data
    except Exception as e:
        logger.error(f"Error running model: {str(e)}", exc_info=True)
        raise

def calculate_log_average(results):
    try:
        log_sum = sum(math.log(x + 1) for x in results)
        avg_log = log_sum / len(results)
        log_average = math.exp(avg_log) - 1
        return log_average
    except Exception as e:
        logger.error(f"Error calculating log average: {str(e)}", exc_info=True)
        return 0

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)

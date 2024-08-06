# Human Face Liveness Detection

This project is a human face liveness detection system using deep learning techniques to distinguish between real and fake faces. It aims to provide fast and accurate face liveness detection, optimized for mobile applications using lightweight models.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Models](#models)
- [Results](#results)
- [Future Work](#future-work)

## Introduction

Face liveness detection is critical for ensuring the security and integrity of facial recognition systems. This project leverages deep learning to accurately identify whether a face is real or a spoof (e.g., a photo or video).

## Features

- **Real-time Liveness Detection**: Efficient and quick detection suitable for mobile applications.
- **Lightweight Models**: Uses models like MobileNet and MobileNetV2, optimized for performance on mobile devices.
- **Flask Backend**: Processes images and handles liveness detection on the server side.
- **Flutter Frontend**: Mobile application interface for capturing and displaying detection results.

## Architecture

The project consists of two main components:
1. **Frontend (Flutter)**:
    - Captures frames from the camera.
    - Sends frames to the backend for processing.
    - Displays the detection results.
2. **Backend (Flask)**:
    - Receives frames from the mobile application.
    - Preprocesses images to the required format (128x128 pixels, 3 channels).
    - Feeds images into the liveness detection model.
    - Computes the logarithmic average of the last 5 predictions.
    - Sends the decision ('fake' or 'real') back to the mobile application.

## Installation

### Prerequisites

- Python 3.9
- Flask
- TensorFlow Lite
- Flutter

### Steps

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yavuzserdarkocyigit/Liveness-Detection.git
    cd Liveness-Detection
    ```

2. **Backend Setup**

3. **Frontend Setup**

## Usage

1. Launch the backend server:
    ```bash
    cd backend
    python app.py
    ```

2. Run the Flutter application:
    ```bash
    cd frontend
    flutter run
    ```

3. Use the mobile app to capture frames and receive liveness detection results in real-time.

## Models

- **Custom Model**: Designed specifically for this project.
- **MobileNet**: Lightweight and efficient.
- **MobileNetV2**: Improved performance and accuracy.

## Results

- **Accuracy**: The custom model achieved high accuracy in distinguishing between real and fake faces in various testing environments.
- **Model Size**: Models were converted to TensorFlow Lite format and optimized for mobile applications, reducing their sizes by half.

## Future Work

- Develop faster and more reliable verification models.
- Design advanced user interfaces.
- Add additional security layers such as voice recognition.

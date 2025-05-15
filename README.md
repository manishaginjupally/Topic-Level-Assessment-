# Gesture Recognition with Kivy and Mediapipe

This project demonstrates a real-time hand gesture recognition system using **Mediapipe** and **Kivy**. The application recognizes different hand gestures and logs the information such as detected gestures, student ID, and the selected correct option, alongside capturing snapshots of the hand gestures.

## Features

- **Hand Gesture Recognition**: Using the **Mediapipe** library, the app can identify various hand gestures like:
  - "thumb up"
  - "one finger up"
  - "three fingers up"
  - "all fingers open"
  
- **Real-time Feedback**: The detected gestures are displayed on the app, and the app provides feedback on the accuracy of the recognized gestures.

- **Snapshot Capture**: The app allows you to take snapshots of recognized gestures and save them with metadata such as timestamps, student ID, and gesture log.

- **Gesture Logging**: Captures gesture information and stores it in a CSV file, logging the timestamp, detected gestures, and student IDs.

- **Cross-platform Support**: Designed to work on Windows, macOS, and Linux.

## Requirements

To run this project, you need:

- **Python 3.7+**
- **Required Libraries**:
  - OpenCV
  - Mediapipe
  - Kivy
  - Numpy
  - CSV
  - os
  - datetime

### Installing Required Libraries

If you're setting up the project on your machine, it's recommended to use a virtual environment. To do so, follow these steps:

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/manishaginjupally/sorting-visualizer.git
    ```

2. Navigate to the project directory:

    ```bash
    cd sorting-visualizer
    ```

3. Create and activate a virtual environment (recommended):

    - **Windows**:

        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

    - **macOS/Linux**:

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

4. Install the required libraries:

    ```bash
    pip install opencv-python mediapipe kivy numpy
    ```

5. Alternatively, you can create a `requirements.txt` file and install the dependencies by running:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

After setting up the project, you can run the application using:

```bash
python app.py

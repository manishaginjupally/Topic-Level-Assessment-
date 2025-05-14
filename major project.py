
import os
import cv2
import csv
import mediapipe as mp
import numpy as np
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import platform  # For OS detection

# Suppress Mediapipe logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

gesture_to_option = {
    "one_finger_up": "A",
    "thumb_up": "B",
    "three_fingers_up": "C",
    "all_fingers_open": "D",
    "unknown": "Unknown",
}

def classify_gesture(landmarks, width, height):
    lm = [(int(landmark.x * width), int(landmark.y * height)) for landmark in landmarks]

    if lm[4][1] < lm[3][1] and lm[8][1] > lm[6][1]:
        return "thumb_up"
    if lm[8][1] < lm[6][1] and all(lm[i][1] > lm[i - 2][1] for i in [12, 16, 20]):
        return "one_finger_up"
    if lm[8][1] < lm[6][1] and lm[12][1] < lm[10][1] and lm[16][1] < lm[14][1] and lm[20][1] > lm[18][1]:
        return "three_fingers_up"
    if all(lm[i][1] < lm[i - 2][1] for i in [8, 12, 16, 20]):
        return "all_fingers_open"
    return "unknown"

class GestureApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.image = Image()
        self.layout.add_widget(self.image)

        self.spinner = Spinner(text='Select Correct Option', values=('A', 'B', 'C', 'D'))
        self.layout.add_widget(self.spinner)

        self.student_id_input = TextInput(hint_text="Enter Student ID", multiline=False)
        self.layout.add_widget(self.student_id_input)

        self.capture_button = Button(text='📸 Capture Snapshot')
        self.capture_button.bind(on_press=self.capture_snapshot)
        self.layout.add_widget(self.capture_button)

        self.result_label = Label(text='Waiting for hand gesture...')
        self.layout.add_widget(self.result_label)

        # Try back camera (ID 1), fallback to front (ID 0)
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            self.result_label.text = "❌ Error: Unable to access camera"
        else:
            self.hands = mp_hands.Hands(static_image_mode=False, max_num_hands=50, min_detection_confidence=0.5)

        self.current_frame = None
        self.detected_gestures = []

        Clock.schedule_interval(self.update, 1.0 / 30.0)

        return self.layout

    def update(self, dt):
        if not self.camera.isOpened():
            return

        ret, frame = self.camera.read()
        if not ret:
            self.result_label.text = "❌ Error: Unable to capture video frame."
            return

        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.current_frame = frame.copy()
        self.detected_gestures = []

        hand_result = self.hands.process(rgb_frame)
        if hand_result.multi_hand_landmarks:
            for hand_landmarks in hand_result.multi_hand_landmarks:
                gesture = classify_gesture(hand_landmarks.landmark, w, h)
                self.detected_gestures.append(gesture)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(w, h), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture

        correct_option = self.spinner.text
        correct_responses = sum(1 for g in self.detected_gestures if gesture_to_option.get(g) == correct_option)
        total_responses = len(self.detected_gestures)
        accuracy = (correct_responses / total_responses) * 100 if total_responses > 0 else 0.0

        if self.detected_gestures:
            self.result_label.text = f"Detected Gestures: {', '.join(self.detected_gestures)} | Accuracy: {accuracy:.2f}%"
        else:
            self.result_label.text = "No hands detected."

    def capture_snapshot(self, instance):
        if self.current_frame is not None:
            save_dir = "captured_gestures"
            os.makedirs(save_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"gesture_{timestamp}.jpg"
            image_path = os.path.join(save_dir, image_filename)

            # Save image
            cv2.imwrite(image_path, self.current_frame)

            # Get student ID from input
            student_id = self.student_id_input.text.strip()

            # Save log
            csv_path = os.path.join(save_dir, "gesture_log.csv")
            file_exists = os.path.isfile(csv_path)
            with open(csv_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Timestamp", "Image Filename", "Detected Gestures", "Correct Option", "Result Info", "Student ID"])
                writer.writerow([
                    timestamp,
                    image_filename,
                    ", ".join(self.detected_gestures),
                    self.spinner.text,
                    self.result_label.text,
                    student_id
                ])

            self.result_label.text = f"📸 Saved: {image_filename} + logged"

            try:
                if platform.system() == "Windows":
                    os.startfile(save_dir)
                elif platform.system() == "Darwin":
                    os.system(f"open {save_dir}")
                else:
                    os.system(f"xdg-open {save_dir}")
            except Exception as e:
                print("Could not open folder:", e)

    def on_stop(self):
        if self.camera.isOpened():
            self.camera.release()
        self.hands.close()

if __name__ == '__main__':
    GestureApp().run()

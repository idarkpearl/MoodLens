import cv2
from fer import FER
from flask import Flask, render_template, Response, jsonify

app = Flask(__name__)

# Initialize the camera
camera = cv2.VideoCapture(0)  # 0 is usually the default webcam

# Initialize the FER detector
detector = FER()

current_frame = None
current_emotion = None
current_suggestion = None

# Define the suggestion dictionary
emotion_suggestions = {
    "happy": "Go for a walk or call a friend!",
    "sad": "Take a break, listen to music.",
    "angry": "Take deep breaths, relax.",
    "surprise": "Take a moment to collect yourself.",
    "neutral": "Everything is okay, continue as you are."
}

# Function to generate video stream with emotion detection
def generate_frames():
    global current_frame, current_emotion, current_suggestion
    while True:
        success, frame = camera.read()  # Capture frame from webcam
        if not success:
            break

        # Resize the frame to make it bigger (adjust size as needed)
        frame = cv2.resize(frame, (800, 600))  # Adjust width and height as needed

        # Detect emotion
        emotion, score = detector.top_emotion(frame)

        # Get suggestion based on the detected emotion
        suggestion = emotion_suggestions.get(emotion, "Relax and take a break.")

        # Update global variables with current frame and suggestion
        current_frame = frame
        current_emotion = emotion
        current_suggestion = suggestion

        # Add text to frame (Emotion and Suggestion)
        cv2.putText(frame, f'Emotion: {emotion}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Suggestion: {suggestion}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Convert frame to bytes to send it to the webpage
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame = buffer.tobytes()

        # Send the frame to the frontend
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/get_suggestion')
def get_suggestion():
    # Return the current suggestion as JSON data
    return jsonify({'suggestion': current_suggestion})

def generate_frames():
    global current_frame, current_emotion, current_suggestion
    while True:
        success, frame = camera.read()  # Capture frame from webcam
        if not success:
            break

        # Resize the frame to make it bigger (adjust size as needed)
        frame = cv2.resize(frame, (800, 600))  # Adjust width and height as needed

        # Detect emotion
        emotion, score = detector.top_emotion(frame)

        # Get suggestion based on the detected emotion
        suggestion = emotion_suggestions.get(emotion, "Relax and take a break.")

        # Update global variables with current frame and suggestion
        current_frame = frame
        current_emotion = emotion
        current_suggestion = suggestion

        # Add text to frame (Emotion and Suggestion)
        cv2.putText(frame, f'Emotion: {emotion}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Suggestion: {suggestion}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Convert frame to bytes to send it to the webpage
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame = buffer.tobytes()

        # Send the frame to the frontend
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


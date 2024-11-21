from flask import Flask, render_template, Response, jsonify
import cv2
from fer import FER

app = Flask(__name__)

# Initialize emotion detector
detector = FER()

# Initialize the webcam
camera = cv2.VideoCapture(0)

# Define a dictionary for emotion suggestions
emotion_suggestions = {
    "angry": "Take a deep breath and relax.",
    "disgust": "Take a moment to calm down and relax.",
    "fear": "Try doing some light exercises to ease tension.",
    "happy": "Go for a walk or call a friend!",
    "sad": "Try doing a quick workout or listening to your favorite music.",
    "surprise": "Take a deep breath and try something new!",
    "neutral": "Relax and take a break."
}

# Variable to hold the current frame for suggestion
current_frame = None
current_emotion = None
current_suggestion = None

# Function to generate video stream with emotion detection
def generate_frames():
    global current_frame, current_emotion, current_suggestion
    while True:
        success, frame = camera.read()  # Capture frame from webcam
        if not success:
            break

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

# Route to display the main page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_suggestion')
def get_suggestion():
    return jsonify({'suggestion': current_suggestion})

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        frame = cv2.resize(frame, (800, 600))
        emotion, score = detector.top_emotion(frame)
        suggestion = emotion_suggestions.get(emotion, "Relax and take a break.")
        current_frame = frame
        current_emotion = emotion
        current_suggestion = suggestion
        cv2.putText(frame, f'Emotion: {emotion}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f'Suggestion: {suggestion}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


# Route to stream video
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

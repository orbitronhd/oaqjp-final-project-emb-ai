from flask import Flask, render_template, request
from EmotionDetection import emotion_detector
import traceback
app = Flask(__name__)
@app.route('/')
def render_index_page():
    return render_template('index.html')
@app.route('/emotionDetector')
def detect_emotion():
    text_to_analyze = request.args.get('textToAnalyze')
    print(f"DEBUG: Received text for analysis: '{text_to_analyze}'")
    try:
        response_data = emotion_detector(text_to_analyze)
        print(f"DEBUG: Emotion detector returned: {response_data}")
        if response_data['dominant_emotion'] is None:
            return "Invalid text! Please try again!", 200
        else:
            anger = response_data.get('anger', 'N/A')
            disgust = response_data.get('disgust', 'N/A')
            fear = response_data.get('fear', 'N/A')
            joy = response_data.get('joy', 'N/A')
            sadness = response_data.get('sadness', 'N/A')
            dominant_emotion = response_data['dominant_emotion']

            formatted_response = (
                f"For the given statement, the system response is "
                f"'anger': {anger}, "
                f"'disgust': {disgust}, "
                f"'fear': {fear}, "
                f"'joy': {joy} and "
                f"'sadness': {sadness}. "
                f"The dominant emotion is {dominant_emotion}."
            )
            return formatted_response, 200

    except Exception as e:
        print(f"ERROR: An unexpected error occurred in /emotionDetector route: {e}")
        traceback.print_exc()
        return "Internal Server Error: Something went wrong during emotion detection.", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


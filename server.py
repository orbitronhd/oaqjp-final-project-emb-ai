from flask import Flask, render_template, request
from EmotionDetection import emotion_detector
app = Flask(__name__)
@app.route('/')
def render_index_page():
    return render_template('index.html')
@app.route('/emotionDetector')
def detect_emotion():
    text_to_analyze = request.args.get('textToAnalyze')
    response_data = emotion_detector(text_to_analyze)
    if response_data['dominant_emotion'] is None:
        return "No dominant emotion could be detected for the given text."
    else:
        anger = response_data['anger']
        disgust = response_data['disgust']
        fear = response_data['fear']
        joy = response_data['joy']
        sadness = response_data['sadness']
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
        return formatted_response
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


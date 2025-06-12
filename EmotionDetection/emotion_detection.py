import requests
import json

def emotion_detector(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyse } }
    response = requests.post(url, headers=headers, json=input_json)
    json_response = json.loads(response.text)
    
    emotions_data = json_response['emotionPredictions'][0]['emotion']
        
    anger_score = emotions_data.get('anger', 0.0)
    disgust_score = emotions_data.get('disgust', 0.0)
    fear_score = emotions_data.get('fear', 0.0)
    joy_score = emotions_data.get('joy', 0.0)
    sadness_score = emotions_data.get('sadness', 0.0)
        
    emotion_scores = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score
    }
    non_zero_emotions = {k: v for k, v in emotion_scores.items() if v > 0}
    if non_zero_emotions:
        dominant_emotion = max(non_zero_emotions, key=non_zero_emotions.get)
    else:
        dominant_emotion = None

    return {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
        'dominant_emotion': dominant_emotion
    }
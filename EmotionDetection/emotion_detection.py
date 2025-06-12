import requests
import json

def emotion_detector(text_to_analyse):
    if not text_to_analyse or text_to_analyse.strip() == '':
        print("DEBUG: Blank text received. Returning None for emotions.")
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyse } }
    try:
        response = requests.post(url, headers=headers, json=input_json)
        response.raise_for_status()
        json_response = json.loads(response.text)

        emotions_data = None
        if 'emotionPredictions' in json_response and \
           len(json_response['emotionPredictions']) > 0 and \
           'emotion' in json_response['emotionPredictions'][0]:

            emotions_data = json_response['emotionPredictions'][0]['emotion']
        else:
            print(f"DEBUG: Expected emotion structure not found in response for '{text_to_analyse}'.")
    
        anger_score = emotions_data.get('anger', 0.0) if emotions_data else 0.0
        disgust_score = emotions_data.get('disgust', 0.0) if emotions_data else 0.0
        fear_score = emotions_data.get('fear', 0.0) if emotions_data else 0.0
        joy_score = emotions_data.get('joy', 0.0) if emotions_data else 0.0
        sadness_score = emotions_data.get('sadness', 0.0) if emotions_data else 0.0
        
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

    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return {
            'anger': None, 'disgust': None, 'fear': None,
            'joy': None, 'sadness': None, 'dominant_emotion': f"API HTTP Error: {e.response.status_code}"
        }
    except requests.exceptions.ConnectionError as e:
        print(f"ERROR: Connection error occurred: {e}")
        return {
            'anger': None, 'disgust': None, 'fear': None,
            'joy': None, 'sadness': None, 'dominant_emotion': "API Connection Error"
        }
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON decoding error: {e}. Raw response: {response.text}")
        return {
            'anger': None, 'disgust': None, 'fear': None,
            'joy': None, 'sadness': None, 'dominant_emotion': "Invalid JSON from API"
        }
    except Exception as e:
        print(f"ERROR: An unexpected error occurred in emotion_detector: {e}")
        return {
            'anger': None, 'disgust': None, 'fear': None,
            'joy': None, 'sadness': None, 'dominant_emotion': "Unknown Error in Detector"
        }

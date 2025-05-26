import librosa
import numpy as np
import pickle
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
from home.predict_ults import clean_lyrics as cl
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'home', 'predict_ults', 'best_model.h5')
scaler_path = os.path.join(BASE_DIR, 'home', 'predict_ults', 'scaler.pkl')
labels_path = os.path.join(BASE_DIR, 'home', 'predict_ults', 'labels.pkl')
vectorizer_path = os.path.join(BASE_DIR, 'home', 'predict_ults', 'vectorizer.pkl')

def process_lyrics(lyrics, vectorizer):
    # print('lyrics bthg: ' + lyrics)
    cleaned_lyrics = cl.clean_lyrics(lyrics)
    # print(cleaned_lyrics)
    lyrics_tfidf = vectorizer.transform([cleaned_lyrics]).toarray()
    return lyrics_tfidf

def extract_features(file_path):
    try:
        # print('basedir goc: ' + BASE_DIR)
        # print('filepath goc: '  + file_path)
        file_path = os.path.normpath(file_path.lstrip("/\\"))
        audio_path = os.path.join(BASE_DIR, file_path)
        # print(f"Đang load file: {audio_path}")
        y, sr = librosa.load(audio_path, sr=None)  # Load file âm thanh
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr)

        return np.hstack([
            np.mean(mfccs, axis=1),  # 20 MFCC
            np.mean(chroma, axis=1), # 12 Chroma
            np.mean(mel_spec, axis=1) # 128 Mel Spectrogram
        ])
    except Exception as e:
        print(f"Lỗi xử lý {audio_path}: {e}")
        return None
    
model = tf.keras.models.load_model(model_path)

with open(vectorizer_path, 'rb') as f:
    vectorizer = pickle.load(f)
    
scaler = joblib.load(scaler_path)

labels = joblib.load(labels_path)

def predict_genre(audio_path, lyrics):
    audio_features = extract_features(audio_path)
    if audio_features is None:
        return "Lỗi khi trích xuất đặc trưng âm thanh"

    # Xử lý lyrics và vector hóa chúng
    lyrics_tfidf = process_lyrics(lyrics, vectorizer)

    combined_features = np.hstack([audio_features, lyrics_tfidf.flatten()])

    combined_features = scaler.transform([combined_features])
    combined_features = combined_features.reshape(1, 1, -1)

    prediction = model.predict(combined_features)[0] 

    # Lấy top 2 chỉ số xác suất cao nhất
    top_indices = prediction.argsort()[-2:][::-1]  # sắp xếp giảm dần

    top1_index, top2_index = top_indices
    top1_label = labels[top1_index]
    top1_conf = float(prediction[top1_index])

    top2_label = labels[top2_index]
    top2_conf = float(prediction[top2_index])

    return (top1_label, top1_conf), (top2_label, top2_conf)

def predict_genre_from_audio_and_lyrics(audio_path, lyrics):
    result = predict_genre(audio_path, lyrics)
    
    if isinstance(result, str):
        return result 
    
    (genre1, conf1), (genre2, conf2) = result
    print(f"Thể loại 1: {genre1} - Độ tự tin: {conf1:.2f}")
    print(f"Thể loại 2: {genre2} - Độ tự tin: {conf2:.2f}")
    return genre1, conf1

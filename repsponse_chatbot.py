
from Util.prep_data import prep, process_slang
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import load
import pickle
import json



# membuat tf-idf vectorizer
with open('./Kuliah-tugas-besar-bigdata/Util/tfidf_vectorizer.pkl', 'rb') as f:
   vectorizer = pickle.load(f)

# Load the model and data
lr_model = load('./Kuliah-tugas-besar-bigdata/Util/lr_nonspark.joblib')

# import data json
with open('./Kuliah-tugas-besar-bigdata/Cache/chatbot.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


def get_response(text):
    # melakukan preprocessing terhadap data inputan baru
    text_slang = process_slang(text)
    text_prep = prep(text_slang)
    
    # melakukan vectorizer terhadap data inputan baru menggunakan Tf-Idf
    text_vector = vectorizer.transform([' '.join(text_prep)])
    
    # mengambil prediksi dan probabilitas dari model
    pred = lr_model.predict(text_vector)
    pred_class = pred[0] 
    probs = lr_model.predict_proba(text_vector)[0]
    max_prob = max(probs)
    
    # respon jika probabilitas diatas 0.7
    prob_predict = "Probabilitas prediksi: " + str(max_prob)
    # batas probabilitas
    if max_prob >= 0.8:
        for intent in data['intents']:
            if intent['tag'] == pred_class:
                responses = intent['responses']
                output = responses[0]
                return output
    else:
        # respon jika probabilitas dibawah 0.8
        output = "maksud anda tidak saya mengerti, bisa dijelaskan lebih detail?"

    return output
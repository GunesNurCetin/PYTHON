from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from preprocess import clean_text
import pickle

app = Flask(__name__)

# --- ÖRNEK VERİ SETİ (Modelin öğrenmesi için) ---
# Gerçek projede binlerce satırlık CSV kullanılır.
train_texts = [
    "bu ürün harika kesinlikle tavsiye ederim", 
    "berbat bir kargo süreci çok pişmanım",
    "kalitesi beklediğimden iyi çıktı",
    "hiç beğenmedim paranıza yazık",
    "hızlı teslimat ve güzel paketleme"
]
labels = [1, 0, 1, 0, 1] # 1: Olumlu, 0: Olumsuz

# --- MODEL EĞİTİMİ ---
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform([clean_text(t) for t in train_texts])

model = LogisticRegression()
model.fit(X, labels)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    raw_comment = data.get("comment", "")
    
    if not raw_comment:
        return jsonify({"error": "Yorum boş olamaz"}), 400

    # 1. Metni temizle
    cleaned = clean_text(raw_comment)
    
    # 2. Vektöre çevir
    vec = vectorizer.transform([cleaned])
    
    # 3. Tahmin et
    prediction = model.predict(vec)[0]
    probability = model.predict_proba(vec).max()

    result = "Olumlu (Positive)" if prediction == 1 else "Olumsuz (Negative)"
    
    return jsonify({
        "comment": raw_comment,
        "sentiment": result,
        "confidence": f"%{round(probability * 100, 2)}"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)

import cv2
import datetime

# OpenCV'nin önceden eğitilmiş yüz tanıma modelini yüklüyoruz
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Kamerayı başlat (0 varsayılan kameradır)
cap = cv2.VideoCapture(0)

print("[INFO] Sistem başlatıldı. Çıkmak için 'q' tuşuna basın.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Görüntüyü gri tonlamaya çevir (AI işlemleri için daha hızlıdır)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Yüzleri tespit et
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Tespit edilen her yüz için bir dikdörtgen çiz ve zaman damgası ekle
    for (x, y, w, h) in faces:
        # Yüzü çerçevele (Mavi Renk)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Etiket ekle
        cv2.putText(frame, "Insan Yuzu Tespit Edildi", (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Sağ alt köşeye canlı saat ekle (Güvenlik kamerası efekti)
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cv2.putText(frame, timestamp, (10, frame.shape[0] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    # Görüntüyü göster
    cv2.imshow('AI Vision Engine', frame)

    # 'q' tuşuna basılırsa çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

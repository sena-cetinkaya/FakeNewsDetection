# 📰 Fake News Detection – Türkçe BERT ile Sahte Haber Tespiti

Bu proje, Türkçe haber metinleri üzerinde BERT tabanlı derin öğrenme modeli kullanarak sahte / gerçek haber tespiti yapar.

## 🚀 Özellikler

- Türkçe BERT Modeli ile haber sınıflandırma

- FastAPI REST API ile tahmin servisi

- Docker Compose ile geliştirme ve test ortamları

- SQLModel ile PostgreSQL veritabanı entegrasyonu
 
- Pytest ile API endpoint testleri

- Veri Ön İşleme: stopword temizleme, URL ve özel karakter silme, lowercase dönüşümü

## 🛠 Kullanılan Teknolojiler

- Python 3.11

- FastAPI

- Transformers (BERT)

- PyTorch

- SQLModel + PostgreSQL

- Docker & Docker Compose

- Pytest

## 📂 Proje Yapısı

FakeNewsDetection/

│── app/

│   ├── main.py

│   ├── routes.py

│   ├── model_loader.py

│   ├── db.py

│   ├── schemas.py

│── config/

│   ├── dev/.env.dev

│   ├── test/.env.test

│── data/

│   ├── bert_model/

│   ├── cleaned_data.csv

│   ├── Sahte_Haber_Analizi.xlsx

│── scripts/

│   ├── preprocess.py

│   ├── create_BERT_model.py

│   ├── upload_to_database.py

│── tests/

│   ├── test_prediction.py

│── docker-compose.dev.yml

│── docker-compose.test.yml

│── Dockerfile

│── requirements.txt

## 🔍 API Kullanımı

### 1️⃣ Haber Tahmini

POST /predict

```
{
  "news": "Bu bir örnek haber metnidir."
}
```

Response:

```
{
  "result": "gerçek"
}
```

## 🐳 Docker ile Çalıştırma

### Geliştirme Ortamı:
```
docker-compose -f docker-compose.dev.yml up --build
```

### Test Ortamı:
```
docker-compose -f docker-compose.test.yml up --build
```
## 🧪 Test Çalıştırma
```
pytest tests/
```

📃 Lisans: MIT Lisansı

👩‍💻 Geliştirici: Sena Çetinkaya

🌐 GitHub: [https://github.com/sena-cetinkaya](https://github.com/sena-cetinkaya)

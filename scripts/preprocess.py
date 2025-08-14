import pandas as pd
import re
import nltk
import string
import os

from nltk.corpus import stopwords

nltk.download("stopwords")

turkish_stopwords = stopwords.words("turkish")

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    words = text.split()
    words = [word for word in words if word not in turkish_stopwords]
    text = " ".join(words)
    return text


def main():
    data_path = "C:/Users/LENOVO/PycharmProjects/FakeNewsDetection/data/Sahte_Haber_Analizi.xlsx"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dosya bulunamadı: {data_path}")
    df = pd.read_excel(data_path)
    if 'Haberler' not in df.columns:
        raise ValueError("Excel dosyasında 'Haberler' adında bir sütun bulunmalı.")
    df["clean_text"] = df["Haberler"].astype(str).apply(clean_text)
    output_path = "../data/cleaned_data.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Temizlenmiş veri başarıyla kaydedildi: {output_path}")
    
if __name__ == "__main__":
    main()


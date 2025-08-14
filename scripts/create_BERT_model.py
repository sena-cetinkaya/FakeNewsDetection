import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from transformers import DataCollatorWithPadding
import torch

# 1. Veriyi oku
df = pd.read_csv("C:/Users/LENOVO/PycharmProjects/FakeNewsDetection/data/cleaned_data.csv")

# 2. Gerekli sütunları al ve eksik verileri temizle
df = df[['clean_text', 'Sonuc']].dropna()

# 3. Eğitim ve test verisine ayır
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df['clean_text'].tolist(),
    df['Sonuc'].tolist(),  # Zaten sayısal: 0 veya 1
    test_size=0.2,
    random_state=42
)

# 4. Tokenizer (Türkçe BERT)
tokenizer = BertTokenizer.from_pretrained("dbmdz/bert-base-turkish-cased")

# 5. Encoding (tokenize et ve pad/truncate işlemleri)  - truncation=True: Uzun cümleleri keser - padding=True: Kısa cümlelere dolgu ekler
train_encodings = tokenizer(train_texts, truncation=True, padding=True)
val_encodings = tokenizer(val_texts, truncation=True, padding=True)

# 6. Dataset sınıfı. - Bu sınıf verileri PyTorch’un anlayacağı formatta geri döndürür
class HaberDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    # __getitem__: Tek bir örneği getirir
    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    # __len__: Dataset’in toplam uzunluğu
    def __len__(self):
        return len(self.labels)

# 7. Dataset nesneleri oluştur
train_dataset = HaberDataset(train_encodings, train_labels)
val_dataset = HaberDataset(val_encodings, val_labels)

# 8. BERT modeli (2 sınıf için ayarlandı)
model = BertForSequenceClassification.from_pretrained(
    "dbmdz/bert-base-turkish-cased",     # dbmdz/bert-base-turkish-cased: Türkçe için eğitilmiş bir BERT modeli
    num_labels=2  # 0 ve 1 için iki sınıf
)

# 9. Eğitim ayarları
training_args = TrainingArguments(
    output_dir="./results",            # Eğitim sonuçlarının kaydedileceği klasör
    eval_strategy="epoch",             # Her epoch sonunda validation verisiyle değerlendirme yapılır
    save_strategy="epoch",             # Her epoch sonunda model kaydedilir
    per_device_train_batch_size=8,     # Eğitim sırasında işlemci/GPU başına batch boyutu
    per_device_eval_batch_size=8,      # Değerlendirme için batch boyutu
    num_train_epochs=3,                # Toplam 3 epoch eğitilecek
    logging_dir="./logs",              # Log kayıtları bu klasöre yazılır
    logging_steps=10,                  # Her 10 adımda bir log yazılır
    load_best_model_at_end=True        # En iyi sonucu veren model epoch sonunda yeniden yüklenir
)

# 10. Padding ve veri düzenleyici
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# 11. Trainer nesnesi
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator
)

# 12. Modeli eğit
trainer.train()

# 13. Eğitilen modeli kaydet
model.save_pretrained("bert_fake_news_model")
tokenizer.save_pretrained("bert_fake_news_model")




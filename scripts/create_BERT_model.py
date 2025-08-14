import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from transformers import DataCollatorWithPadding
import torch

df = pd.read_csv("C:/Users/LENOVO/PycharmProjects/FakeNewsDetection/data/cleaned_data.csv")

df = df[['clean_text', 'Sonuc']].dropna()

train_texts, val_texts, train_labels, val_labels = train_test_split(
    df['clean_text'].tolist(),
    df['Sonuc'].tolist(), 
    test_size=0.2,
    random_state=42
)

tokenizer = BertTokenizer.from_pretrained("dbmdz/bert-base-turkish-cased")

train_encodings = tokenizer(train_texts, truncation=True, padding=True)
val_encodings = tokenizer(val_texts, truncation=True, padding=True)

class HaberDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = HaberDataset(train_encodings, train_labels)
val_dataset = HaberDataset(val_encodings, val_labels)

model = BertForSequenceClassification.from_pretrained(
    "dbmdz/bert-base-turkish-cased",    
    num_labels=2  
)

training_args = TrainingArguments(
    output_dir="./results",           
    eval_strategy="epoch",           
    save_strategy="epoch",             
    per_device_train_batch_size=8,    
    per_device_eval_batch_size=8,     
    num_train_epochs=3,               
    logging_dir="./logs",             
    logging_steps=10,                 
    load_best_model_at_end=True        
)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator
)

trainer.train()

model.save_pretrained("bert_fake_news_model")
tokenizer.save_pretrained("bert_fake_news_model")





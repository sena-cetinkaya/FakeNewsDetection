from sqlmodel import SQLModel, Session, create_engine
import pandas as pd
from app.schemas import News

engine = create_engine(r"postgresql://postgres:postgres@localhost:5437/news_dev")
#engine = create_engine(r"postgresql://postgres:postgres@localhost:5438/news_test")

df = pd.read_csv("../data/cleaned_data.csv")

with Session(engine) as session:
    for _, row in df.iterrows():
        news_item = News(news=row["clean_text"], result=row["Sonuc"])
        session.add(news_item)
        session.commit()

print("Veriler başarıyla yüklendi.")




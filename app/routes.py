from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.schemas import PredictionInput, PredictionOutput, News
from app.model_loader import predict_new
from app.db import get_session

router = APIRouter()

# 0/1 değerini açıklayan sözlük
label_map = {
    0: "gerçek",
    1: "sahte"
}

@router.post("/predict", response_model=PredictionOutput)
def predict(payload: PredictionInput, session: Session = Depends(get_session)):
    if not payload.news:
        raise HTTPException(status_code=400, detail="Prediction input is required.")
    try:
        prediction = predict_new(payload.news)  # bu int: 0 veya 1
        entry = News(news=payload.news, result=prediction)  # int olarak DB'ye gider
        session.add(entry)
        session.commit()
        return {"result": label_map.get(prediction, "bilinmiyor")}  # kullanıcıya string döner
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


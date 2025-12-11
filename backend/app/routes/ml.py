from fastapi import APIRouter

router = APIRouter(prefix="/ml")

@router.get("/predict")
def predict():
    return {"prediction": 123}

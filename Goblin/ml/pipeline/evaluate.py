import pandas as pd
from sklearn.metrics import mean_squared_error
from joblib import load
from .preprocess import preprocess
from loguru import logger

def evaluate_model(model_path: str, test_path: str):
    logger.info("Evaluating model...")
    model = load(model_path)
    df = pd.read_csv(test_path)
    df = preprocess(df)
    X = df.drop('target', axis=1)
    y = df['target']
    preds = model.predict(X)
    mse = mean_squared_error(y, preds)
    logger.info(f"MSE: {mse}")
    return mse

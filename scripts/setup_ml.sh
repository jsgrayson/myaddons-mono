#!/bin/bash
set -e

################################################################################
# ML Setup Script (SAFE VERSION — no heredocs)
################################################################################

BASE_DIR="$HOME/Documents/goblin-clean/ml"

echo "[ML] Creating ML directories ..."

mkdir -p "$BASE_DIR/pipeline"
mkdir -p "$BASE_DIR/data/raw"
mkdir -p "$BASE_DIR/data/processed"
mkdir -p "$BASE_DIR/models"

# Keep empty directories tracked
echo "" > "$BASE_DIR/data/raw/.gitkeep"
echo "" > "$BASE_DIR/data/processed/.gitkeep"
echo "" > "$BASE_DIR/models/.gitkeep"

################################################################################
# Helper function
################################################################################
write_file() {
    FILE="$1"
    shift
    printf "%s\n" "$@" > "$FILE"
}

################################################################################
# preprocess.py
################################################################################

write_file "$BASE_DIR/pipeline/preprocess.py" \
"import pandas as pd" \
"from loguru import logger" \
"" \
"def preprocess(df: pd.DataFrame) -> pd.DataFrame:" \
"    logger.info(\"Preprocessing data...\")" \
"    df = df.dropna()" \
"    return df"

################################################################################
# train.py
################################################################################

write_file "$BASE_DIR/pipeline/train.py" \
"import pandas as pd" \
"from sklearn.linear_model import LinearRegression" \
"from joblib import dump" \
"from loguru import logger" \
"from .preprocess import preprocess" \
"" \
"def train_model(input_path: str, model_path: str):" \
"    logger.info(\"Training model...\")" \
"    df = pd.read_csv(input_path)" \
"    df = preprocess(df)" \
"    X = df.drop('target', axis=1)" \
"    y = df['target']" \
"    model = LinearRegression()" \
"    model.fit(X, y)" \
"    dump(model, model_path)" \
"    logger.info(f\"Model saved to {model_path}\")"

################################################################################
# evaluate.py
################################################################################

write_file "$BASE_DIR/pipeline/evaluate.py" \
"import pandas as pd" \
"from sklearn.metrics import mean_squared_error" \
"from joblib import load" \
"from .preprocess import preprocess" \
"from loguru import logger" \
"" \
"def evaluate_model(model_path: str, test_path: str):" \
"    logger.info(\"Evaluating model...\")" \
"    model = load(model_path)" \
"    df = pd.read_csv(test_path)" \
"    df = preprocess(df)" \
"    X = df.drop('target', axis=1)" \
"    y = df['target']" \
"    preds = model.predict(X)" \
"    mse = mean_squared_error(y, preds)" \
"    logger.info(f\"MSE: {mse}\")" \
"    return mse"

################################################################################
# predict.py
################################################################################

write_file "$BASE_DIR/pipeline/predict.py" \
"from joblib import load" \
"import pandas as pd" \
"from loguru import logger" \
"" \
"def predict(model_path: str, input_data: dict):" \
"    logger.info(\"Running prediction...\")" \
"    df = pd.DataFrame([input_data])" \
"    model = load(model_path)" \
"    return model.predict(df)[0]"

################################################################################
# config.py
################################################################################

write_file "$BASE_DIR/pipeline/config.py" \
"MODEL_PATH = './ml/models/model.pkl'" \
"TRAIN_DATA = './ml/data/raw/train.csv'" \
"TEST_DATA = './ml/data/raw/test.csv'"

################################################################################
# Done
################################################################################

echo "[ML] ML subsystem created successfully."


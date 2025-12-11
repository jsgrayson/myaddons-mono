from loguru import logger
from .model import TSMModel

class TSMBrain:
    def __init__(self):
        self.model = TSMModel()
        logger.info("TSM Brain initialized")

    def predict(self, item_id: int):
        return self.model.predict_price(item_id)

if __name__ == "__main__":
    brain = TSMBrain()
    print(brain.predict(123))

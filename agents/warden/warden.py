import time
from loguru import logger

class Warden:
    def __init__(self):
        logger.info("Warden agent initialized")

    def heartbeat(self):
        logger.info("Warden heartbeat OK")

if __name__ == "__main__":
    w = Warden()
    while True:
        w.heartbeat()
        time.sleep(5)

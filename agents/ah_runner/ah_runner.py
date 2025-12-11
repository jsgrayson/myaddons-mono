from loguru import logger

class AHRunner:
    def scan(self):
        logger.info("Scanning Auction House...")
        return True

if __name__ == "__main__":
    a = AHRunner()
    a.scan()

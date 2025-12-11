from loguru import logger

class BankRunner:
    def run(self):
        logger.info("Running bank operations...")
        return True

if __name__ == "__main__":
    r = BankRunner()
    r.run()

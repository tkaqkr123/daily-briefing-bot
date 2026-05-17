import logging
from dotenv import load_dotenv
from src.config import load_config
from src.pipeline import run_pipeline

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    config = load_config("config.yml")
    success = run_pipeline(config)
    if success:
        logger.info("Daily briefing sent successfully.")
    else:
        logger.error("Failed to send daily briefing.")

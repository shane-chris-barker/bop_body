from logger_config import setup_logging
import logging
setup_logging()
from events.factories.consumer_factory import get_consumer
from events.handlers.registry_setup import register_handlers
from hardware_detection.helpers.services_startup_helper import start_enabled_services
import time
logger = logging.getLogger(__name__)

def main():
    log_prefix = "[🦾 MAIN]"
    logger.info(f"{log_prefix} Bop Body is waking up and checking the configuration")
    services = start_enabled_services()
    if not services:
        logger.info(f"{log_prefix} Bop Body started no services and will not be respond!")
    register_handlers()
    consumer = get_consumer()
    consumer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info(f"{log_prefix} Bop Body Is Shutting down")
        for service in services:
            if hasattr(service.instance, 'cleanup') and callable(service.instance.cleanup):
                service.instance.cleanup()
    finally:
        consumer.stop()

if __name__ == "__main__":
    main()

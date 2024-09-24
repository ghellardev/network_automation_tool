# utils/logger.py

# Import 'logging' module
import logging

# Configure the basic settings for logging
logging.basicConfig(
    # Set the filename for the log file
    filename='network_automation.log',
    # Set the logging level to INFO
    level=logging.INFO,
    # Define the format for log messages
    format='%(asctime)s:%(levelname)s:%(message)s'
)

import logging



def setup_logging(log_filename="face_attendance.log"):
    # Basic configuration for logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Create file handler which logs even debug messages
    file_handler = logging.FileHandler(log_filename, mode="a")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # Add handlers to the root logger
    logging.getLogger("").addHandler(file_handler)
    



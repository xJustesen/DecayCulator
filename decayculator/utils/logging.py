import logging
import os

logger = logging.getLogger("decayculator")


def configure_logger(debug_mode: bool = False, save_logs: bool = True) -> None:
    """Configure logging level and output destinations."""
    logger.setLevel(logging.DEBUG if debug_mode else logging.WARNING)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s :: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Guard to check if the logger already has handlers to avoid duplicate messages
    if logger.hasHandlers():
        return

    # File handler
    if save_logs:
        log_dir = ".logs"
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(os.path.join(log_dir, "entropy.log"))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Console handler (optional)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if debug_mode else logging.WARNING)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

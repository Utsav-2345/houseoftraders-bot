import logging
import os

class LoggingFormatter(logging.Formatter):
    """A custom logging formatter with colors for different log levels."""
    
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, self.reset)
        log_format = (
            f"{self.black + self.bold}{{asctime}}{self.reset} "
            f"{log_color}{{levelname:<8}}{self.reset} "
            f"{self.green + self.bold}{{name}}{self.reset} "
            "{message}"
        )

        formatter = logging.Formatter(log_format, "%Y-%m-%d %H:%M:%S", style="{")

        if record.exc_info:
            record.exc_text = formatter.formatException(record.exc_info)

        return formatter.format(record)

def setup_logging():    
    log_directory = "logs"
    os.makedirs(log_directory, exist_ok=True)
    
    logger = logging.getLogger("discord_bot")
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(LoggingFormatter())
    
    file_handler = logging.FileHandler(filename=f"{log_directory}/discord.log", encoding="utf-8", mode="a")
    file_formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
    )
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.WARNING)
    discord_logger.addHandler(console_handler)
    discord_logger.addHandler(file_handler)
    
    return logger

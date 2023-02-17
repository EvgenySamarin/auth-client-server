"""
Util functions
"""


def print_debug(application, message, tag="DEBUG",):
    """
    Debug logging

    :param application: Flask application context
    :param message: message for logging
    :param tag: tag log message, DEBUG by default
    """
    if application.config['DEBUG']:
        print(f"TAG: {tag}, message: {message}")
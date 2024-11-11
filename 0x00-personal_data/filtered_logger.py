#!/usr/bin/env python3
""" Filtered logger

Functions:
    filter_datum() - Returns a log mesage obfuscated

Classes:
    RedactingFormatter
"""
import logging
import mysql.connector
import re
from os import environ
from typing import List


PII_FIELDS = ("email", "phone", "ssn", "password", "ip")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Returns a log message obfuscated

    Args:
        fields (list of str): Fields in log message to obfuscate
        redaction (str): Character to replace fields values with
        message (str): Log message
        separator (str): Separator of fields in log message

    Returns:
        (str): Log message obfuscated

    Example:
        >>> print(filter_datum(["password"], 'xxx', "name=love;password=1234",
                  ';'))
        name=love;password=xxx
    """
    fields_str = ('|').join(fields)
    return re.sub(rf"({fields_str})=[^{separator}]+", rf"\1={redaction}",
                  message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming records """
        message = record.getMessage()
        record.msg = filter_datum(self.fields, self.REDACTION, message,
                                  self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """ Returns a custom logger """
    # Create logger
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False  # Prevent propagation to other handlers

    # Create and configure handler
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnect:
    """ Returns a database connector """
    # Get database configurations
    db = environ.get("PERSONAL_DATA_DB_NAME")
    user = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")

    # Connect to database
    connector = mysql.connector.connect(database=db, user=user,
                                        password=password, host=host)

    return connector

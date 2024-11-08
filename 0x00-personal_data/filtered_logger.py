#!/usr/bin/env/python3
from typing import List
import logging
import re


def filter_datum(fields: List, redaction: str, message: str, separator: str):
    """  """


# class RedactingFormatter(logging.Formatter):
#     """ Redacting Formatter class
#         """

#     REDACTION = "***"
#     FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
#     SEPARATOR = ";"

#     def __init__(self):
#         super(RedactingFormatter, self).__init__(self.FORMAT)

#     def format(self, record: logging.LogRecord) -> str:
#         NotImplementedError
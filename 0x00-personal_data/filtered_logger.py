#!/usr/bin/env python3
""" Filtered logger

Functions:
    filter_datum() - Returns a log mesage obfuscated
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str):
    """ Returns a log message obfuscated"""
    fields_str = ('|').join(fields)
    return re.sub(rf"({fields_str})=[^{separator}]+", rf"\1={redaction}",
                  message)


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

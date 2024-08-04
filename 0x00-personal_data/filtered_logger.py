#!/usr/bin/env python3
"""This module covers fields obfuscation."""

import re
from typing import List
import logging


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """Obfuscates specified fields in a log message."""
    pattern = r'({})=[^{}]*'.format(
            '|'.join(map(re.escape, fields)), re.escape(separator))
    return re.sub(pattern, r'\1=' + redaction, message)


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
        """Filter values in incoming log records using filter_datum.
        """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            original_message, self.SEPARATOR)

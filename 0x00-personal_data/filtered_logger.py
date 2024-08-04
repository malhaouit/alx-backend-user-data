#!/usr/bin/env python3
"""This module covers fields obfuscation."""

import re
from typing import List
import logging
import csv
import mysql.connector
from mysql.connector import MySQLConnection
import os


# Define the PII_FIELDS constant
PII_FIELDS = ("name", "email", "ssn", "password", "phone")


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


def get_logger() -> logging.Logger:
    """Creates and returns a logger named 'user_data'.
    """
    # Create a logger with the name of 'user_data' and level 'INFO'
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a stream handler
    stream_handler = logging.StreamHandler()

    # Create and set the formatter
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Get a database connection using environment variables.
    """
    # Retrieve the environment variables with default values
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connection.MySQLConnection(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
    return connection

#!/usr/bin/env python3
"""This module covers fields obfuscation."""

import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """Obfuscates specified fields in a log message."""
    pattern = r'({})=[^{}]*'.format(
            '|'.join(map(re.escape, fields)), re.escape(separator))
    return re.sub(pattern, r'\1=' + redaction, message)

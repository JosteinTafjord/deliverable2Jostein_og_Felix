import json
import re
import pathlib

import numpy as np
import pandas as pd

def read_log_file(path: str | pathlib.Path) -> tuple[str, str]:
    path = pathlib.Path(path)
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        return raw.decode("ISO-8859-1"), "ISO-8859-1"

LOG_PATTERN = re.compile(
    r"^\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s+"
    r"\[(?P<register_id>[^\]]+)\]\s+"
    r"item=(?P<item>.+?)\s+"
    r"price=(?P<price>\d+(?:\.\d+)?)\s+"
    r"(?P<currency>[A-Z]{3})\s+"
    r"\((?P<status>SUCCESS|REFUND|CANCELLED)\)\s*$"
)

def parse_log(text: str) -> list[dict]:
    """Extract valid transaction records from log text, ignoring noise lines."""
    records = []
    for line in text.splitlines():
        match = LOG_PATTERN.match(line.strip())
        if match:
            record = match.groupdict()
            record["price"] = float(record["price"])
            records.append(record)
    return records
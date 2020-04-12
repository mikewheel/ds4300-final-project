"""
Project-wide constants and settings.
"""

from pathlib import Path
from typing import Any, Dict, List
import json

BASE_DIR: Path = Path(__file__).parent
DATA_DIR : Path = BASE_DIR / "data"
INPUT_DATA_DIR: Path = DATA_DIR / "input"
OUTPUT_DATA_DIR: Path = DATA_DIR / "output"

WIKIPEDIA_ARCHIVE_FILE: Path = INPUT_DATA_DIR / "enwiki-20200201-pages-articles-multistream.xml.bz2"
WIKIPEDIA_INDEX_FILE: Path = INPUT_DATA_DIR / "enwiki-20200201-pages-articles-multistream-index.txt"

NEO4J_CONNECTION_PARAMETERS: Dict[str, Any] = json.load(open(BASE_DIR / 'neo4j.json', 'r'))
REDIS_CONNECTION_PARAMETERS: Dict[str, Any] = json.load(open(BASE_DIR / 'redis.json', 'r'))
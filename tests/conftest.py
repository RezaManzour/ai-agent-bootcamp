"""pytest configuration: add src/ to Python path for imports."""

import sys
from pathlib import Path

# Add src/ directory to Python path so tests can import ai_utils
SRC_DIR = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

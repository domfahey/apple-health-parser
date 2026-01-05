from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from apple_health_parser.utils.parser import Parser

# Use Path(__file__).parent for portable test data paths
TEST_DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def xml_file() -> Path:
    """Path to the test XML export file."""
    return TEST_DATA_DIR / "export.xml"


@pytest.fixture
def export_file() -> str:
    """Path to the test ZIP export file."""
    return str(TEST_DATA_DIR / "export.zip")


@pytest.fixture
def root(xml_file: Path) -> ET.Element:
    """Root element of the parsed XML test file."""
    with open(xml_file, "r") as file:
        return ET.parse(file).getroot()


@pytest.fixture
def parser(export_file: str, tmp_path: Path) -> Parser:
    """Parser instance configured with test data and temporary output directory."""
    return Parser(export_file=export_file, output_dir=tmp_path)


@pytest.fixture
def activity_flags() -> list[str]:
    """Activity overview flags for testing."""
    return [
        "HKQuantityTypeIdentifierActiveEnergyBurned",
        "HKQuantityTypeIdentifierAppleExerciseTime",
        "HKQuantityTypeIdentifierAppleStandTime",
    ]

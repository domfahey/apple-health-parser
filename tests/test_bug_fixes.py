"""Tests for bug fixes - TDD approach."""

from pathlib import Path
from unittest import mock
from xml.etree import ElementTree as ET

import pytest

from apple_health_parser.models.records import HeartRateData, HealthData
from apple_health_parser.utils.loader import Loader
from apple_health_parser.utils.parser import Parser


class TestHeartRateMotionContext:
    """Test heart rate parsing with missing or wrong motionContext metadata."""

    def test_heart_rate_without_metadata(self) -> None:
        """Heart rate records without MetadataEntry should not crash."""
        # Create a minimal heart rate record without metadata
        record = HeartRateData(
            type="HKQuantityTypeIdentifierHeartRate",
            sourceName="Test Watch",
            sourceVersion="1.0",
            device="Test Device",
            unit="count/min",
            creationDate="2024-01-01 00:00:00 +0000",
            startDate="2024-01-01 00:00:00 +0000",
            endDate="2024-01-01 00:00:00 +0000",
            value="72",
            motionContext=None,  # No motion context available
        )
        # Should default to "Unset" or handle None gracefully
        assert record.motion_context in ["Unset", None]

    def test_heart_rate_with_valid_motion_context(self) -> None:
        """Heart rate records with valid motionContext should parse correctly."""
        record = HeartRateData(
            type="HKQuantityTypeIdentifierHeartRate",
            sourceName="Test Watch",
            sourceVersion="1.0",
            device="Test Device",
            unit="count/min",
            creationDate="2024-01-01 00:00:00 +0000",
            startDate="2024-01-01 00:00:00 +0000",
            endDate="2024-01-01 00:00:00 +0000",
            value="72",
            motionContext="1",  # Sedentary
        )
        assert record.motion_context == "Sedentary"


class TestOverwriteBehavior:
    """Test overwrite=False behavior in Loader."""

    def test_overwrite_false_skips_extraction(self, tmp_path: Path) -> None:
        """When overwrite=False and export exists, extraction should be skipped."""
        # Create existing export directory
        export_dir = tmp_path / "apple_health_export"
        export_dir.mkdir()
        existing_file = export_dir / "existing.txt"
        existing_file.write_text("existing content")

        # Call delete_previous_export with overwrite=False
        # Should NOT delete the directory and should signal to skip extraction
        result = Loader.delete_previous_export(export_dir, overwrite=False)

        # The existing file should still be there
        assert existing_file.exists()
        # Function should return False to signal skip extraction
        assert result is False

    def test_overwrite_true_deletes_and_continues(self, tmp_path: Path) -> None:
        """When overwrite=True, existing export should be deleted."""
        export_dir = tmp_path / "apple_health_export"
        export_dir.mkdir()
        existing_file = export_dir / "existing.txt"
        existing_file.write_text("existing content")

        result = Loader.delete_previous_export(export_dir, overwrite=True)

        # Directory should be deleted
        assert not export_dir.exists()
        # Function should return True to signal continue extraction
        assert result is True

    def test_overwrite_none_prompts_user(self, tmp_path: Path) -> None:
        """When overwrite=None, user should be prompted."""
        export_dir = tmp_path / "apple_health_export"
        export_dir.mkdir()

        with mock.patch("click.confirm", return_value=False) as mock_confirm:
            result = Loader.delete_previous_export(export_dir, overwrite=None)
            mock_confirm.assert_called_once()
            # User declined, should return False
            assert result is False
            # Directory should still exist
            assert export_dir.exists()


class TestFormatCaseSensitivity:
    """Test image format case sensitivity."""

    def test_uppercase_html_format(self, parser: Parser) -> None:
        """Uppercase 'HTML' format should work the same as lowercase."""
        from apple_health_parser.plot.plots import Plot

        records = parser.get_flag_records("HKQuantityTypeIdentifierActiveEnergyBurned")
        plot = Plot(
            data=records,
            year=2024,
            source="Alexandre's Apple Watch",
            operation="sum",
            heatmap=False,
        )

        with mock.patch("plotly.graph_objs.Figure.write_html") as mock_write:
            plot.plot(show=False, save=True, format="HTML")
            mock_write.assert_called_once()

    def test_mixed_case_png_format(self, parser: Parser) -> None:
        """Mixed case 'Png' format should work."""
        from apple_health_parser.plot.plots import Plot

        records = parser.get_flag_records("HKQuantityTypeIdentifierActiveEnergyBurned")
        plot = Plot(
            data=records,
            year=2024,
            source="Alexandre's Apple Watch",
            operation="sum",
            heatmap=False,
        )

        with mock.patch("plotly.graph_objs.Figure.write_image") as mock_write:
            plot.plot(show=False, save=True, format="Png")
            mock_write.assert_called_once()


class TestEmptyStringValue:
    """Test empty string value handling."""

    def test_empty_string_value_handled(self) -> None:
        """Empty string values should be handled gracefully."""
        # Empty string is listed as valid in examples, should not raise
        record = HealthData(
            type="HKQuantityTypeIdentifierBodyMass",
            sourceName="Test",
            sourceVersion="1.0",
            unit="kg",
            creationDate="2024-01-01 00:00:00 +0000",
            startDate="2024-01-01 00:00:00 +0000",
            endDate="2024-01-01 00:00:00 +0000",
            value="",
        )
        # Empty string should be converted to None
        assert record.value is None

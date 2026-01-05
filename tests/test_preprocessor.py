import pandas as pd
import pytest

from apple_health_parser.exceptions import (
    InvalidHeatmapOperation,
    InvalidOperation,
    InvalidSource,
    MissingYear,
)
from apple_health_parser.utils.parser import Parser
from apple_health_parser.utils.preprocessor import Preprocessor


class TestPreprocessor:
    def test_exceptions(self, parser: Parser) -> None:
        data = parser.get_flag_records("HKQuantityTypeIdentifierActiveEnergyBurned")
        year = 2024
        source = "Alexandre's Apple Watch"
        operation = "sum"
        heatmap = False

        with pytest.raises(MissingYear):
            Preprocessor(
                data, year=2020, source=source, operation=operation, heatmap=heatmap
            )

        with pytest.raises(InvalidOperation):
            Preprocessor(
                data, year=year, source=source, operation="test", heatmap=heatmap
            )

        with pytest.raises(InvalidSource):
            Preprocessor(
                data,
                year=year,
                source="Invalid Source",
                operation=operation,
                heatmap=heatmap,
            )

    def test_get_dataframe(self, parser: Parser) -> None:
        data = parser.get_flag_records("HKQuantityTypeIdentifierActiveEnergyBurned")
        year = 2024
        source = "Alexandre's Apple Watch"
        operation = "sum"
        heatmap = False
        preprocessor = Preprocessor(data, year, source, operation, heatmap)
        df = preprocessor.get_dataframe()

        assert isinstance(df, pd.DataFrame)
        assert df.shape == (2, 2)

        heatmap = True
        preprocessor = Preprocessor(data, year, source, operation, heatmap)
        df = preprocessor.get_dataframe()
        assert df.shape == (1, 2)

    def test_get_heatmap(self, parser: Parser) -> None:
        data = parser.get_flag_records("HKQuantityTypeIdentifierActiveEnergyBurned")
        year = 2024
        source = "Alexandre's Apple Watch"
        operation = "sum"
        heatmap = False
        preprocessor = Preprocessor(data, year, source, operation, heatmap)
        df = preprocessor.get_dataframe()
        heatmap = Preprocessor.get_heatmap(df)

        assert isinstance(heatmap, pd.DataFrame)
        assert heatmap.shape == (1, 2)
        assert heatmap.columns.name == "day"
        assert heatmap.index.name == "month"

    def test_invalid_heatmap_operation(self, parser: Parser) -> None:
        """Test that InvalidHeatmapOperation is raised when heatmap=True but no operation."""
        data = parser.get_flag_records("HKQuantityTypeIdentifierActiveEnergyBurned")

        with pytest.raises(InvalidHeatmapOperation):
            Preprocessor(data, year=2024, operation=None, heatmap=True)

    def test_sleep_data_ignores_operation(self, parser: Parser) -> None:
        """Test that sleep data logs warning and ignores operation."""
        data = parser.get_flag_records("HKCategoryTypeIdentifierSleepAnalysis")

        # Should not raise, but should reset operation to None
        preprocessor = Preprocessor(data, year=2024, operation="sum", heatmap=False)
        df = preprocessor.get_dataframe()

        # Operation should be cleared for sleep data
        assert preprocessor.oper is None
        assert isinstance(df, pd.DataFrame)

    def test_sleep_data_with_heatmap_returns_raw_data(self, parser: Parser) -> None:
        """Test that sleep data with heatmap returns raw data (operation is cleared first)."""
        data = parser.get_flag_records("HKCategoryTypeIdentifierSleepAnalysis")

        # Sleep data clears operation, so heatmap logic is bypassed
        preprocessor = Preprocessor(data, year=2024, operation="sum", heatmap=True)
        df = preprocessor.get_dataframe()

        # Operation is cleared for sleep data
        assert preprocessor.oper is None
        # Returns raw sleep data
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

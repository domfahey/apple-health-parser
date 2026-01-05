from unittest import mock

import pytest
from plotly.graph_objs import Figure

from apple_health_parser.exceptions import InvalidImageFormat
from apple_health_parser.plot.sleep import SleepPlot
from apple_health_parser.utils.parser import Parser


class TestSleepPlot:
    def test_timerange_valid(self, parser: Parser) -> None:
        """Test SleepPlot with valid timerange filtering."""
        records = parser.get_flag_records(flag="HKCategoryTypeIdentifierSleepAnalysis")

        # Use a timerange that includes the test data
        timerange = ("2024-01-01T00:00:00+00:00", "2024-01-02T23:59:59+00:00")
        plot = SleepPlot(data=records, year=2024, timerange=timerange)

        # Should filter the dataframe based on the timerange
        assert plot.dataframe is not None

    def test_timerange_invalid_type(self, parser: Parser) -> None:
        """Test SleepPlot raises ValueError for invalid timerange type."""
        records = parser.get_flag_records(flag="HKCategoryTypeIdentifierSleepAnalysis")

        # Test with non-tuple type
        with pytest.raises(ValueError, match="timerange must be a tuple"):
            SleepPlot(data=records, year=2024, timerange=["2024-01-01", "2024-01-02"])

        # Test with tuple of wrong length
        with pytest.raises(ValueError, match="timerange must be a tuple"):
            SleepPlot(data=records, year=2024, timerange=("2024-01-01",))

    def test_timerange_invalid_elements(self, parser: Parser) -> None:
        """Test SleepPlot raises ValueError for non-string timerange elements."""
        records = parser.get_flag_records(flag="HKCategoryTypeIdentifierSleepAnalysis")

        # Test with non-string elements
        with pytest.raises(ValueError, match="must be strings in ISO format"):
            SleepPlot(data=records, year=2024, timerange=(123, 456))

        with pytest.raises(ValueError, match="must be strings in ISO format"):
            SleepPlot(data=records, year=2024, timerange=("2024-01-01T00:00:00", 456))


    def test_get_figure(self, parser: Parser) -> None:
        records = parser.get_flag_records(flag="HKCategoryTypeIdentifierSleepAnalysis")

        plot = SleepPlot(data=records, year=2024)
        fig = plot._get_figure()
        assert isinstance(fig, Figure)

    def test_plot(self, parser: Parser) -> None:
        records = parser.get_flag_records(flag="HKCategoryTypeIdentifierSleepAnalysis")

        plot = SleepPlot(data=records, year=2024)
        fig = plot.plot(show=False, save=False)
        assert isinstance(fig, Figure)

        with (
            mock.patch("plotly.graph_objs.Figure.show") as mock_show,
            mock.patch("plotly.graph_objs.Figure.write_html") as mock_write_html,
            mock.patch("plotly.graph_objs.Figure.write_image") as mock_write_image,
        ):
            plot.plot(show=True, save=False)
            mock_show.assert_called_once()

            plot.plot(show=False, save=True, format="html")
            mock_write_html.assert_called_once()

            plot.plot(show=False, save=True, format="png")
            mock_write_image.assert_called_once()

    def test_plot_invalid_image_format(self, parser: Parser) -> None:
        records = parser.get_flag_records(flag="HKCategoryTypeIdentifierSleepAnalysis")

        overview = SleepPlot(data=records, year=2024)
        fmt = "tiff"
        with pytest.raises(InvalidImageFormat):
            overview.plot(show=False, save=True, format=fmt)

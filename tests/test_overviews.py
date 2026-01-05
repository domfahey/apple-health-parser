from unittest import mock

import pytest
from plotly.graph_objs import Figure

from apple_health_parser.exceptions import (
    InvalidImageFormat,
    InvalidOverviewType,
    MissingFlag,
)
from apple_health_parser.plot.overviews import Overview
from apple_health_parser.utils.parser import Parser


class TestOverviews:
    def test_validate(self, parser: Parser, activity_flags: list[str]) -> None:
        """Test validation raises appropriate exceptions."""
        records = parser.get_flag_records(flag=activity_flags)

        with pytest.raises(InvalidOverviewType):
            Overview(data=records, overview_type="fake-overview", year=2024)

        with pytest.raises(MissingFlag):
            Overview(data=records, overview_type="body", year=2024)

    def test_get_figure(self, parser: Parser, activity_flags: list[str]) -> None:
        """Test figure generation for activity overview."""
        records = parser.get_flag_records(flag=activity_flags)

        overview = Overview(data=records, overview_type="activity", year=2024)
        fig = overview._get_figure()
        assert isinstance(fig, Figure)

    def test_plot(self, parser: Parser, activity_flags: list[str]) -> None:
        """Test plot show and save functionality."""
        records = parser.get_flag_records(flag=activity_flags)

        overview = Overview(data=records, overview_type="activity", year=2024)
        fig = overview.plot(show=False, save=False)
        assert isinstance(fig, Figure)

        with (
            mock.patch("plotly.graph_objs.Figure.show") as mock_show,
            mock.patch("plotly.graph_objs.Figure.write_html") as mock_write_html,
            mock.patch("plotly.graph_objs.Figure.write_image") as mock_write_image,
        ):
            overview.plot(show=True, save=False)
            mock_show.assert_called_once()

            overview.plot(show=False, save=True, format="html")
            mock_write_html.assert_called_once()

            overview.plot(show=False, save=True, format="png")
            mock_write_image.assert_called_once()

    @pytest.mark.parametrize("fmt", ["tiff", "bmp", "gif"])
    def test_plot_invalid_image_format(
        self, parser: Parser, activity_flags: list[str], fmt: str
    ) -> None:
        """Test that invalid image formats raise InvalidImageFormat."""
        records = parser.get_flag_records(flag=activity_flags)

        overview = Overview(data=records, overview_type="activity", year=2024)
        with pytest.raises(InvalidImageFormat):
            overview.plot(show=False, save=True, format=fmt)

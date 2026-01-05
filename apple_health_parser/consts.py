"""Constants for Apple Health data parsing.

Provides derived constants from configuration definitions:
- FLAG_METADATA: Mapping of health data type identifiers to display metadata
- ALLOWED_IMAGE_FORMATS: Valid image export formats (png, jpg, svg, pdf, html)
- OPERATIONS: Valid aggregation operations (sum, mean, min, max, std)
- PLOT_TYPES: Available plot types (plot, heatmap)
- OVERVIEW_TYPES: Overview categories (activity, body)
"""

from apple_health_parser.config.definitions import (
    AllowedImageFormats,
    Operations,
    OverviewSubtypes,
    PlotType,
    get_flag_metadata,
)

FLAG_METADATA = get_flag_metadata()
ALLOWED_IMAGE_FORMATS = [fmt.value for fmt in AllowedImageFormats]
OPERATIONS = [op.value for op in Operations]
PLOT_TYPES = [ptype.value for ptype in PlotType]
OVERVIEW_TYPES = [overview.name.lower() for overview in OverviewSubtypes]

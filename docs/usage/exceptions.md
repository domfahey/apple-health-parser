# Exceptions

Custom exceptions for handling parsing errors and invalid inputs.

| Exception | When Raised |
|-----------|-------------|
| `MissingFlag` | Flag not found in parsed data |
| `MissingRecords` | No records available to process |
| `MissingYear` | No records for the specified year |
| `InvalidFlag` | Flag string not in allowed flags list |
| `InvalidFileFormat` | Output file not `.csv` |
| `InvalidImageFormat` | Image format not `png`, `svg`, etc. |
| `InvalidOperation` | Aggregation operation not supported |
| `InvalidSource` | Source device/app not found |
| `InvalidOverviewType` | Overview type not valid |
| `InvalidHeatmapOperation` | Heatmap requires an aggregation operation |

::: apple_health_parser.exceptions

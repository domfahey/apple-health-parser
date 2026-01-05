# Apple Health Parser

![logo](assets/images/logo.png){ align=left width=18% }

The *Apple Health Parser* Python package simplifies the extraction and analysis of health data exported from [Apple HealthKit](https://developer.apple.com/documentation/healthkit). Designed for seamless integration into data science workflows and health analytics applications, this package offers robust parsing and plotting capabilities for various health metrics stored in the Apple Health export XML format.

!!! warning
    This package is still in active development and has not been tested on real data coming from different sources, nor has it been tested with data originating from versions of iOS < 17.

## Quick Start

```python
from apple_health_parser.utils.parser import Parser
from apple_health_parser.plot.plots import Plots

# Parse your Apple Health export
parser = Parser(export_file="export.zip", overwrite=True)

# Get heart rate data
data = parser.get_flag_records("HKQuantityTypeIdentifierHeartRate")

# Plot daily averages for 2024
plot = Plots(data=data, year=2024, operation="mean")
plot.plot(plot_type="bar", save=True)
```

<div class="grid cards" markdown>

- :octicons-terminal-16: __Installation__

    ---

    Install `apple-health-parser` with `pip` or `uv` and get up
    and running in a jiffy!

    [:octicons-arrow-right-24: Get the package!](installation.md)

- :octicons-table-16: __Data Processing__

    ---

    Comes with a parser and all the tooling needed to extract and process Apple Health records

    [:octicons-arrow-right-24: Getting started](tutorial/basics.md)

- :material-chart-scatter-plot: __Visualize Health Data__

    ---

    Visualize meaningful health metrics using the built-in plotting capabilities

    [:octicons-arrow-right-24: Plots](tutorial/plots.md)

- :material-scale-balance: __Open Source, MIT__

    ---

    **Apple Health Parser** is licensed under MIT and available on [GitHub](https://github.com/alxdrcirilo/apple-health-parser)

    [:octicons-arrow-right-24: License](#)

</div>

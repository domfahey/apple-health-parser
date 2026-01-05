# Parser

The main interface for parsing Apple Health exports.

`Parser` extends `Loader` and provides methods to:

- Extract and read `export.zip` files
- Group records by HealthKit flag types
- Build validated Pydantic models from XML records
- Get sources and devices for each flag
- Export parsed data to CSV

## Basic Usage

```python
from apple_health_parser.utils.parser import Parser

parser = Parser(export_file="export.zip", overwrite=True)
data = parser.get_flag_records("HKQuantityTypeIdentifierHeartRate")
```

---

::: apple_health_parser.utils.parser.Parser
    options:
      show_root_heading: true

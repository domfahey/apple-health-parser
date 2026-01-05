# Models

Pydantic models for validated health records and parsed data containers.

## Record Models

Health records are validated using Pydantic models that map XML attributes to typed Python fields:

- **HealthData** - Base model for all health metrics (heart rate, steps, distance, etc.)
- **HeartRateData** - Extends HealthData with `motion_context` (sedentary, active, unset)
- **SleepData** - Extends HealthData with `timezone` and computed `range` duration

## Container Model

**ParsedData** holds the results of parsing a specific flag, containing:

- `flag` - The HealthKit identifier (e.g., `HKQuantityTypeIdentifierHeartRate`)
- `sources` - List of source apps/devices
- `devices` - List of hardware devices with version info
- `dates` - Set of unique dates in the data
- `records` - pandas DataFrame of all records

---

::: apple_health_parser.models.parsed.ParsedData
    options:
      show_root_heading: true

::: apple_health_parser.models.records.HealthData
    options:
      show_root_heading: true

::: apple_health_parser.models.records.HeartRateData
    options:
      show_root_heading: true

::: apple_health_parser.models.records.SleepData
    options:
      show_root_heading: true

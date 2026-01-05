# PreprocessorInterface

Abstract base class for data preprocessing operations.

`PreprocessorInterface` defines the contract for transforming parsed health data:

- Filtering by year and source
- Validating operation types (sum, mean, count, etc.)
- Aggregating records by time periods

The `Preprocessor` class implements this interface to prepare DataFrames for plotting.

---

::: apple_health_parser.interfaces.preprocessor_interface.PreprocessorInterface
    options:
      show_root_heading: true

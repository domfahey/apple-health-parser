# Loader

Base class for loading and extracting Apple Health export files.

`Loader` handles:

- Extracting `export.zip` to a target directory
- Reading and parsing the `export.xml` file
- Logging metadata (file sizes, record counts)
- Managing overwrite behavior for existing extractions

`Parser` extends this class to add record processing and model building.

---

::: apple_health_parser.utils.loader.Loader
    options:
      show_root_heading: true

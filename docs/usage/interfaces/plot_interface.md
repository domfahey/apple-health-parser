# PlotInterface

Abstract base class for all plot types.

`PlotInterface` defines the contract for creating health data visualizations:

- Preprocessing data with filtering and aggregation
- Selecting plot types (scatter, bar, line, heatmap)
- Saving plots to files or displaying interactively
- Configuring colormaps and styling

All concrete plot classes (e.g., `Plots`, `Overviews`, `SleepPlots`) inherit from this interface.

---

::: apple_health_parser.interfaces.plot_interface.PlotInterface
    options:
      show_root_heading: true

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python tool for comparing heart rate data from multiple devices by plotting data from TCX, GPX, or FIT files. The tool helps validate heart rate monitor accuracy by comparing different devices worn simultaneously.

## Architecture

The codebase follows a parser pattern with:

- `base.py`: Abstract `ActivityParser` class defining the interface for parsing activity files
- `tcx.py`, `gpx.py`, `fit.py`: Concrete parser implementations for different file formats
- `activity_parser.py`: Factory function `get_parser()` that returns appropriate parser based on file extension
- `chart.py`: Main CLI application that creates comparison charts from parsed data

All parsers implement the same interface providing:
- Heart rate values and timestamps
- Statistics (min/max/average HR, distance, duration)
- Pace and location data where available

## Development Commands

**IMPORTANT**: Always activate the virtual environment by running `source ./activate.sh` - this will create venv, install dependencies and activate the venv.

### Dependencies
- Install development dependencies: `source ./activate.sh`
- Update requirements: `source ./activate.sh && make reqs` (upgrades pre-commit and recompiles requirements)

### Testing
- Run tests: `pytest`
- Run tests with coverage: `pytest --cov`
- Test files are in `tests/` directory using pytest framework

### Code Quality
- Type checking: `mypy src/`
- Linting: `pylint src/`
- Pre-commit hooks are configured and should be updated with `make reqs`

### Running the Tool
- Basic usage: `python src/chart.py [folder]`
- With file prefix filter: `python src/chart.py tests/resources -p 2018`
- Generate output file: `python src/chart.py -o output_name [folder]`

## Key Dependencies
- `click`: CLI framework
- `matplotlib`: Chart generation
- `fitparse`, `gpxpy`, `lxml`: File format parsing
- `pytest`: Testing framework
- `mypy`, `pylint`: Code quality tools

## File Formats Supported
- TCX: Garmin, Polar, Suunto devices
- GPX: Strava, Komoot (with heart rate extensions)
- FIT: Garmin, Wahoo, modern Polar/Suunto devices

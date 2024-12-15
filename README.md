[![Build Status](https://github.com/andgineer/hrcomparison/workflows/ci/badge.svg)](https://github.com/andgineer/hrcomparison/actions)
[![Coverage](https://raw.githubusercontent.com/andgineer/hrcomparison/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/andgineer/hrcomparison/blob/python-coverage-comment-action-data/htmlcov/index.html)
# Heart Rate Monitor Comparison Tool

Compare heart rate readings from multiple devices by plotting data from TCX, GPX, or FIT files.
Perfect for validating heart rate monitor accuracy or comparing different devices worn simultaneously.

See example in the [Article comparing heart rate monitors (Garmin vs Coospo vs Scosche)](https://sorokin.engineer/posts/en/heart_rates_sensor_garmin_vs_coospo_vs_scosche)

## Supported Devices and Formats

### Heart Rate Recording Devices
- Chest Straps: Polar H9/H10, Garmin HRM-Pro/HRM-Dual, Wahoo TICKR
- Optical Sensors: Garmin/Polar/Suunto watches, Apple Watch

### File Formats
- TCX: Garmin, Polar, Suunto devices
- GPX: Strava, Komoot (with heart rate in extensions)
- FIT: Garmin, Wahoo, modern Polar and Suunto devices

### Compatible Apps
Export your data from:
- Garmin Connect
- Polar Flow
- Suunto app
- Strava
- Nike Run Club
- Training Peaks
- Zwift
- Endomondo (legacy)

With that tool was created [Article with heart rate monitor comparison](https://sorokin.engineer/posts/en/heart_rates_sensor_garmin_vs_coospo_vs_scosche)

## Usage

```bash
python src/chart.py --help

Usage: chart.py [OPTIONS] [FOLDER]

  Create comparison chart with plots from files in the `folder`.

  FOLDER Folder with data files (.tcx, .gpx, or .fit). By default, current folder is used.

Options:
  -p, --prefix TEXT      Prefix to filter files in the FOLDER. If not
                         specified, all files will be used.
  -o, --output FILENAME  Output file name without extension. If not specified,
                         chart will be shown.
  --help                 Show this message and exit.

```

For example to see on the screen chart created from files with names starting from `2018`
in folder `tests`:

```bash
    python src/chart.py tests/resources -p 2018
```

## Coverage report
* [Codecov](https://app.codecov.io/gh/andgineer/hrcomparison/tree/master/src)
* [Coveralls](https://coveralls.io/github/andgineer/hrcomparison)
[![Build Status](https://github.com/andgineer/hrcomparison/workflows/ci/badge.svg)](https://github.com/andgineer/hrcomparison/actions)
# TCX file analizer

Draw comparison chart combining all the plots from some TCX files set.

The TCX files contains data from Garmin, Polar or other sport hart rate tracker. 

Or just from apps like Strava, Endomondo, Nike running, Garmin Connect and many others.

With that tool was created [Article with heart rate monitor comparison](https://sorokin.engineer/posts/en/heart_rates_sensor_garmin_vs_coospo_vs_scosche)

## Usage

```bash
python chart.py --help

Usage: chart.py [OPTIONS] [FOLDER]

  Create comparison chart with plots from files in the `folder`.

  FOLDER Folder with data files (.tcx). By default, current folder is used.

Options:
  -p, --prefix TEXT      Prefix to filter files in the FOLDER. If not
                         specified, all files will be used.
  -o, --output FILENAME  Output file name without extension. If not specified,
                         chart will be shown.
  --help                 Show this message and exit.

```

For example to see on the screen chart created from files with names starting from `2018`
in folder `test`:

```bash
    python chart.py test -p 2018
```
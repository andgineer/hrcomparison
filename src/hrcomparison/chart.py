import os.path
import time
from datetime import datetime
from pathlib import Path

import click
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, date2num
from matplotlib.pyplot import legend

from hrcomparison.activity_parser import get_parser
from hrcomparison.base import ActivityParser


def parse_activity_file(filepath: str) -> ActivityParser | None:
    """
    Parse an activity file and return the parser instance.
    Returns None if parsing fails.
    """
    try:
        return get_parser(filepath)
    except Exception as exc:  # noqa: BLE001
        print(f"Error parsing {filepath}: {exc}")
        return None


def get_activity_files(folder: str, prefix: str = "") -> list[str]:
    """Get all supported activity files from the folder matching the prefix."""
    supported_extensions = (".tcx", ".gpx", ".fit")
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.startswith(prefix) and f.lower().endswith(supported_extensions)
    ]


@click.command()
@click.argument(
    "folder",
    type=click.Path(exists=True),
    default=".",
)
@click.option(
    "--prefix",
    "-p",
    "prefix",
    default="",
    help="Prefix to filter files in the FOLDER. If not specified, all files will be used.",
)
@click.option(
    "--output",
    "-o",
    "output",
    type=click.File("wb"),
    default=None,
    help="Output file name without extension. If not specified, chart will be shown.",
)
def compare_chart(folder: Path, prefix: str, output: str | None) -> None:
    """Create comparison chart with plots from files in the `folder`.

    FOLDER Folder with data files (.tcx, .gpx, or .fit). By default, current folder is used.
    """

    fig, ax = plt.subplots()
    now_timestamp = time.time()
    utc_offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
        now_timestamp,
    )
    ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))  # type: ignore

    # Get list of activity files
    activity_files = get_activity_files(str(folder), prefix)
    if not activity_files:
        print(
            f"No supported activity files found in {folder}"
            + (f" with prefix '{prefix}'" if prefix else ""),
        )
        return

    # Process each activity file
    for filepath in activity_files:
        data = parse_activity_file(filepath)
        if data is None:
            continue

        # Convert datetime objects to numbers matplotlib can plot
        adjusted_times = [date2num(t + utc_offset) for t in data.time_values]  # type: ignore

        # Extract sensor name from filename
        filename = os.path.basename(filepath)
        sensor = filename[len(prefix) :].split(".")[0]

        # Plot the data
        ax.plot(adjusted_times, data.hr_values, label=sensor)

    # Configure plot
    ax.grid(True)
    fig.autofmt_xdate()
    legend()

    ax.set_ylabel("Heart Rate (bpm)")
    ax.set_xlabel("Time")

    # Handle output
    if output:
        plt.savefig(os.path.join(folder, f"{output}.svg"))
    else:
        plt.show()


if __name__ == "__main__":
    compare_chart()  # pylint: disable=no-value-for-parameter

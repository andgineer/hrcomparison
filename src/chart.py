from pathlib import Path
from typing import Optional

import click
from pylab import legend
import tcx
import os.path
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import time
from datetime import datetime
import lxml.etree


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
def compare_chart(folder: Path, prefix: str, output: Optional[str]) -> None:
    """Create comparison chart with plots from files in the `folder`.

    FOLDER Folder with data files (.tcx). By default, current folder is used.
    """

    fig, ax = plt.subplots()
    now_timestamp = time.time()
    utc_offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
        now_timestamp
    )
    ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))  # type: ignore

    for file in os.listdir(folder):
        if file.startswith(prefix):
            try:
                data = tcx.TCXParser(os.path.join(folder, file))
            except lxml.etree.XMLSyntaxError as exc:  # pylint: disable=c-extension-no-member
                print(f"Error parsing {file}: {exc}")
                continue
            for key, time_value in enumerate(data.time_values):
                data.time_values[key] = time_value + utc_offset
            sensor = file[len(prefix) :].split(".")[0]
            ax.plot(data.time_values, data.hr_values, label=sensor)

    ax.grid(True)
    fig.autofmt_xdate()
    legend()

    if output:
        plt.savefig(os.path.join(folder, f"{output}.svg"))
    else:
        plt.show()


if __name__ == "__main__":
    compare_chart()  # pylint: disable=no-value-for-parameter

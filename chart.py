from pathlib import Path

import click
from pylab import *
import tcx
import os.path
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import time
from datetime import datetime


@click.command()
@click.argument(
    'folder',
    type=click.Path(exists=True),
    default='.',
)
@click.option(
    "--prefix",
    "-p",
    'prefix',
    default='',
    help='Prefix to filter files in the FOLDER. If not specified, all files will be used.',
)
@click.option(
    "--output",
    "-o",
    'output',
    type=click.File('wb'),
    default=None,
    help='Output file name without extension. If not specified, chart will be shown.',
)
def compare_chart(prefix: str, folder: Path, output: str):
    """Create comparison chart with plots from files in the `folder`.

    FOLDER Folder with data files (.tcx). By default, current folder is used.
    """

    fig, ax = plt.subplots()
    now_timestamp = time.time()
    utc_offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

    for file in os.listdir(folder):
        if file.startswith(prefix):
            data = tcx.TCXParser(os.path.join(folder, file))
            for key, time_value in enumerate(data.time_values):
                data.time_values[key] = time_value + utc_offset
            sensor = file[len(prefix):].split('.')[0]
            ax.plot(data.time_values, data.hr_values, label=sensor)

    ax.grid(True)
    fig.autofmt_xdate()
    legend()

    if output:
        savefig(os.path.join(folder, f'{output}.svg'))
    else:
        show()


if __name__ == "__main__":
    compare_chart()  # pylint: disable=no-value-for-parameter

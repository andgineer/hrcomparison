from pylab import *
import tcx
import os.path
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import time
from datetime import datetime


def compare_chart(prefix, folder='.', save_to_file=False):
    """
    :param prefix: filename prefix
    :param folder: folder with data files
    :param save_to_file - if False(by default) shows the chart on screen.
    if True then saves it into the file with name <prefix>.svg
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

    if save_to_file:
        savefig(os.path.join(folder, f'{prefix[:-1]}.svg'))
    else:
        show()


if __name__ == "__main__":
    # compare_chart('20180415_ski_', folder='/users/andrejsorokin/Downloads/')
    compare_chart('20180506_roller_', folder='/users/andrejsorokin/Downloads/', save_to_file=True)
    # compare_chart('20180509_run_', folder='/users/andrejsorokin/Downloads/', save_to_file=True)

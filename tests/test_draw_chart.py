import traceback
from datetime import datetime

import click
import matplotlib
import pytest

matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import os
from unittest.mock import Mock, MagicMock
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from pathlib import Path
from click.testing import CliRunner

import chart

def test_compare_chart(mocker):
    fig_mock = Mock(spec=Figure)
    ax_mock = Mock(spec=Axes)
    ax_mock.xaxis = Mock()  # Add the xaxis attribute
    mocker.patch('matplotlib.pyplot.subplots', return_value=(fig_mock, ax_mock))
    mock_show = mocker.patch('chart.matplotlib.pyplot.show')
    mocker.patch('matplotlib.pyplot.savefig')
    mocker.patch('os.listdir', return_value=['file1.tcx', 'file2.tcx'])

    parse_mock = mocker.patch('tcx.TCXParser')
    parse_mock.side_effect = [
        Mock(hr_values=[1, 2, 3], time_values=[datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3)]),
        Mock(hr_values=[4, 5, 6], time_values=[datetime(2023, 2, 1), datetime(2023, 2, 2), datetime(2023, 2, 3)])]

    runner = CliRunner()
    result = runner.invoke(chart.compare_chart, [".", "--prefix", "", "--output", None])

    assert result.exit_code == 0, traceback.format_exception(*result.exc_info)

    os.listdir.assert_called_once_with('.')
    assert parse_mock.call_count == 2
    assert parse_mock.call_args_list[0] == mocker.call(os.path.join('.', 'file1.tcx'))
    assert parse_mock.call_args_list[1] == mocker.call(os.path.join('.', 'file2.tcx'))

    mock_show.assert_called_once()

def test_compare_chart_with_output(mocker):
    fig_mock = Mock(spec=Figure)
    ax_mock = Mock(spec=Axes)
    ax_mock.xaxis = Mock()  # Add the xaxis attribute
    mocker.patch('matplotlib.pyplot.subplots', return_value=(fig_mock, ax_mock))
    mocker.patch('chart.matplotlib.pyplot.show')
    savefig_mock = mocker.patch('chart.matplotlib.pyplot.savefig')
    mocker.patch('os.listdir', return_value=['file1.tcx'])

    parse_mock = mocker.patch('tcx.TCXParser')
    parse_mock.return_value = Mock(hr_values=[1,2,3], time_values=[datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3)])

    runner = CliRunner()
    result = runner.invoke(chart.compare_chart, [".", "--prefix", "", "--output", "output"])

    assert result.exit_code == 0, traceback.format_exception(*result.exc_info)

    os.listdir.assert_called_once_with('.')
    parse_mock.assert_called_once_with(os.path.join('.', 'file1.tcx'))

    savefig_mock.assert_called_once()
    matplotlib.pyplot.show.assert_not_called()

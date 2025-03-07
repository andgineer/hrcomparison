import traceback
from datetime import datetime

import matplotlib

matplotlib.use("Agg")  # Must be before importing matplotlib.pyplot or pylab!
import os
from unittest.mock import Mock
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from click.testing import CliRunner

import chart


def test_compare_chart(mocker):
    # Mock matplotlib
    fig_mock = Mock(spec=Figure)
    ax_mock = Mock(spec=Axes)
    ax_mock.xaxis = Mock()
    mocker.patch("matplotlib.pyplot.subplots", return_value=(fig_mock, ax_mock))
    mocker.patch("chart.plt.show")
    mocker.patch("matplotlib.pyplot.savefig")

    # Mock file listing
    mocker.patch("os.listdir", return_value=["file1.tcx", "file2.tcx"])

    # Create two different mock parsers with different data
    mock_parser1 = Mock()
    mock_parser1.hr_values = [1, 2, 3]
    mock_parser1.time_values = [
        datetime(2023, 1, 1),
        datetime(2023, 1, 2),
        datetime(2023, 1, 3),
    ]

    mock_parser2 = Mock()
    mock_parser2.hr_values = [4, 5, 6]
    mock_parser2.time_values = [
        datetime(2023, 2, 1),
        datetime(2023, 2, 2),
        datetime(2023, 2, 3),
    ]

    # Make get_parser return different mock parsers for different files
    get_parser_mock = mocker.patch("chart.get_parser", side_effect=[mock_parser1, mock_parser2])

    # Run test
    runner = CliRunner()
    result = runner.invoke(chart.compare_chart, [".", "--prefix", "", "--output", None])

    # Verify results
    assert result.exit_code == 0, traceback.format_exception(*result.exc_info)

    os.listdir.assert_called_once_with(".")
    assert get_parser_mock.call_count == 2
    assert get_parser_mock.call_args_list[0] == mocker.call(os.path.join(".", "file1.tcx"))
    assert get_parser_mock.call_args_list[1] == mocker.call(os.path.join(".", "file2.tcx"))

    # Verify both datasets were plotted
    assert ax_mock.plot.call_count == 2
    # Verify first plot call args
    assert ax_mock.plot.call_args_list[0][0][1] == [1, 2, 3]  # first hr_values
    # Verify second plot call args
    assert ax_mock.plot.call_args_list[1][0][1] == [4, 5, 6]  # second hr_values

    chart.plt.show.assert_called_once()


def test_compare_chart_with_output(mocker):
    # Mock matplotlib
    fig_mock = Mock(spec=Figure)
    ax_mock = Mock(spec=Axes)
    ax_mock.xaxis = Mock()
    mocker.patch("matplotlib.pyplot.subplots", return_value=(fig_mock, ax_mock))
    mocker.patch("matplotlib.pyplot.show")
    savefig_mock = mocker.patch("matplotlib.pyplot.savefig")

    # Mock file listing
    mocker.patch("os.listdir", return_value=["file1.tcx"])

    # Mock parser factory and parser
    mock_parser = Mock()
    mock_parser.hr_values = [1, 2, 3]
    mock_parser.time_values = [
        datetime(2023, 1, 1),
        datetime(2023, 1, 2),
        datetime(2023, 1, 3),
    ]

    get_parser_mock = mocker.patch("chart.get_parser", return_value=mock_parser)

    # Run test
    runner = CliRunner()
    result = runner.invoke(chart.compare_chart, [".", "--prefix", "", "--output", "output"])

    # Verify results
    assert result.exit_code == 0, traceback.format_exception(*result.exc_info)

    os.listdir.assert_called_once_with(".")
    get_parser_mock.assert_called_once_with(os.path.join(".", "file1.tcx"))

    savefig_mock.assert_called_once()
    matplotlib.pyplot.show.assert_not_called()


def test_get_activity_files(mocker):
    mock_listdir = mocker.patch(
        "os.listdir",
        return_value=[
            "file1.tcx",
            "file2.gpx",
            "file3.fit",
            "file4.txt",
            "test1.tcx",
            "test2.gpx",
        ],
    )

    # Test without prefix
    files = chart.get_activity_files("testdir")
    assert len(files) == 5  # Should get all .tcx, .gpx, and .fit files
    assert all(f.endswith((".tcx", ".gpx", ".fit")) for f in files)

    # Test with prefix
    files = chart.get_activity_files("testdir", "test")
    assert len(files) == 2  # Should only get test1.tcx and test2.gpx
    assert all(os.path.basename(f).startswith("test") for f in files)


def test_parse_activity_file(mocker):
    mock_parser = Mock()
    get_parser_mock = mocker.patch(
        "chart.get_parser",
        side_effect=[
            mock_parser,  # Success case
            ValueError("Unsupported format"),  # Failed case
            Exception("Parse error"),  # Error case
        ],
    )

    # Test successful parse
    result = chart.parse_activity_file("test.tcx")
    assert result == mock_parser

    # Test unsupported format
    result = chart.parse_activity_file("test.txt")
    assert result is None

    # Test parse error
    result = chart.parse_activity_file("bad.tcx")
    assert result is None


def test_compare_chart_no_files(mocker):
    # Mock matplotlib
    fig_mock = Mock(spec=Figure)
    ax_mock = Mock(spec=Axes)
    ax_mock.xaxis = Mock()  # Add the xaxis attribute
    mocker.patch("matplotlib.pyplot.subplots", return_value=(fig_mock, ax_mock))
    mocker.patch("chart.plt.show")

    # Mock empty directory
    mocker.patch("os.listdir", return_value=[])

    runner = CliRunner()
    result = runner.invoke(chart.compare_chart, ["."])

    assert result.exit_code == 0
    assert "No supported activity files found" in result.output


def test_compare_chart_mixed_formats(mocker):
    fig_mock = Mock(spec=Figure)
    ax_mock = Mock(spec=Axes)
    ax_mock.xaxis = Mock()
    mocker.patch("matplotlib.pyplot.subplots", return_value=(fig_mock, ax_mock))
    mocker.patch("chart.plt.show")

    # Mock files of different formats
    mocker.patch("os.listdir", return_value=["file1.tcx", "file2.gpx", "file3.fit"])

    mock_parser = Mock()
    mock_parser.hr_values = [1, 2, 3]
    mock_parser.time_values = [
        datetime(2023, 1, 1),
        datetime(2023, 1, 2),
        datetime(2023, 1, 3),
    ]

    get_parser_mock = mocker.patch("chart.get_parser", return_value=mock_parser)

    runner = CliRunner()
    result = runner.invoke(chart.compare_chart, ["."])

    assert result.exit_code == 0
    assert get_parser_mock.call_count == 3  # Should try to parse all three files

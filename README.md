# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/andgineer/hrcomparison/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                 |    Stmts |     Miss |   Cover |   Missing |
|------------------------------------- | -------: | -------: | ------: | --------: |
| src/hrcomparison/\_\_about\_\_.py    |        1 |        0 |    100% |           |
| src/hrcomparison/activity\_parser.py |       13 |        0 |    100% |           |
| src/hrcomparison/base.py             |       57 |        1 |     98% |        91 |
| src/hrcomparison/chart.py            |       52 |        3 |     94% |85, 104, 117 |
| src/hrcomparison/fit.py              |       84 |        3 |     96% | 57-58, 93 |
| src/hrcomparison/gpx.py              |       80 |        4 |     95% |56, 62, 80, 85 |
| src/hrcomparison/tcx.py              |       66 |        2 |     97% |    44, 50 |
|                            **TOTAL** |  **353** |   **13** | **96%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/andgineer/hrcomparison/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/andgineer/hrcomparison/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/andgineer/hrcomparison/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/andgineer/hrcomparison/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fandgineer%2Fhrcomparison%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/andgineer/hrcomparison/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.
# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/andgineer/hrcomparison/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                    |    Stmts |     Miss |   Cover |   Missing |
|------------------------ | -------: | -------: | ------: | --------: |
| src/activity\_parser.py |       13 |        0 |    100% |           |
| src/base.py             |       58 |        1 |     98% |        92 |
| src/chart.py            |       51 |        2 |     96% |   85, 113 |
| src/fit.py              |       87 |        7 |     92% |29-30, 34-35, 63-64, 97 |
| src/gpx.py              |       80 |        4 |     95% |57, 63, 80, 84 |
| src/tcx.py              |       68 |        4 |     94% |38, 42, 48, 54 |
|               **TOTAL** |  **357** |   **18** | **95%** |           |


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
from pathlib import Path
import pytest


def _get_repo_root_dir() -> str:
    """
    :return: path to the project folder.
    `tests/` should be in the same folder and this file should be in the root of `tests/`.
    """
    return str(Path(__file__).parent.parent)


ROOT_DIR = _get_repo_root_dir()
RESOURCES = Path(f"{ROOT_DIR}/tests/resources")


@pytest.fixture(
    scope="function",
    params=[
        "20180415_ski_garmin.tcx",
    ],
)
def tcx_file(request) -> str:
    return str(RESOURCES / request.param)

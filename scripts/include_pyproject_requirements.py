#!/usr/bin/env python3
"""Include requirements.txt in pyproject.toml project.dependencies array.

Author: Andrey Sorokin
email: andrey@sorokin.engineer
url: https://github.com/andgineer
License: MIT
"""

import argparse

import toml

PROJECT_METADATA_FILE_NAME = "pyproject.toml"
REQUIREMENTS_FILE_NAME = "requirements.txt"


def main(requirements_file_name: str, section_path: str) -> None:
    """Include requirements.txt in pyproject.toml project.dependencies array."""
    with open(requirements_file_name, encoding="utf8") as f:
        requirements = [
            line.strip() for line in f if line.strip() and not line.lstrip().startswith("#")
        ]
    print(
        f"From {requirements_file_name} read requirements:"
        f"\n{requirements[:10]}...\n...{len(requirements)} total",
    )

    with open(PROJECT_METADATA_FILE_NAME, encoding="utf8") as f:
        pyproject_data = toml.load(f)

    section_keys = section_path.split(".")
    target_section = pyproject_data
    for key in section_keys:
        target_section = target_section[key]

    print(
        f"To section `{section_path}` array `dependencies`"
        f" of `{PROJECT_METADATA_FILE_NAME}`, project `{pyproject_data['project']['name']}`.\n",
    )
    target_section["dependencies"] = requirements

    with open(PROJECT_METADATA_FILE_NAME, "w", encoding="utf8") as f:
        toml.dump(pyproject_data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="""Include dependencies from `requirements_file` into array `dependencies`
of pyproject.toml's section specified in `section_path`.

By default includes requirements.txt into `dependencies` array of section `project`.""",
    )
    parser.add_argument(
        "requirements_file",
        nargs="?",
        default=REQUIREMENTS_FILE_NAME,
        help="Input file with dependencies",
    )
    parser.add_argument(
        "section_path",
        nargs="?",
        default="project",
        help="Path to the section in pyproject.toml (e.g., tool.hatch.envs.test)",
    )

    args = parser.parse_args()
    main(requirements_file_name=args.requirements_file, section_path=args.section_path)

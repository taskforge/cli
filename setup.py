"""A task management tool that integrates with 3rd party services."""

from os import getenv

from setuptools import setup, find_packages

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="task_forge",
    version=getenv("VERSION", "0.0.0"),
    url="https://github.com/chasinglogic/taskforge",
    license="AGPL-3.0",
    author="Mathew Robinson",
    author_email="chasinglogic@gmail.com",
    description="A task management tool that integrates with 3rd party services",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=requirements,
    python_requires=">=3.6",
    entry_points={
        "task_forge.lists": [
            "taskforged = task_forge.lists.taskforged",
            "sqlite = task_forge.lists.sqlite",
        ],
        "console_scripts": [
            "task=task_forge.cli:main",
            "taskforged=task_forge.daemon:main",
        ],
    },
    classifiers=[
        # As from https://pypi.org/classifiers/
        "Development Status :: 4 - Beta",
        # 'Development Status :: 5 - Production/Stable',
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

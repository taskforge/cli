"""A task management tool that integrates with 3rd party services."""

from os import getenv, walk
from setuptools import find_packages, setup

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

with open("requirements/runtime.txt") as f:
    requirements = f.read().splitlines()

extras = {}
for root, filenames, _ in walk("requirements/extras"):
    for filename in filenames:
        with open(os.path.join(root, filename)) as f:
            extras[filename[: len(".txt")]] = f.read().splitlines()

setup(
    name="task_forge",
    version=getenv("VERSION", "0.0.0"),
    url="https://github.com/chasinglogic/taskforge",
    license="AGPL-3.0",
    author="Mathew Robinson",
    author_email="chasinglogic@gmail.com",
    description="A task management library and tool that integrates"
    " with 3rd party services",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=requirements,
    extras_require=extras,
    python_requires=">=3.6",
    entry_points={
        "task_forge.lists": [
            "task_server = task_forge.lists.task_server_client",
            "mongodb = task_forge.lists.mongo",
            "sqlite = task_forge.lists.sqlite",
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

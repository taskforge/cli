"""A task management tool that integrates with 3rd party services."""

from setuptools import find_packages, setup

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

with open("requirements.txt") as f:
    install_requires = [line for line in f if line]

setup(
    name="taskforge-cli",
    version="0.3.0",
    url="https://github.com/taskforge/cli",
    license="Apache-2.0",
    author="Mathew Robinson",
    author_email="chasinglogic@gmail.com",
    description="A task management tool that automates your workflow",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=True,
    platforms="any",
    install_requires=install_requires,
    entry_points={"console_scripts": ["task = taskforge:cli"]},
    classifiers=[
        # As from https://pypi.org/classifiers/
        "Development Status :: 4 - Beta",
        # 'Development Status :: 5 - Production/Stable',
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

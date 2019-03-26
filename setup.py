"""A task management tool that integrates with 3rd party services."""

from os import getenv
from setuptools import find_packages, setup

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='taskforge-cli',
    version=getenv('VERSION', '0.0.0'),
    url='https://github.com/chasinglogic/taskforge',
    license='AGPL-3.0',
    author='Mathew Robinson',
    author_email='chasinglogic@gmail.com',
    description='A task management library and tool that integrates'
    ' with 3rd party services',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=requirements,
    extras_require={
        'mongo': ['pymongo==3.7.1'],
        'github': ['pygithub==1.43.5'],
    },
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'task = task_forge.cli:main',
            'taskforged = task_forge.taskforged.cli:main'
        ],
        'task_forge.lists': [
            'task_server = task_forge.lists.task_server_client',
            'mongodb = task_forge.lists.mongo',
            'sqlite = task_forge.lists.sqlite',
        ],
    },
    classifiers=[
        # As from https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])

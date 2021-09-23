#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0',
                ]

test_requirements = [ ]

setup(
    author="Gerit Wagner",
    author_email='gerit.wagner@posteo.de',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Digital tickler activating files or directories on pre-defined dates",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='digital_tickler',
    name='digital_tickler',
    packages=find_packages(include=['digital_tickler', 'digital_tickler.*']),
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
    'console_scripts': [
        'digital_tickler=digital_tickler.digital_tickler:main',
        ],
    },
    url='https://github.com/geritwagner/digital_tickler',
    version='0.0.1',
    zip_safe=False,
)

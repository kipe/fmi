#!/usr/bin/env python
from setuptools import setup

setup(
    name='fmi_weather',
    version='1.0.0',
    description='FMI weather data fetcher',
    author='Kimmo Huoman',
    author_email='kipenroskaposti@gmail.com',
    url='https://github.com/kipe/fmi',
    packages=['fmi', 'fmi.symbols'],
    package_data={
        'fmi.symbols': [
            '*.svg',
            'fmi/symbols/*',
        ],
    },
    install_requires=[
        'beautifulsoup4>=4.8.1',
        'python-dateutil>=2.8.0',
        'requests>=2.20.0',
    ])

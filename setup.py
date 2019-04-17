#!/usr/bin/env python
from distutils.core import setup

setup(
    name='fmi_weather',
    version='0.50.1',
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
        'beautifulsoup4>=4.4.0',
        'python-dateutil>=2.4.2',
        'requests>=2.20.0',
    ])

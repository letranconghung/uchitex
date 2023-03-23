"""
Set up script for terminal use.
"""
from setuptools import setup

setup(
    name='texify',
    version='0.1.0',
    py_modules=['texify'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'texify = texify:cli',
        ],
    },
)

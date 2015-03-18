from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='milight',
    version='0.1',
    description='Controller for milight/limitlessled Wi-Fi LEDs',
    long_description=long_description,
    url='https://github.com/McSwindler/python-milight',
    author='McSwindler',
    author_email='wilingua@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Home Automation',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='limitlessled easybulb milight led wifi applight applamp ledme dekolight ilight',
    packages=["milight"],
    install_requires=[],
    test_suite="tests",
)

from setuptools import setup, find_packages
from codecs import open


setup(
    name='milight',
    version='0.5.2',
    description='Controller for milight/limitlessled Wi-Fi LEDs',
    long_description='Visit GitHub for more information: https://github.com/McSwindler/python-milight',
    url='https://github.com/McSwindler/python-milight',
    author='McSwindler',
    author_email='wilingua@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
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

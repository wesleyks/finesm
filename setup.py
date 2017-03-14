from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='fine_sm',

    version='0.0.0',

    description='A fine state machine',
    long_description=long_description,

    url='https://github.com/wesleyks/fine_sm',

    author='wesley sun',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
    ],

    keywords='finite-state machine state',

    packages=['fine_sm'],
)

from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='finesm',

    version='1.0.0',

    description='A fine state machine',
    long_description=long_description,
    long_description_content_type="text/markdown",

    url='https://github.com/wesleyks/finesm',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],

    keywords='finite-state machine state',

    packages=['finesm'],
)

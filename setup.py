from setuptools import setup
from jsrn import __version__

setup(
    name='jsrn',
    version=__version__,
    packages=['jsrn', 'jsrn.fields'],
    url='',
    license='BSD',
    author='Tim Savage',
    author_email='tim.savage@poweredbypenguins.org',
    description='JavaScript Resource Notation'
)
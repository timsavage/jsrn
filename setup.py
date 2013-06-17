from setuptools import setup
from jsrn import __version__

setup(
    name='jsrn',
    version=__version__,
    packages=['jsrn', 'jsrn.fields'],
    url='https://github.com/timsavage/jsrn',
    license='BSD',
    author='Tim Savage',
    author_email='tim.savage@poweredbypenguins.org',
    description='JavaScript Resource Notation for Python',
    install_requires=['six'],
    extras_require={
        # Extra performance
        'performance': ['simplejson'],
        # Documentation support using Jinja2
        'doc': ["jinja2>=2.7"],
    },
)

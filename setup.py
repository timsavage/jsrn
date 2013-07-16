from setuptools import setup

# Work around between pypi packages and Github needing a .rst
try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name='jsrn',
    version="0.3.2",
    url='https://github.com/timsavage/jsrn',
    license='LICENSE',
    author='Tim Savage',
    author_email='tim.savage@poweredbypenguins.org',
    description='JavaScript Resource Notation for Python',
    long_description=long_description,
    package_dir={'': 'src'},
    packages=['jsrn', 'jsrn.fields'],
    install_requires=['six'],
    extras_require={
        # Extra performance
        'performance': ['simplejson'],
        # Documentation support using Jinja2
        'doc': ["jinja2>=2.7"],
    },

    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
)

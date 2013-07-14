from setuptools import setup

setup(
    name='jsrn',
    version="0.3",
    url='https://github.com/timsavage/jsrn',
    license='LICENSE',
    author='Tim Savage',
    author_email='tim.savage@poweredbypenguins.org',
    description='JavaScript Resource Notation for Python',
    long_description=open("README.rst").read(),
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

import os.path
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()
with open(os.path.join(here, 'VERSION')) as f:
    VERSION = f.read()

requires = []

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-flake8',
    'pytest-cov',
    'mock',
]

graphs_require = [
    'pygraphviz'
]

setup(
    name='cd4ml',
    version=VERSION,
    description='Library to enable CD4ML steps',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 1 - Planning'
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Build Tools'
    ],
    keywords="machine learning mlops",
    packages=find_packages(),
    include_package_data=True,
    url='',
    license='BSD',
    author='Eduardo Santos',
    author_email='eduardo@eduardosan.com',
    extras_require={
        'testing': tests_require,
        'graphs': graphs_require
    },
    install_requires=requires,
)

import os
from setuptools import find_packages, setup

import rest_scaffold


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# get README
with open('README.rst') as f:
    long_description = f.read()

setup(
    name='django-rest-scaffold',
    version=rest_scaffold.__version__,
    packages=find_packages(),
    install_requires=['Django>=2', 'djangorestframework>=3'],
    description='A re-useable Django helper app for integrating rest-scaffold.js.',
    long_description=long_description,
    url='https://github.com/gregschmit/django-rest-scaffold',
    author='Gregory N. Schmit',
    author_email='me@gregschmit.com',
    license='MIT',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)

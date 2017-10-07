import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='stackable',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',  # example license
    description='stackable settings for Django',
    long_description=README,
    author='miraculixx',
    author_email='miraculixx@gmx.ch',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: Commercial',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # replace these appropriately if you are using Python 3
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django<1.9',
        'PyYAML',
        'ordered_set',
        'pyaes',
        'six',
    ],
    dependency_links=[
    ]
)

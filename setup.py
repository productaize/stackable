import os

from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
VERSION =open(os.path.join(os.path.dirname(__file__), 'stackable', 'VERSION')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='stackable',
    version=VERSION,
    packages=find_packages(),
    url='https://github.com/productaize/stackable',
    include_package_data=True,
    license='MIT',  # example license
    description='stackable settings for any Python and Django application',
    long_description=README,
    long_description_content_type='text/markdown',
    author='miraculixx',
    author_email='miraculixx@gmx.ch',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # replace these appropriately if you are using Python 3
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'pyyaml>3.11',
        'ordered_set',
        'pyaes',
    ],
    dependency_links=[
    ]
)

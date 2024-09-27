from setuptools import setup, find_packages

setup(
    name='subdomainradar',
    version='1.0.0',
    author='Alexandre Vandamme',
    author_email='alexandrevandammepro@gmail.com',
    description='Python wrapper for SubdomainRadar.io API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/alexandrevandamme59/subdomainradar-python-wrapper',
    packages=find_packages(),
    install_requires=[
        'requests>=2.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)

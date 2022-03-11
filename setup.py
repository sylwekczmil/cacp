#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'Jinja2>=3.0.3',
    'joblib>=1.1.0',
    'matplotlib>=3.3.4',
    'numpy>=1.18.5',
    'pandas>=1.1.5',
    'scikit-learn>=0.24.1',
    'tqdm>=4.62.3',
    'typing-extensions>=4.1.1'
]

test_requirements = ['pytest>=3', ]

setup(
    author="Sylwester Czmil",
    author_email='sylwekczmil@gmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="CACP: Classification Algorithms Comparison Pipeline",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='cacp',
    name='cacp',
    packages=find_packages(include=['cacp', 'cacp.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/sylwekczmil/cacp',
    version='0.1.2',
    zip_safe=False,
)


from setuptools import (
    setup,
    find_packages,
)


setup(
    name='pullenti_wrapper',
    version='0.4.0',
    description='Simpler interface for PullEnti Python package',
    url='https://github.com/pullenti/pullenti-wrapper',
    author='Alexander Kukushkin',
    author_email='alex@alexkuk.ru',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='natural language processing, named entity recognition',
    packages=find_packages(),
    install_requires=[
        'pullenti==3.14',
        'pullenti_client'
    ]
)

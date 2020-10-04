"""Tabu board game web application
"""
from setuptools import setup, find_packages
import glob


setup(
    name='ws.tabu',
    version='1.0.0.dev0',

    install_requires=[
        'setuptools',
        'tornado',
    ],

    extras_require={'test': [
        'pytest',
    ]},

    entry_points={
        'console_scripts': [
            'tabu-serve=ws.tabu.application:main',
        ],
    },

    author='Wolfgang Schnerring <wosc@wosc.de>',
    author_email='wosc@wosc.de',
    license='ZPL 2.1',
    url='https://github.com/wosc/tabu',

    description=__doc__.strip(),
    long_description='\n\n'.join(open(name).read() for name in (
        'README.rst',
        'CHANGES.txt',
    )),

    classifiers="""\
License :: OSI Approved :: Zope Public License
Programming Language :: Python
Programming Language :: Python :: 3
"""[:-1].split('\n'),

    namespace_packages=['ws'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    data_files=[('', glob.glob('*.txt'))],
    zip_safe=False,
)

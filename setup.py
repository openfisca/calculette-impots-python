#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name='calculette_impots',
    version='0.0.0.dev0',

    author='Christophe Benz',
    author_email='christophe.benz@data.gouv.fr',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Information Analysis',
        ],
    description='Calculette des impôts traduite en Python',
    keywords='calculette impôts tax',
    license='http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    url='https://git.framasoft.org/openfisca/calculette-impots-python',

    entry_points={
        'console_scripts': ['calculette-impots=calculette_impots.scripts.command_line:main'],
        },
    install_requires=[
        'calculette_impots_m_language_parser >= 0.0.0.dev0',
        'docopt',
        'toolz >= 0.7.4',
        ],
    packages=find_packages(),
    )

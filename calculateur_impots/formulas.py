# -*- coding: utf-8 -*-


import glob
import importlib
import os
import pkg_resources


def load_formulas():
    distribution_dir_path = pkg_resources.get_distribution('calculateur_impots').location
    for file_path in sorted(glob.iglob(os.path.join(distribution_dir_path, 'calculateur_impots', 'generated', '*.py'))):
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        importlib.import_module('.generated.' + file_name, 'calculateur_impots')

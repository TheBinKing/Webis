# conf.py — Webis documentation configuration file

import os
import sys
sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------

project = 'Webis'
copyright = '2025, Webis'
author = 'Webis Team'
release = '1.0'

# -- General configuration -----------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

# -- HTML output ----------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Encoding & Language --------------------------------------------------

language = 'en'  # Changed from zh_CN to en for English documentation

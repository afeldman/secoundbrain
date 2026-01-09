# Sphinx configuration for secoundbrain project
default_role = 'py'
project = 'secoundbrain'
author = 'afeldman'
release = '1.0.0'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]
napoleon_google_docstring = True
html_theme = 'alabaster'

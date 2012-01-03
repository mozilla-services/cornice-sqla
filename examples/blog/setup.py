import os
from setuptools import setup, find_packages

requires = ['cornice', 'cornicesqla', 'Mako']


setup(name='myblog',
      version='0.1',
      description='Demo for cornicesqla',
      author='Mozilla Services',
      author_email='services-dev@mozilla.org',
      packages=find_packages(),
      zip_safe=False,
      install_requires=requires)

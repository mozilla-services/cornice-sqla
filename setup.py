import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()


requires = ['cornice', 'SQLAlchemy', 'WebTest', 'Colander']


setup(name='cornicedb',
      version='0.1',
      description='CRUD for Cornice & SQLALchemy',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Mozilla Services',
      author_email='services-dev@mozilla.org',
      url='https://github.com/mozilla-services/cornicedb',
      keywords='web pyramid pylons',
      packages=find_packages(),
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="cornice",
      paster_plugins=['pyramid'])

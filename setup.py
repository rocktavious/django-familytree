import sys
from setuptools import setup, find_packages

import familytree

kw = {}
if sys.version_info >= (3,):
    kw['use_2to3'] = True

setup(name='django-' + familytree.__name__,
      version=familytree.__version__,
      description=familytree.__description__,
      long_description=open('README.md').read(),
      classifiers=[
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Development Status :: 4 - Beta',
          'Operating System :: OS Independent',
      ],
      keywords='',
      author=familytree.__author__,
      author_email=familytree.__author_email__,
      url=familytree.__url__,
      license=open('LICENSE').read(),
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=open('requirements.txt').read().splitlines(),
      setup_requires=[],
      tests_require=open('test_requirements.txt').read().splitlines(),
      namespace_packages=[],
      **kw)   

import os
import sys
from setuptools import setup, find_packages

version = '0.1.0'

def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


setup(name='flickr-views-counter',
      version=version,
      description=('Get view counts, favorites, and other data for each '
        'picture in a user\'s photostream'),
      long_description='\n\n'.join((read('README.md'), read('CHANGELOG'))),
      classifiers=[
          'License :: OSI Approved :: BSD License',
          'Intended Audience :: Developers',
          'Programming Language :: Python'],
      keywords='flickr photos views favorites',
      author='Jordan Jozwiak',
      author_email='support@jozapps.com',
      url='https://github.com/jordanjoz1/flickr-views-counter',
      license='MIT',
      py_modules=['count-views'],
      namespace_packages=[],
      install_requires = ['flickrapi'],
      entry_points={
          'console_scripts': [
              'flickr-views-counter = count-views:main']
      },
      include_package_data = False)
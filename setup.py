try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='erepublik',
      version='1.0',
      py_modules=['erepublik'],
      description='Unofficial erepublik API wrapper',
      author='Nikola Kovacevic',
      author_email='nikolak@outlook.com',
      url='https://github.com/Nikola-K/erepAPI',
      )

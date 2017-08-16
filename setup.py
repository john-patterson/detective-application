from setuptools import setup

setup(name='detective',
      version='1.0',
      description='Implementation of detective problem for Redacted application.',
      author='John P. Patterson',
      author_email='john@johnppatterson.com',
      license='MIT',
      packages=['detectiveapp'],
      test_suite='tests',
      entry_points={'console_scripts': ['detective=detectiveapp.cli:main']})


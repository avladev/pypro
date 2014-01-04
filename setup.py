import os
from distutils.core import setup

version = '0.1.0'

description = "Simple provisioning system suitable for deploying, configuring and task execution written in Python."
cur_dir = os.path.dirname(__file__)
try:
    long_description = open(os.path.join(cur_dir, 'README.md')).read()
except:
    long_description = description

setup(
    name = "pyprov",
    version = version,
    url = 'https://github.com/avladev/pyprov',
    license = 'MIT',
    description = description,
    long_description = long_description,
    author = 'Anatoli Vladev',
    author_email = 'avladev@gmail.com',
    packages = ['pyprov'],
    scripts = ['scripts/ppr.py'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)
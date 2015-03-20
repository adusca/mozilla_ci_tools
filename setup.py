import mozci
from setuptools import setup, find_packages

setup(
    name='mozci',
    version='0.3.1.dev0',
    packages=find_packages(),

    install_requires=[
        'beautifulsoup4==4.3.2',
        'requests==2.5.1',
        'bugsy==0.4.0',
        'mozillapulse'
    ],

    # Meta-data for upload to PyPI
    author='Armen Zambrano G.',
    author_email='armenzg@mozilla.com',
    description='It helps us dealing with the CI.',
    license='MPL',
    url='http://github.com/armenzg/mozilla_ci_tools',
)

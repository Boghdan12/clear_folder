from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='1.1',
    author='Bohdan_Haidaenko',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean=clean_folder.clean:start']}
)
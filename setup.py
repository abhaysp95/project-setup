from setuptools import find_packages, setup
from os import path

def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()

setup(
    name='mkproj',
    version='1.0',
    packages=find_packages('project'),
    description='create projects in cli',
    author='Abhay Shanker Pathak',
    author_email='abhaysp9955@gmail.com',
    platform='linux/unix',
    keywords="project programming language",
    long_description=read('README.md'),
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'mkproj=project.app:main',
        ],
    },
)

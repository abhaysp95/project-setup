from setuptools import find_packages, setup
from os import path

def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()

setup(
    name='mkproj',
    version='0.0.1',
    packages=find_packages('src'),
    description='create projects in cli',
    author='Abhay Shanker Pathak',
    author_email='abhaysp9955@gmail.com',
    keywords="project programming language",
    long_description=read('README.md'),
    url="https://github.com/coolabhays/project-setup",
    license="MIT",
    package_dir={'': 'src'},
    py_modules=["mkproj"],
    install_requires=[
        'Click',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilites",
        "Operating System :: Linux/Unix"
    ],
    entry_points={
        'console_scripts': [
            'mkproj=src.app:main',
        ],
    },
)

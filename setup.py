from setuptools import find_packages, setup
from os import path

def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()

setup(
    name='setproj',
    version='1.0.1',
    description='create projects in cli',
    author='Abhay Shanker Pathak',
    author_email='abhaysp9955@gmail.com',
    keywords="project programming language",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",  # set if not reStructuredText
    url="https://github.com/coolabhays/project-setup",
    license="MIT",
    # package_dir={'': 'setproj'},
    # py_modules=["setupProject"],
    # packages=["setproj"],
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Topic :: Terminals",
        "Operating System :: POSIX"
    ],
    entry_points={
        'console_scripts': [
            'setproj=setproj.__main__:main',
        ],
    },
)

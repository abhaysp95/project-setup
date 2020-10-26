from pathlib import Path
from os import uname
from sys import exit
import subprocess

# TODO:
# write for java-servlet and web-desinging(h/c/j)
# see, if you can activate virtualenv

class SetProject:
    """ General Project setup class """

    def __init__(self, name='new-project'):
        self.projName = name
        self.path = Path.cwd() / self.projName
        assert not self.path.exists(), "Provided project name already EXISTS in directory"
        self.path.mkdir()


class LangC(SetProject):
    """ further project setup for C language """

    def __init__(self, name='new-project'):
        super().__init__(name)

    def setup(self):
        src = self.path / 'src'
        obj = self.path / 'obj'
        mfile = src / 'main.c'
        hfile = input("Press enter if don't want header file created: ")
        sfile = ""
        makef = self.path / 'Makefile'
        src.mkdir()
        obj.mkdir()
        Path.touch(mfile)
        if hfile:
            hefile = src / (hfile + '.h')
            sefile = src / (hfile + '.c')
            Path.touch(hefile)
            Path.touch(sefile)
        with open(makef, 'w') as file:
            file.writelines(""" # auto-gen makefile

CC=clang
CFLAG=-Wall

main: main.o
    $(CC) $(CFLAG) -o $@ $^

%.o: %.c
    $(CC) $(CFLAG) -c $^ -o $@

clean:
    rm -f *.o main""")


class LangCpp(SetProject):
    """ further project setup for C++ language """

    def __init__(self, name='new-project'):
        super().__init__(name)

    def setup(self):
        src = self.path / 'src'
        obj = self.path / 'obj'
        mfile = src / 'main.cpp'
        hfile = input("Press enter if don't want header file created: ")
        sfile = ""
        makef = self.path / 'Makefile'
        src.mkdir()
        obj.mkdir()
        Path.touch(mfile)
        if hfile:
            hefile = src / (hfile + '.hpp')
            sefile = src / (hfile + '.cpp')
            Path.touch(hefile)
            Path.touch(sefile)
        with open(makef, 'w') as file:
            file.writelines(""" # auto-gen makefile

CC=clang++
CFLAG=-Wall -std=c++14

main: main.o
    $(CC) $(CFLAG) -o $@ $^

%.o: %.c
    $(CC) $(CFLAG) -c $^ -o $@

clean:
    rm -f *.o main""")


class LangJava(SetProject):
    """ further project setup for C language """

    def __init__(self, name='new-project'):
        super().__init__(name)

    def __writeToFiles(self):
        for gotFile in self.dsrc.rglob("*.java"):
            with open(gotFile, 'w') as file:
                if gotFile.stem == "Main":
                    file.writelines(f"""package com.{self.packageName.stem};

public class {gotFile.stem} {{
    public static void main(String ...args) {{
        /** code */
    }}
}}""")
                else:
                    file.writelines(f"""package com.{self.packageName.stem};

class {gotFile.stem} {{
        /** code */
}}""")

    def setup(self):
        self.dsrc = self.path / 'src'
        self.dbin = self.path / 'bin'
        self.packageName = input("Package Name [if not provided, default will be hostname]: ")
        if not self.packageName:
            self.packageName = self.dsrc / ('com') / uname()[1]
        else:
            self.packageName = self.dsrc / ('com') / self.packageName
        className = list()
        try:
            count = int(input('Number of class files(except Main.java): '))
        except ValueError as ve:
            print("Enter correct values: " + ve)
        else:
            for x in range(count):
                className.append(input(str(x + 1) + ": "))
            choice = input("Separate Main.java? [y/n]: ")
            if choice == 'y':
                className.append('Main')
            if len(className) > 0:
                self.dbin.mkdir()
                self.packageName.mkdir(parents=True)
                for classfile in className:
                    Path.touch(self.packageName / (classfile + ".java"))
                if choice == 'y':
                    Path.touch(self.packageName / 'Main.java')
                LangJava.__writeToFiles(self)
            else:
                print("Error: There must atleast on class file")
                self.path.rmdir()
                exit(2)


class LangPython(SetProject):
    """ further project setup for Python language """

    def __init__(self, name='new-project'):
        super().__init__(name)

    def setup(self):
        choiceVenv = input("Want virtualenv setup for python? [y/n]: ")
        if choiceVenv == "y":
            directory = input('Enter dir name(blank for current dir): ')
            if directory:
                subprocess.run(['virtualenv', '-p', 'python3', directory])
                self.path = self.path / directory
            else:
                subprocess.run(['virtualenv', '-p', 'python3', self.path])
        else:
            print('Not setting virtualenv')
        self.path = self.path / self.path.stem
        src = self.path / 'src'
        src.mkdir(parents=True)
        Path.touch(src / 'app.py')
        if input("Want to have main.py for project? [y/n]: "):
            Path.touch(self.path / 'main.py')
        Path.touch(self.path / 'README.md')
        with open(self.path / 'setup.py', 'w') as file:
            file.writelines(f"""from setuptools import find_packages, setup
from os import path

def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()

setup(
    name='<put-project-name-here>',
    version='1.0',
    packages=find_packages('{self.path.stem}'),
    description='<provide-project-description>',
    author='<name-here>',
    author_email='author@xyz.com',
    platform='<platform-here>',
    keywords="",
    long_description=read('README.md'),
    install_requires=[
    ],
    entry_points={{
        'console_scripts': [
        ],
    }},
)""")

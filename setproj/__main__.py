# system modules

from sys import exit
import subprocess
from pathlib import Path

# third-party module
import click

# project module
import setproj
from setproj import langSetup

# TODO:
# see that if click provides a way to only accept provided values for a argument(like argparse)
# else/also envolve supported languages in help
# see, if you can have globbing with filenames like for java, java8 or java11 both should be accepted and checked

@click.command()
@click.option('--language', '-l', prompt='Input Language', help='Enter the programming language to setup project for')
@click.option('--name', '-n', prompt='Input Project Name', help='Provide the name of project')
@click.option('--gitit', '-g', is_flag=True, help='Want git setup?')
def main(language, name, gitit):
    '''Project Setup Helper:

    Current Language Support:

    [C, C++, Java, Java-Servlet, Python, Web-Designing]

    You can provide '-g' or '--gitit' flag to initialize git inside the project of yours.

    You'll be provided option to select compiler for C/C++ projects.
    Default compiler for 'C' will be "cc" which is generally an aliased form of "gcc" in linux.
    For 'C++' will be 'g++'
    '''

    ifProjectExists(name)

    if language.lower() == 'c':
        print("project setup for C language, named: {}".format(name))
        langs = langSetup.LangC(name)
        langs.setup()
    elif language.lower() in ["cpp", "c++"]:
        print("project setup for C++ language, named: {}".format(name))
        langs = langSetup.LangCpp(name)
        langs.setup()
    elif language.lower() == "java":
        print("project setup for Java language, named: {}".format(name))
        langs = langSetup.LangJava(name)
        langs.setup()
    elif language.lower() == "python":
        print("project setup for Python language, named: {}".format(name))
        langs = langSetup.LangPython(name)
        langs.setup()
    elif language.lower() == "webd":
        print("project setup for Web Designing, named: {}".format(name))
        langs = langSetup.LangWebD(name)
        langs.setup()
    elif language.lower() in ["servlet", "java-servlet", "servlet-java"]:
        print("project setup for Java Servlet, named: {}".format(name))
        langs = langSetup.LangServlet(name)
        langs.setup()
    else:
        print("Language not supported or not correct language name")
        exit(2)
    extraSetup(name, gitit)


def ifProjectExists(projectPath):
    """ check if project user is trying to create already exists """
    projectPath = Path.cwd() / projectPath
    if Path.is_dir(projectPath):
        print("Project already exists in current directory")
        createAgain = input("Do you want to create another project with another name[y/n]? ")
        if createAgain == 'y':
            main()
        else:
            print("Exiting !!!")
            exit(1)


def extraSetup(dirname, isgit):
    """additional setup"""
    if isgit:
        subprocess.run(["git", "init"], cwd=dirname)
        subprocess.run(["git", "add", "*"], cwd=dirname)
        subprocess.run(["git", "commit", "-m", "'initial commit'"], cwd=dirname)


if __name__ == "__main__":
    main()

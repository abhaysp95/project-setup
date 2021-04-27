# system modules

from sys import exit
import subprocess
from pathlib import Path

# third-party module
import click

# project module
import setproj
from setproj import langSetup
from setproj import __version__

# TODO:
# see that if click provides a way to only accept provided values for a argument(like argparse)
# else/also envolve supported languages in help
# see, if you can have globbing with filenames like for java, java8 or java11 both should be accepted and checked

@click.command()
@click.option('--gitit', '-g', is_flag=True, help='Want git setup?')
@click.option('--version', '-v', is_flag=True, help='gives version')
def main(gitit, version):
    '''Project Setup Helper:

    Current Language Support:

    [C, C++, Java, Java-Servlet, Python, Web-Designing]

    You can provide '-g' or '--gitit' flag to initialize git inside the project of yours.

    You'll be provided option to select compiler for C/C++ projects.
    Default compiler for 'C' will be "cc" which is generally an aliased form of "gcc" in linux.
    For 'C++' will be 'g++'
    '''

    if version:
        giveVersion()
        exit(0)
    else:
        projectSetup(gitit)


def projectSetup(gitit):
    # take important entries
    name = input("Input project name[leave blank to cancel]: ")
    # if both entries entered by user
    if name:
        language = input("Input Language[leave blank to cancel]: ")
        if language:
            # check if project already exist
            ifProjectExists(name)
            if language.lower() == 'c':
                print("Project setup for C language, named: {}".format(name))
                langs = langSetup.LangC(name)
                langs.setup()
            elif language.lower() in ["cpp", "c++"]:
                print("Project setup for C++ language, named: {}".format(name))
                langs = langSetup.LangCpp(name)
                langs.setup()
            elif language.lower() == "java":
                print("Project setup for Java language, named: {}".format(name))
                langs = langSetup.LangJava(name)
                langs.setup()
            elif language.lower() == "python":
                print("Project setup for Python language, named: {}".format(name))
                langs = langSetup.LangPython(name)
                langs.setup()
            elif language.lower() == "webd":
                print("Project setup for Web Designing, named: {}".format(name))
                langs = langSetup.LangWebD(name)
                langs.setup()
            elif language.lower() in ["servlet", "java-servlet", "servlet-java"]:
                print("Project setup for Java Servlet, named: {}".format(name))
                langs = langSetup.LangServlet(name)
                langs.setup()
            elif language.lower() in ["javafx", "JavaFX", "JavaFx"]:
                print("Project setup for JavaFX, named: {}".format(name))
                langs = langSetup.LangJavaFx(name)
                langs.setup()
                langs.doFurtherSetup()
            else:
                print("Language not supported or not correct language name")
                exit(2)
            extraSetup(name, gitit)
    else:
        print("Exiting !!!")
        exit(1)


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


def giveVersion():
    __version = "not provided"
    try:
        __version = __version__.returnVersion()
    except (NameError, ValueError):
        pass
    finally:
        print(f"""setproj (SETPROJ), version: {__version}
This is a free software; licensed under "MIT License" """)


if __name__ == "__main__":
    main()

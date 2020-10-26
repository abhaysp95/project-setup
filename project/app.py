import click
from project import langSetup

# TODO:
# see that if click provides a way to only accept provided values for a argument(like argparse)
# else/also envolve supported languages in help
# see, if you can have globbing with filenames like for java, java8 or java11 both should be accepted and checked

@click.command()
@click.option('--language', '-l', prompt='Input Language', help='Enter the programming language to setup project for')
@click.option('--name', '-n', prompt='Input Project Name', help='Provide the name of project')
@click.option('--gitit', '-g', is_flag=True, help='Want git setup?')
def main(language, name, gitit):
    ''' This here is the help for making project '''

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
    if gitit:
        print('initializing git setup')
    else:
        print('no git setup')

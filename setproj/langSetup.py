from pathlib import Path
from os import uname
from sys import exit
import subprocess
import re

# TODO:
# see, if you can activate virtualenv
# for JavaFX, check if the distro have rsync installed if not install it
# (requires for update_files.sh) and 'entr' too

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
        self.mfile = None
        self.hfile = None
        self.makef = None
        self.sefile = ''
        self.hefile = ''
        self.compiler = None

    def __writeToFiles(self):
        """write some initial data to files"""
        with open(self.mfile, 'w') as file:
            file.writelines(f"""// main file

#include <stdio.h>

int main(int argc, char **argv) {{
\t/* code here */
\treturn 0;
}}""")

        try:
            with open(self.hefile, 'w') as file:
                file.write("#pragma once")
            with open(self.sefile, 'w') as file:
                file.write(f"#include \"../inc/{self.hefile.stem}.h\"")
        except AttributeError:
            pass
        except FileNotFoundError:
            pass
        with open(self.makef, 'w') as file:
            file.writelines(f"""# /* --- Makefile --- */

CC     = {self.compiler}
CFLAG  = -Wall -std=c99
CDFLAG = -Wall -std=c99 -g
LD     = {self.compiler}
LFLAG  = -v


SRC_DIR   = src
OBJ_DIR   = obj
INC_DIR   = inc
BIN_DIR   = bin
DEBUG_DIR = debug
DIRS      = ${{BIN_DIR}} ${{OBJ_DIR}} ${{DEBUG_DIR}}


SRC       = $(wildcard ${{SRC_DIR}}/*.c)
OBJ       = $(addprefix ${{OBJ_DIR}}/, $(notdir ${{SRC:.c=.o}}))
BIN       = ${{BIN_DIR}}/$(notdir $(realpath .))
DEBUG_OBJ = $(addprefix ${{DEBUG_DIR}}/, $(notdir ${{SRC:.c=.o}}))
DEBUG_BIN = $(addprefix ${{DEBUG_DIR}}/, $(notdir $(realpath .)))


all: dir ${{BIN}}

dir:
\tmkdir -p ${{DIRS}}


${{OBJ_DIR}}/%.o: ${{SRC_DIR}}/%.c
\t-@echo "compiling $? -> $@"
\t${{CC}} ${{CFLAG}} -I ${{INC_DIR}} -c -o $@ $^

${{BIN}}: ${{OBJ}}
\t-@echo "Linking $? -> $@"
\t${{LD}} ${{LFLAG}} -o $@ ${{OBJ_DIR}}/*.o
\t-@echo "copied ${{BIN}} -> $(notdir $(realpath .))"
\tcp -f ${{BIN}} .


debug: dir ${{DEBUG_BIN}}

${{DEBUG_DIR}}/%.o: ${{SRC_DIR}}/%.c
\t-@echo "compiling $? -> $@"
\t${{CC}} ${{CDFLAG}} -I ${{INC_DIR}} -c -o $@ $^

${{DEBUG_BIN}}: ${{DEBUG_OBJ}}
\t-@echo "Linking to -> $@"
\t${{LD}} ${{LFLAG}} -o $@ ${{DEBUG_DIR}}/*.o


clean:
\trm -rf ${{DIRS}} $(notdir $(realpath .))

.SILENT:
.PHONY: all dir debug clean""")

    def setup(self):
        src = self.path / 'src'
        obj = self.path / 'obj'
        inc = self.path / 'inc'
        self.mfile = src / 'main.c'
        self.hfile = input("Press enter if don't want header file created: ")
        self.makef = self.path / 'Makefile'
        src.mkdir()
        Path.touch(self.mfile)
        if self.hfile:
            inc.mkdir()
            self.hefile = inc / (self.hfile + '.h')
            self.sefile = src / (self.hfile + '.c')
            Path.touch(self.hefile)
            Path.touch(self.sefile)
        self.compiler = input("Select compiler[defualt to clang]: ")
        if not self.compiler:
            self.compiler = "clang"
        LangC.__writeToFiles(self)



class LangCpp(SetProject):
    """ further project setup for C++ language """

    def __init__(self, name='new-project'):
        super().__init__(name)
        self.mfile = None
        self.hfile = None
        self.makef = None
        self.sefile = ''
        self.hefile = ''
        self.compiler = None

    def __writeToFiles(self):
        """write some initial data to files"""
        with open(self.mfile, 'w') as file:
            file.writelines(f"""// main file

#include <iostream>

int main(int argc, char **argv) {{
\t/* code here */
\treturn 0;
}}""")

        try:
            with open(self.hefile, 'w') as file:
                file.write("#pragma once")
            with open(self.sefile, 'w') as file:
                file.write(f"#include \"../inc/{self.hefile.stem}.hpp\"")
        except AttributeError:
            pass
        except FileNotFoundError:
            pass
        with open(self.makef, 'w') as file:
            file.writelines(f"""# /* --- Makefile --- */

CC     = {self.compiler}
CFLAG  = -Wall -std=c++14
CDFLAG = -Wall -std=c++14 -g
LD     = {self.compiler}
LFLAG  = -v


SRC_DIR   = src
OBJ_DIR   = obj
INC_DIR   = inc
BIN_DIR   = bin
DEBUG_DIR = debug
DIRS      = ${{BIN_DIR}} ${{OBJ_DIR}} ${{DEBUG_DIR}}


SRC       = $(wildcard ${{SRC_DIR}}/*.cpp)
OBJ       = $(addprefix ${{OBJ_DIR}}/, $(notdir ${{SRC:.cpp=.o}}))
BIN       = ${{BIN_DIR}}/$(notdir $(realpath .))
DEBUG_OBJ = $(addprefix ${{DEBUG_DIR}}/, $(notdir ${{SRC:.cpp=.o}}))
DEBUG_BIN = $(addprefix ${{DEBUG_DIR}}/, $(notdir $(realpath .)))


all: dir ${{BIN}}

dir:
\tmkdir -p ${{DIRS}}


${{OBJ_DIR}}/%.o: ${{SRC_DIR}}/%.cpp
\t-@echo "compiling $? -> $@"
\t${{CC}} ${{CFLAG}} -I ${{INC_DIR}} -c -o $@ $^

${{BIN}}: ${{OBJ}}
\t-@echo "Linking $? -> $@"
\t${{LD}} ${{LFLAG}} -o $@ ${{OBJ_DIR}}/*.o
\t-@echo "copied ${{BIN}} -> $(notdir $(realpath .))"
\tcp -f ${{BIN}} .


debug: dir ${{DEBUG_BIN}}

${{DEBUG_DIR}}/%.o: ${{SRC_DIR}}/%.cpp
\t-@echo "compiling $? -> $@"
\t${{CC}} ${{CDFLAG}} -I ${{INC_DIR}} -c -o $@ $^

${{DEBUG_BIN}}: ${{DEBUG_OBJ}}
\t-@echo "Linking to -> $@"
\t${{LD}} ${{LFLAG}} -o $@ ${{DEBUG_DIR}}/*.o


clean:
\trm -rf ${{DIRS}}

.SILENT:
.PHONY: all dir debug clean""")

    def setup(self):
        src = self.path / 'src'
        obj = self.path / 'obj'
        inc = self.path / 'inc'
        self.mfile = src / 'main.cpp'
        self.hfile = input("Press enter if don't want header file created: ")
        self.makef = self.path / 'Makefile'
        src.mkdir()
        Path.touch(self.mfile)
        if self.hfile:
            inc.mkdir()
            self.hefile = inc / (self.hfile + '.hpp')
            self.sefile = src / (self.hfile + '.cpp')
            Path.touch(self.hefile)
            Path.touch(self.sefile)
        self.compiler = input("Enter compiler[defualt is clang++]: ")
        if not self.compiler:
            self.compiler = "clang++"
        LangCpp.__writeToFiles(self)


class LangJava(SetProject):
    """ further project setup for Java language """

    def __init__(self, name='new-project'):
        super().__init__(name)
        self.dsrc = self.path / 'src'
        self.dbin = self.path / 'bin'
        self.packageName = None
        self.packageDir = None

    def __writeToFiles(self):
        for gotFile in self.dsrc.rglob("*.java"):
            with open(gotFile, 'w') as file:
                if gotFile.stem == "Main":
                    file.writelines(f"""package com.{self.packageName.replace('/', '.')};

public class {gotFile.stem} {{
\tpublic static void main(String ...args) {{
\t\t/** code */
\t}}
}}""")
                else:
                    file.writelines(f"""package com.{self.packageName.replace('/', '.')};

class {gotFile.stem} {{
\t\t/** code */
}}""")

    def setup(self):
        self.dsrc = self.path / 'src'
        self.dbin = self.path / 'bin'
        self.packageName = input("Package Name [if not provided, default will be hostname]: ")
        if not self.packageName:
            self.packageDir = self.dsrc / ('com') / uname()[1]
            self.packageName = uname()[1]
        else:
            self.packageDir = self.dsrc / ('com') / self.packageName
        className = list()
        try:
            count = int(input('Number of class files(except Main.java)[Enter 0 if none]: '))
        except ValueError as ve:
            print("Enter correct values: " + ve)
        else:
            for x in range(count):
                gotClassName = input(str(x + 1) + ": ")
                if gotClassName.islower():
                    className.append(gotClassName.title())
                else:
                    className.append(gotClassName)
            choice = input("Separate Main.java? [y/n]: ")
            if choice == 'y':
                className.append('Main')
            if len(className) > 0:
                self.dbin.mkdir()
                self.packageDir.mkdir(parents=True)
                for classfile in className:
                    Path.touch(self.packageDir / (classfile + ".java"))
                if choice == 'y':
                    Path.touch(self.packageDir / 'Main.java')
                LangJava.__writeToFiles(self)
            else:
                print("Error: There must atleast on class file")
                self.path.rmdir()
                print("Exiting !!!")
                exit(2)


class LangJavaFx(LangJava):
    """further project setup for JavaFx(suitable for terminal development)"""

    def __init__(self, name="new_project"):
        super().__init__(name)
        self.fxmlFile = None
        self.cssFile = None
        self.scenebuilderPos = "/opt/SceneBuilder/app"
        self.updateScript = self.dsrc / "update_files.sh"
        self.module = self.dsrc / "module-info.java"
        self.javaFiles = list()

    def __getJavaFiles(self):
        for file in self.dsrc.rglob("*.java"):
            self.javaFiles.append(file)
        print(self.javaFiles)

    def __writeToFiles(self):
        # for gotFile in self.dsrc.rglob("*.java"):
        for gotFile in self.javaFiles:
            with open(gotFile, "w") as file:
                if gotFile.stem == "Main":
                    if not self.fxmlFile:
                        file.writelines(f"""package com.{self.packageName.replace('/', '.')};

import javafx.application.Application;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.scene.layout.GridPane;

public class {gotFile.stem} extends Application {{

\t@Override
\tpublic void start(Stage primaryStage) throws Exception {{
\t\tGridPane root = new GridPane();
\t\tprimaryStage.setTitle("{self.projName}");
\t\tprimaryStage.setScene(new Scene(root, 400, 400));
\t\tprimaryStage.show();
\t}}
\tpublic static void main(String ...args) {{
\t\tlaunch(args);
\t}}
}}""")
                    else:
                        file.writelines(f"""package com.{self.packageName.replace('/', '.')};

import javafx.application.Application;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.scene.Parent;
import javafx.fxml.FXMLLoader;

public class {gotFile.stem} extends Application {{

\t@Override
\tpublic void start(Stage primaryStage) throws Exception {{
\t\tParent root = FXMLLoader.load(getClass().getResource("/com/{self.packageName}/{self.fxmlFile}.fxml"));
\t\tprimaryStage.setTitle("{self.projName}");
\t\tprimaryStage.setScene(new Scene(root, 400, 400));
\t\tprimaryStage.show();
\t}}
\tpublic static void main(String ...args) {{
\t\tlaunch(args);
\t}}
}}""")
                # going to be Controller or some other java files
                else:
                    file.writelines(f"""package com.{self.packageName.replace('/', '.')};

public class {gotFile.stem} {{
\t/** code here */
}}""")
        # basic setup for fxml files
        isControllerAvailable = False
        controllerName = ""
        for gotFile in self.dsrc.rglob("*.fxml"):
            for file in self.javaFiles:
                res = re.match(r".*/\.?(.*[cC]ontroller.*)\..*$", str(file))
                if res:
                    isControllerAvailable = True
                    controllerName = res.group(1)
            if controllerName != "":
                controllerName = "com." + self.packageName.replace('/', '.') + '.' + controllerName
            with open(gotFile, 'w') as file:
                file.writelines(f"""<?import javafx.geometry.Insets?>
<?import javafx.scene.layout.GridPane?>

<GridPane fx:controller="{controllerName}" xmlns:fx="http://javafx.com/fxml">
\t<!-- code here -->
</GridPane>""")
        # basic setup for css files
        for gotFile in self.dsrc.rglob("*.css"):
            with open(gotFile, 'w') as file:
                file.write("/* provide styling here */")
        if self.scenebuilderPos:
            if Path(self.scenebuilderPos).is_dir():
                with open(Path(self.scenebuilderPos + '/' + (self.fxmlFile + '.fxml')), 'w') as file:
                    file.writelines(f"""<?import javafx.geometry.Insets?>
<?import javafx.scene.layout.GridPane?>

<GridPane fx:controller="{controllerName}" xmlns:fx="http://javafx.com/fxml">
\t<!-- code here -->
</GridPane>""")
        with open(Path(self.module), 'w') as file:
            file.writelines(f"""/** module file for project */

module com.{self.packageName.replace('/', '.')} {{
\trequires javafx.fxml;
\trequires javafx.controls;

\topens com.{self.packageName.replace('/', '.')} to javafx.fxml, javafx.graphics;
}}""")
        # one of the two or both are required by user
        if self.fxmlFile or self.cssFile:
            with open(Path(self.updateScript), 'w') as file:
                # if fxmlFile is available and not css one
                if not self.cssFile:
                    file.writelines(f"""#!/usr/bin/env bash

# file: {Path(self.fxmlFile).stem}.fxml
# source: {self.scenebuilderPos}
# desitination: src and bin(module)
rsync -av {self.scenebuilderPos}/{Path(self.fxmlFile).stem}.fxml {self.dsrc}/com/{self.packageName}
rsync -av {self.scenebuilderPos}/{Path(self.fxmlFile).stem}.fxml {self.dbin}/com.{self.packageName.replace('/', '.')}/com/{self.packageName}

# file: {Path(self.fxmlFile).stem}.fxml
# source: src
# desitnation: scenebuilder pos. and bin(module)
rsync -a {self.dsrc}/com/{self.packageName}/{Path(self.fxmlFile).stem}.fxml {self.scenebuilderPos}
rsync -a {self.dsrc}/com/{self.packageName}/{Path(self.fxmlFile).stem}.fxml {self.dbin}/com.{self.packageName.replace('/', '.')}/com/{self.packageName}

# provide further sync details here""")
                # if css file is available and not fxml one
                elif not self.fxmlFile:
                    file.writelines(f"""#!/usr/bin/env bash

# file: {Path(self.cssFile).stem}.fxml
# source: src
# desitnation: scenebuilder pos. and bin(module)
rsync -a {self.dsrc}/com/{self.packageName}/{Path(self.cssFile).stem}.css {self.dbin}/com.{self.packageName.replace('/', '.')}/com/{self.packageName}

# provide further sync details here""")
                # if both fxml and css are required by user
                else:
                    file.writelines(f"""#!/usr/bin/env bash

# file: {Path(self.fxmlFile).stem}.fxml
# source: {self.scenebuilderPos}
# desitination: src and bin(module)
rsync -av {self.scenebuilderPos}/{Path(self.fxmlFile).stem}.fxml {self.dsrc}/com/{self.packageName}
rsync -av {self.scenebuilderPos}/{Path(self.fxmlFile).stem}.fxml {self.dbin}/com.{self.packageName.replace('/', '.')}/com/{self.packageName}

# file: {Path(self.fxmlFile).stem}.fxml
# source: src
# desitnation: scenebuilder pos. and bin(module)
rsync -a {self.dsrc}/com/{self.packageName}/{Path(self.fxmlFile).stem}.fxml {self.scenebuilderPos}
rsync -a {self.dsrc}/com/{self.packageName}/{Path(self.fxmlFile).stem}.fxml {self.dbin}/com.{self.packageName.replace('/', '.')}/com/{self.packageName}

# file: {Path(self.cssFile).stem}.fxml
# source: src
# desitnation: scenebuilder pos. and bin(module)
rsync -a {self.dsrc}/com/{self.packageName}/{Path(self.cssFile).stem}.css {self.dbin}/com.{self.packageName.replace('/', '.')}/com/{self.packageName}

# provide further sync details here""")

    def doFurtherSetup(self):
        self.fxmlFile = input("Enter the fxml file name[if not, leave blank]: ")
        self.cssFile = input("Enter the css file name[if not, leave blank]: ")
        print("Enter scenebuilder position")
        enteredSceneBuilderPos = input("[default: \"/opt/SceneBuilder/app\" | if not, leave blank]: ")
        if enteredSceneBuilderPos:
            self.scenebuilderPos = enteredSceneBuilderPos
        if self.fxmlFile:
            Path.touch(self.packageDir / (self.fxmlFile + ".fxml"))
        if self.cssFile:
            Path.touch(self.packageDir / (self.cssFile + ".css"))
        (self.dbin / ('com.' + self.packageName.replace('/', '.'))).mkdir()  # create module
        LangJavaFx.__getJavaFiles(self)
        LangJavaFx.__writeToFiles(self)
        # or just do 0o754
        if Path(self.updateScript).is_file():
            Path(self.updateScript).chmod(492)  # octal permission is 754(4 + 40 + 448)

class LangServlet(SetProject):
    """ further project setup for Java Servlet languages """

    def __init__(self, name='new-project'):
        super().__init__(name)
        self.packageName = None

    def __writeToFiles(self):
        with open(self.path / "index.html", 'w') as file:
            file.writelines(f"""<!DOCTYPE html>
<html>
\t<head></head>
\t<body>
\t\t<form action="" method="get">
\t\t</form>
\t</body>
</html>""")
        with open(self.path / 'WEB-INF' / 'web.xml', 'w') as file:
            file.writelines(f"""<web-app>
\t<servlet>
\t\t<servlet-name></servlet-name>
\t\t<servlet-class></servlet-class>
\t</servlet>
\t<servlet-mapping>
\t\t<servlet-name></servlet-name>
\t\t<url-pattern></url-pattern>
\t</servlet-mapping>
</web-app>""")
        for javafile in self.packageName.rglob("*.java"):
            with open(javafile, 'w') as file:
                file.writelines(f"""package com.{self.packageName.stem};

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.ServletException;

public class {javafile.stem.title()} extends HttpServlet {{
\tpublic void doGet(HttpServletRequest req, HttpServletResponse res) throws IOException, ServletException {{
\t\t/** code */
\t}}
}}""")


    def setup(self):
        src = self.path / 'src'
        classes = self.path / 'WEB-INF' / 'classes'
        findex = self.path / 'index.html'
        fwebxml = self.path / 'WEB-INF' / 'web.xml'
        self.packageName = input("Enter package name(hostname will be default package name): ")
        if self.packageName:
            self.packageName = src / ('com') / self.packageName
        else:
            self.packageName = src / ('com') / uname()[1]
        classfiles = list()
        create = False
        while not create:
            count = input("Count for class names[if single class then enter that class name]: ")
            if count.isdigit():
                print("Enter class names: ")
                for x in range(int(count)):
                    classfiles.append(self.packageName / ((input(str(x + 1) + ": ")).title() + ".java"))
                create = True
            elif count:
                classfiles.append(self.packageName / (count.title() + ".java"))
                create = True
            else:
                choice = input("Providing class file is necessary, Create again[y/n]: ")
                if not choice:
                    self.path.rmdir()
                    print("Entered nothing, Exiting !!!")
                    exit(2)
        if len(classfiles) > 0:
            src.mkdir()
            classes.mkdir(parents=True)
            self.packageName.mkdir(parents=True)
            Path.touch(findex)
            Path.touch(fwebxml)
            for classfile in classfiles:
                Path.touch(classfile)
                LangServlet.__writeToFiles(self)
        else:
            print("providing a class name is necessary")
            print("Exiting !!!")
            exit(2)


class LangPython(SetProject):
    """ further project setup for Python language """

    def __init__(self, name='new-project'):
        super().__init__(name)
        self.path = None

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


class LangWebD(SetProject):
    """ further project setup for Web Designing languages """

    def __init__(self, name='new-project'):
        super().__init__(name)

    def setup(self):
        index = self.path / 'index.html'
        style = self.path / 'style.css'
        script = self.path / 'script.js'
        extras = self.path / 'extras'
        Path.touch(index)
        Path.touch(style)
        Path.touch(script)
        extras.mkdir()
        with open(index, 'w') as file:
            file.writelines(f"""<!DOCTYPE html>
<html>
\t<head>
\t\t<meta charset="UTF-8">
\t\t<link type="text/css" rel="stylesheet" href="style.css">

\t\t<title>Enter title here</title>
\t</head>
\t<body>
\t\t<script src="app.js"></script>
\t</body>
</html>""")


if __name__ == "__main__":
    print("Not a standalone script")
    exit(1)

  #######################################################################

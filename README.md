# D3D-Printer-Workbench

## License
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

GNU Lesser General Public License (LGPL) version 3. See the file [COPYING.Lesser](COPYING.Lesser).

## Instructions

[Requirements slide deck](http://opensourceecology.org/wiki/D3D_Workbench_in_FreeCAD)

[Initial project overview video](https://www.youtube.com/watch?v=HadgIABxLv4)

[Python Style Guide](https://www.python.org/dev/peps/pep-0008/)

[Clone and install repo/workbench](https://www.freecadweb.org/wiki/How_to_install_additional_workbenches)

````
$ mkdir ~/.FreeCAD/Mod
$ cd ~/.FreeCAD/Mod
$ git clone https://github.com/skaiser/D3D-Printer-Workbench.git
````

Create a soft link in your home directory to make it easier to add things like icons from the file browser windows.

````
$ cd
$ ln -s ~/.FreeCAD/Mod/ .
````

## Useful API doc links

These are actually quite helpful:

[Scripting Basics](https://www.freecadweb.org/wiki/index.php?title=FreeCAD_Scripting_Basics)

[PySide (i.e., QtGui)](https://www.freecadweb.org/wiki/PySide)

[Python Scripting Tutorial](https://www.freecadweb.org/wiki/Python_scripting_tutorial)

Also...click Help->Automatic python modules documentation. This is probably what you really want after reading the basic scripting tutorials. 
However, the thing **I've found most helpful is using the interactive python console** as introduced in [Scripting Basics](https://www.freecadweb.org/wiki/index.php?title=FreeCAD_Scripting_Basics)

[Forum](https://forum.freecadweb.org/)

[Part Module](https://www.freecadweb.org/wiki/Part_Module)

[Part Scripting](https://www.freecadweb.org/wiki/Topological_data_scripting)

The [Category:API](https://www.freecadweb.org/wiki/Category:API) page has a more browseable list of API docs for a small set of modules than the main API index pages. FreeCAD and FreeCADGui are the main ones to took at, starting out.



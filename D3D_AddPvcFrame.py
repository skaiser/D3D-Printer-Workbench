#***************************************************************************
#*                                                                         *
#*  This file is part of the Open Source Ecology D3D 3D Printer Workbench  *
#*  for FreeCAD.                                                           *
#*                                                                         *
#*  Copyright (C) 2017                                                     *
#*  Open Source Ecology <info|at|opensourceecology.org>                    *
#*                                                                         *
#*  This library is free software; you can redistribute it and/or          *
#*  modify it under the terms of the GNU Lesser General Public             *
#*  License as published by the Free Software Foundation; either           *
#*  version 2 of the License, or (at your option) any later version.       *
#*                                                                         *            
#*  This library is distributed in the hope that it will be useful,        *
#*  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
#*  Lesser General Public License for more details.                        *
#*                                                                         *
#*  You should have received a copy of the GNU Lesser General Public       *
#*  License along with this library; if not, If not, see                   *
#*  <http://www.gnu.org/licenses/>.                                        *
#*                                                                         *
#*                                                                         *
#***************************************************************************

import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import D3DInit
from PySide import QtGui#, QtCore # https://www.freecadweb.org/wiki/PySide
import pipeGui, cornerGui
import PvcFrameGui

class D3D_AddPvcFrameClass():
    """Command to add the printer frame"""

    def GetResources(self):
        #App.ConfigGet('UserAppData') + '/Mod'
        return {'Pixmap'  : D3DInit.ICON_PATH + '/AddFrame.svg', # the name of a svg file available in the resources
                'Accel' : "Shift+S", # a default shortcut (optional)
                'MenuText': "Add a PVC frame",
                'ToolTip' : "Adds a D3D printer frame built from PVC pipes and fittings"}

    def Activated(self):
        if not(App.ActiveDocument):
            App.newDocument()

        doc = App.activeDocument()
	pipeTable = pipeGui.GuiCheckTable() # Open a CSV file, check its content, and return it as a CsvTable object.
	cornerTable = cornerGui.GuiCheckTable() # Open a CSV file, check its content, and return it as a CsvTable object.
	form = PvcFrameGui.MainDialog(doc, pipeTable, cornerTable)
	form.exec_()
        Gui.ActiveDocument.ActiveView.fitAll()
        doc.recompute()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

Gui.addCommand('D3D_AddPvcFrame', D3D_AddPvcFrameClass()) 

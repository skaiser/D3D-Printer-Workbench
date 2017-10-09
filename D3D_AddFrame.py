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

class D3D_AddFrameClass():
    """Command to add the printer frame"""

    def GetResources(self):
        #App.ConfigGet('UserAppData') + '/Mod'
        return {'Pixmap'  : D3DInit.ICON_PATH + '/DrawStyleWireFrame.svg', # the name of a svg file available in the resources
                'Accel' : "Shift+S", # a default shortcut (optional)
                'MenuText': "Add a frame",
                'ToolTip' : "Adds a D3D printer frame"}

    def Activated(self):
        "Command was selected"
        # See here for opening dialog to choose part to import 
        # https://github.com/hamish2014/FreeCAD_assembly2/blob/master/importPart.py#L125
        App.Console.PrintMessage("D3D Printer workbench is working!")
        if not(App.ActiveDocument):
            App.newDocument()
#        view = Gui.activeDocument().activeView()
        doc = App.activeDocument()
        printer_size = 12
        reply = QtGui.QInputDialog.getText(None, "Printer size", "How large is the printer (in inches)")
        if reply[1]:
            # user clicked OK
            printer_size = int(reply[0])
            App.Console.PrintMessage("Printer size will be " + str(printer_size) + " inches.")
        else:
            # user clicked Cancel
            App.Console.PrintMessage("Printer size will be 12 inches.")
        #FreeCAD.getDocument("D3D_Left_Z_Axis_Simple").getObject("Cylinder").Height = '406.4 mm'
        #FreeCAD.getDocument("D3D_Left_Z_Axis_Simple").getObject("Cylinder").Radius = '5.96875 mm'
        # Angle doesn't appear to do much with the rod itself
        # Axes may already be in the "correct" orientation!
        #App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
        #App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))
        #Gui.activeDocument().activeView().setCamera('#Inventor V2.1 ascii \n OrthographicCamera {\n viewportMapping ADJUST_CAMERA \n position 0 0 87 \n orientation 0 0 1  0 \n nearDistance -112.88701 \n farDistance 287.28702 \n aspectRatio 1 \n focalDistance 87 \n height 143.52005 }')
        #Gui.activeDocument().setEdit('Sketch')
        ##sk.getDatum('Constraint23')
        #App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',2,-506.400000))
        #App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Distance',5,2,2,50.800000)) 
        ########App.ActiveDocument.Sketch.setDatum(22,App.Units.Quantity('50.800000 mm'))
        
        #f.Geometry = [Part.Line(App.Vector(0,0,0),App.Vector(2,20,0)),Part.Line(App.Vector(0,0,0),App.Vector(20,2,0))]
        #f.Constraints = [Sketcher.Constraint('Vertical',0),Sketcher.Constraint('Horizontal',1)]
        #/usr/lib/freecad/Mod/Sketcher/SketcherExample.py
        #[d.FileName for d in App.listDocuments().values()][0]
        # TODO(kaisers): Don't open in a new document!
        #
        App.openDocument(D3DInit.__dir__ + '/Resources/cad/D3D_CAD_Assembly.fcstd')
        #ImportGui.insert(D3DInit.__dir__ + '/Resources/cad/D3D_X_Axis_Simple.step')
        #obj = doc.addObject("Part::FeaturePython", "X_Axis")
        # TODO(kaisers): Might need to use STEP files?
        #http://sliptonic.com/simple-assemblies-in-freecad/
        #obj.addProperty("App::PropertyFile", "sourceFile", "importPart").sourceFile = D3DInit.__dir__ + '/Resources/cad/D3D_X_Axis_Simple.fcstd'
        # TODO(kaisers): If first part
        #obj.addProperty("App::PropertyBool","fixedPosition","importPart")
        Gui.ActiveDocument.ActiveView.fitAll()
        doc.recompute()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

Gui.addCommand('D3D_AddFrame', D3D_AddFrameClass()) 

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

import os
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import D3DInit
from PySide import QtGui, QtCore # https://www.freecadweb.org/wiki/PySide

def importPart(filename):
    doc_assembly = App.ActiveDocument
    App.Console.PrintMessage("importing part from %s\n" % filename)
    
    doc_already_open = filename in [ d.FileName for d in App.listDocuments().values() ]
    App.Console.PrintMessage("%s open already %s" % (filename, doc_already_open))
    
    if doc_already_open:
        doc = [ d for d in App.listDocuments().values() if d.FileName == filename][0]
    else:
        if filename.lower().endswith('.fcstd'):
            App.Console.PrintMessage('opening %s' % filename)
            doc = App.openDocument(filename)
            App.Console.PrintMessage('succesfully opened %s' % filename)
        else: #trying shaping import http://forum.freecadweb.org/viewtopic.php?f=22&t=12434&p=99772#p99772x
            import ImportGui
            doc = App.newDocument( os.path.basename(filename) )
            shapeobj=ImportGui.insert(filename,doc.Name)
    
    visibleObjects = [ obj for obj in doc.Objects
                       if hasattr(obj,'ViewObject') and obj.ViewObject.isVisible()
                       and hasattr(obj,'Shape') and len(obj.Shape.Faces) > 0 and 'Body' not in obj.Name] # len(obj.Shape.Faces) > 0 to avoid sketches, skip Body
    App.Console.PrintMessage('Visible objects %s' % visibleObjects)
    
    obj = doc_assembly.addObject("Part::FeaturePython", 'part123456')
    obj.addProperty("App::PropertyFile", "sourceFile", "D3D_ImportPart").sourceFile = filename
    obj.addProperty("App::PropertyFloat", "timeLastImport", "D3D_ImportPart")
    obj.setEditorMode("timeLastImport", 1)
    obj.addProperty("App::PropertyBool", "fixedPosition", "D3D_ImportPart")
    obj.fixedPosition = not any([i.fixedPosition for i in doc_assembly.Objects if hasattr(i, 'fixedPosition') ])
    #obj.addProperty("App::PropertyBool", "updateColors", "importPart").updateColors = True
    obj_to_copy  = visibleObjects[0]
    obj.Shape = obj_to_copy.Shape.copy()
    
    obj.Proxy = Proxy_importPart()
    obj.timeLastImport = os.path.getmtime( filename )
    #clean up
    #if subAssemblyImport:
    #    doc_assembly.removeObject(tempPartName)
    if not doc_already_open: #then close again
        App.closeDocument(doc.Name)
        App.setActiveDocument(doc_assembly.Name)
        App.ActiveDocument = doc_assembly
    return obj
    
class Proxy_importPart:
    def execute(self, shape):
        pass
    
class D3D_ImportPartCommand:
    def Activated(self):
        if Gui.ActiveDocument == None:
            App.newDocument()
        view = Gui.activeDocument().activeView()
        #filename, filetype = QtGui.QFileDialog.getOpenFileName(
        #    QtGui.qApp.activeWindow(),
        #    "Select FreeCAD document to import part from",
        #    "",# "" is the default, os.path.dirname(FreeCAD.ActiveDocument.FileName),
        #    "FreeCAD Document (*.fcstd)"
        #    )
        dialog = QtGui.QFileDialog(
            QtGui.qApp.activeWindow(),
            "Select FreeCAD document to import part from"
            )
        dialog.setNameFilter("Supported Formats (*.FCStd *.brep *.brp *.imp *.iges *.igs *.obj *.step *.stp);;All files (*.*)")
        if dialog.exec_():
            filename = dialog.selectedFiles()[0]
        else:
            return
        App.Console.PrintMessage(filename)
        importedObject = importPart(filename)
        App.ActiveDocument.recompute()

    def GuiViewFit(self):
        Gui.SendMsgToActiveView("ViewFit")
        self.timer.stop()

    def GetResources(self):
        return {
            'Pixmap' : D3DInit.ICON_PATH + '/DrawStyleWireFrame.svg',
            'MenuText': 'Import a part from another FreeCAD document',
            'ToolTip': 'Import a part from another FreeCAD document'
            }
Gui.addCommand('D3D_ImportPart', D3D_ImportPartCommand())
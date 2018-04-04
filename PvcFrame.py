# -*- coding: utf-8 -*-
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
# Author: Ruslan Krenzler.
# Date: 11 February 2018
# Create a pipe frame box.

import math
import csv
import os.path

import FreeCAD
import Part
import Draft

import OSEBase
from piping import *
import corner as cornermod
import pipe as pipemod

parseQuantity = FreeCAD.Units.parseQuantity

# This version of the macro does not create corners.
DIMENSIONS_USED = ["G", "LX", "LY", "LZ", "POD", "PID"] 

# It must contain unique values in the column "Name" and also, dimensions listened below.
PIPE_DIMENSIONS_USED = ["ID", "OD"]
CORNER_DIMENSIONS_USED = ["G", "H", "M", "POD", "PID"]

class Error(Exception):
	"""Base class for exceptions in this module."""
	def __init__(self, message):
		super(Error, self).__init__(message)

class UnplausibleDimensions(Error):
	"""Exception raised when dimensions are unplausible. For example if
	outer diameter is larger than the inner one.

	Attributes:
	message -- explanation of the error
	"""

	def __init__(self, message):
		super(UnplausibleDimensions, self).__init__(message)


class Box:
	def __init__(self, document):
		self.document = document
		self.G = parseQuantity("2 cm")
		self.LX = parseQuantity("30 cm")
		self.LY = parseQuantity("20 cm")
		self.LZ = parseQuantity("25 in")
		self.POD = parseQuantity("3 cm")
		self.Thk = parseQuantity("0.5 cm")
		self.corner = cornermod.Corner(document)
		
	def checkDimensions(self):
		if not ( self.POD > parseQuantity("0 mm") and self.Thk > parseQuantity("0 mm") ):
			raise UnplausibleDimensions("Pipe dimensions must be positive. They are POD=%s and Thk=%s instead"%(self.POD, self.PID))
		if not (self.LX > 2*self.G):
			raise UnplausibleDimensions("The length LX %smust be larger than 2*G %s"%(self.LX, 2*self.G))
		if not (self.LY > 2*self.G):
			raise UnplausibleDimensions("The length LY %smust be larger than 2*G %s"%(self.LY, 2*self.G))
		if not (self.LZ > 2*self.G):
			raise UnplausibleDimensions("The length LZ %smust be larger than 2*G %s"%(self.LZ, 2*self.G))
	
	def createPipes(self, group, convertToSolid):
		# Calculate pipe lengths.
		x_pipe_l = self.LX - 2*self.G
		y_pipe_l = self.LY - 2*self.G
		z_pipe_l = self.LZ - 2*self.G
		# First 3 pipes around the (0,0,0) origin in X,Y,Z direction
		pipe = pipemod.Pipe(self.document)
		pipe.OD = self.POD
		pipe.Thk = self.Thk
		pipe.H = z_pipe_l
		zpipe = pipe.create(convertToSolid)
		group.addObject(zpipe)
		zpipe.Placement.Base = FreeCAD.Vector(0,0,self.G)
		zpipe.Label = "z-"+zpipe.Label
		pipe.H = x_pipe_l
		xpipe = pipe.create(convertToSolid)
		group.addObject(xpipe)
		xpipe.Placement = FreeCAD.Placement(FreeCAD.Vector(self.G, 0,0), FreeCAD.Rotation(FreeCAD.Vector(0,1,0),90), FreeCAD.Vector(0,0,0))
		xpipe.Label = "x-"+xpipe.Label
		pipe.H = y_pipe_l
		ypipe = pipe.create(convertToSolid)
		group.addObject(ypipe)
		ypipe.Placement = FreeCAD.Placement(FreeCAD.Vector(0, self.G,0), FreeCAD.Rotation(FreeCAD.Vector(1,0,0),-90), FreeCAD.Vector(0,0,0))
		ypipe.Label = "y-"+ypipe.Label

		# Add 3 clones for each x,y,z-type of axis. Place them on the edges of the cube.
		# First add z-pipes (because it simple, and does not require rotation).
		tmp = Draft.clone(zpipe, FreeCAD.Vector(self.LX,0,self.G))
		group.addObject(tmp)
		tmp = Draft.clone(zpipe, FreeCAD.Vector(0, self.LY,self.G))
		group.addObject(tmp)
		tmp = Draft.clone(zpipe, FreeCAD.Vector(self.LX, self.LY,self.G))
		group.addObject(tmp)
		# Then add x pipes.
		tmp = Draft.clone(xpipe)
		group.addObject(tmp)
		tmp.Placement = FreeCAD.Placement(FreeCAD.Vector(self.G, self.LY, 0), FreeCAD.Rotation(FreeCAD.Vector(0,1,0),90), FreeCAD.Vector(0,0,0))
		tmp = Draft.clone(xpipe)
		group.addObject(tmp)
		tmp.Placement = FreeCAD.Placement(FreeCAD.Vector(self.G, 0, self.LZ), FreeCAD.Rotation(FreeCAD.Vector(0,1,0),90), FreeCAD.Vector(0,0,0))
		tmp = Draft.clone(xpipe)
		group.addObject(tmp)
		tmp.Placement = FreeCAD.Placement(FreeCAD.Vector(self.G, self.LY, self.LZ), FreeCAD.Rotation(FreeCAD.Vector(0,1,0),90), FreeCAD.Vector(0,0,0))
		# Finally add y pipes.
		tmp = Draft.clone(ypipe)
		group.addObject(tmp)
		tmp.Placement = FreeCAD.Placement(FreeCAD.Vector(self.LX, self.G, 0), FreeCAD.Rotation(FreeCAD.Vector(1,0,0),-90), FreeCAD.Vector(0,0,0))
		tmp = Draft.clone(ypipe)
		group.addObject(tmp)
		tmp.Placement = FreeCAD.Placement(FreeCAD.Vector(0, self.G, self.LZ), FreeCAD.Rotation(FreeCAD.Vector(1,0,0),-90), FreeCAD.Vector(0,0,0))
		tmp = Draft.clone(ypipe)
		group.addObject(tmp)
		tmp.Placement = FreeCAD.Placement(FreeCAD.Vector(self.LX, self.G, self.LZ), FreeCAD.Rotation(FreeCAD.Vector(1,0,0),-90), FreeCAD.Vector(0,0,0))

	def addCorners(self, group, convertToSolid):
		corner = self.corner.create(convertToSolid)
		group.addObject(corner)
		# clone the corners and put them on right positions.
		tmp = Draft.clone(corner)
		group.addObject(tmp)
		tmp.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, self.LZ), FreeCAD.Rotation(FreeCAD.Vector(0,1,0),90), FreeCAD.Vector(0,0,0))
		tmp = Draft.clone(corner)
		group.addObject(tmp)
		tmp.Placement = FreeCAD.Placement(FreeCAD.Vector(self.LX,0, self.LZ), FreeCAD.Rotation(FreeCAD.Vector(0,1,0),180), FreeCAD.Vector(0,0,0))
		tmp = Draft.clone(corner)
		group.addObject(tmp)
		tmp.Placement = FreeCAD.Placement(FreeCAD.Vector(self.LX,0,0), FreeCAD.Rotation(FreeCAD.Vector(0,1,0),270), FreeCAD.Vector(0,0,0))

		tmp = Draft.clone(corner)
		group.addObject(tmp)
		tmp.Placement = FreeCAD.Placement(FreeCAD.Vector(self.LX,self.LY,0), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),180), FreeCAD.Vector(0,0,0))
		tmp = Draft.clone(corner)
		group.addObject(tmp)
		tmp.Placement = FreeCAD.Placement(FreeCAD.Vector(0,self.LY,0), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),270), FreeCAD.Vector(0,0,0))

		tmp = Draft.clone(corner)
		group.addObject(tmp)
		tmp.Placement = FreeCAD.Placement(FreeCAD.Vector(0,self.LY, self.LZ), FreeCAD.Rotation(FreeCAD.Vector(1,0,0),180), FreeCAD.Vector(0,0,0))
		tmp = Draft.clone(corner)
		group.addObject(tmp)
		# First rotation.
		tmp.Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,0), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),180), FreeCAD.Vector(0,0,0))
		# Second rotation + shift.
		tmp.Placement = FreeCAD.Placement(FreeCAD.Vector(self.LX,self.LY, self.LZ), FreeCAD.Rotation(FreeCAD.Vector(1,0,0),90), FreeCAD.Vector(0,0,0)).multiply(tmp.Placement)
		
	def create(self, convertToSolid):
		self.checkDimensions()
		group = self.document.addObject("App::DocumentObjectGroup", "frame box group")
		self.createPipes(group, convertToSolid)
		self.addCorners(group, convertToSolid)
		return group


class BoxFromTable:
	"""Create a part with dimensions from a CSV table."""
	def __init__ (self, document, pipe_table, corner_table):
		self.document = document
		self.pipe_table = pipe_table
		self.corner_table = corner_table
		# Set some test values. Replace them by custom values
		# before to call BoxFromTable.create().
		self.LX = parseQuantity("12 in")
		self.LY = parseQuantity("10 in")
		self.LZ = parseQuantity("8 in")

	def getCorner(self, partName):
		corner = cornermod.Corner(self.document)
		row = self.corner_table.findPart(partName)
		if row is None:
			print('Corner part "%s" not found'%partName)
			return
		corner.G = parseQuantity(row["G"])
		corner.H = parseQuantity(row["H"])
		corner.M = parseQuantity(row["M"])
		corner.POD = parseQuantity(row["POD"])
		corner.PID = parseQuantity(row["PID"])
		return corner
		
	def create(self, pipeName, cornerName, convertToSolid = True):
		frame_box = Box(self.document)
		frame_box.LX = self.LX
		frame_box.LY = self.LY
		frame_box.LZ = self.LZ
		# Init corner datata
		frame_box.corner = self.getCorner(cornerName)
		frame_box.G = frame_box.corner.G

		"setup pipe dimensions"
		row = self.pipe_table.findPart(pipeName)
		if row is None:
			print('Pipe part "%s" not found'%pipeName)
			return
		frame_box.PID = parseQuantity(row["ID"])
		frame_box.POD = parseQuantity(row["OD"])
		return frame_box.create(convertToSolid)

# Test macros.
def TestBox():
	document = FreeCAD.activeDocument()
	box = Box(document)
	box.create(True)
	document.recompute()

def TestTable():
	document = FreeCAD.activeDocument()
	pipe_table = CsvTable(PIPE_DIMENSIONS_USED)
	corner_table = CsvTable(CORNER_DIMENSIONS_USED)
	pipe_table.load(pipemod.CSV_TABLE_PATH)
	corner_table.load(outer.CSV_TABLE_PATH)
	box = BoxFromTable(document, pipe_table, corner_table)
	pipeName = pipe_table.getPartName(0)
	cornerName = corner_table.getPartName(0)

	print("Using pipe %s"%pipeName)
	print("Using corner %s"%cornerName)
	
	box.create(pipeName, cornerName, False)
	document.recompute()

#TestBox()
#TestTable()


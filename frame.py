# -*- coding: utf-8 -*-
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
import outerCorner
import pipe as pipemod

tu = FreeCAD.Units.parseQuantity

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
	outer diameter is larger than the iner one.

	Attributes:
	message -- explanation of the error
	"""

	def __init__(self, message):
		super(UnplausibleDimensions, self).__init__(message)


class Box:
	def __init__(self, document):
		self.document = document
		self.G = tu("2 cm")
		self.LX = tu("30 cm")
		self.LY = tu("20 cm")
		self.LZ = tu("25 in")
		self.POD = tu("3 cm")
		self.Thk = tu("0.5 cm")
		self.corner = outerCorner.OuterCorner(document)
		
	def checkDimensions(self):
		if not ( self.POD > tu("0 mm") and self.Thk > tu("0 mm") ):
			raise UnplausibleDimensions("Pipe dimensions must be positive. They are POD=%s and Thk=%s instead"%(self.POD, self.PID))
		if not (self.LX > 2*self.G):
			raise UnplausibleDimensions("The length LX %smust be larger than 2*G %s"%(self.LX, 2*self.G))
		if not (self.LY > 2*self.G):
			raise UnplausibleDimensions("The length LY %smust be larger than 2*G %s"%(self.LY, 2*self.G))
		if not (self.LZ > 2*self.G):
			raise UnplausibleDimensions("The length LZ %smust be larger than 2*G %s"%(self.LZ, 2*self.G))
	
	def createPipes(self, group, convertToSolid):
		# Calculate pipe lengthes
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

		# Add 3 clones for each x,y,z-type of axis. Place them on the edges of the quebe
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
		self.LX = tu("12 in")
		self.LY = tu("10 in")
		self.LZ = tu("8 in")

	def getCorner(self, partName):
		corner = OuterCorner(self.document)
		row = self.corner_table.findPart(partName)
		if row is None:
			print('Corner part "%s" not found'%partName)
			return
		corner.G = tu(row["G"])
		corner.H = tu(row["H"])
		corner.M = tu(row["M"])
		corner.POD = tu(row["POD"])
		corner.PID = tu(row["PID"])
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
		frame_box.PID = tu(row["ID"])
		frame_box.POD = tu(row["OD"])
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
	pipe_table.load(PIPE_CSV_TABLE_PATH)
	corner_table.load(CORNER_CSV_TABLE_PATH)
	box = BoxFromTable(document, pipe_table, corner_table)
	pipeName = pipe_table.getPartName(0)
	cornerName = corner_table.getPartName(0)

	print("Using pipe %s"%pipeName)
	print("Using corner %s"%cornerName)
	
	box.create(pipeName, cornerName, False)
	document.recompute()

#TestBox()
#TestTable()


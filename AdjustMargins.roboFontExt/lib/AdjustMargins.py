# The MIT License (MIT)

# Copyright (c) 2015 Alex Jacque <alexjacque.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# import our magic makers
from AppKit import *
import vanilla
import math
from defconAppKit.windows.baseWindow import BaseWindowController

class AdjustMargins(BaseWindowController):
	
	# setup our interface
	def __init__(self): 
		windowWidth = 200
		windowHeight = 270
		
		# amount area
		self.w = vanilla.FloatingWindow((windowWidth,windowHeight),"AdjustMargins")
		self.w.amountText = vanilla.TextBox((15,17,65,22),"Amount:",sizeStyle="small")
		self.w.amountTextBox = vanilla.EditText((70,12,-15,22))
		
		# divider
		self.w.divider1 = vanilla.HorizontalLine((15,48,-15,1))
		
		# glyphs scope area
		self.w.iconAllGlyphs = vanilla.ImageView((15,65,12,13))
		self.w.iconAllGlyphs.setImage(imagePath="../resources/allGlyphs.png")
		self.w.iconSelGlyphs = vanilla.ImageView((15,91,12,13))
		self.w.iconSelGlyphs.setImage(imagePath="../resources/selectedGlyphs.png")
		self.w.glyphsRadioGroup = vanilla.RadioGroup((32,60,-15,50),["All Glyphs","Selected Glyphs"],sizeStyle="small")
		self.w.glyphsRadioGroup.set(1) # default to just selected glyphs
		
		# divider
		self.w.divider2 = vanilla.HorizontalLine((15,121,-15,1))
		
		# margins area
		self.w.iconBothMargins = vanilla.ImageView((15,137,12,12))
		self.w.iconBothMargins.setImage(imagePath="../resources/bothMargins.png")
		self.w.iconLeftMargin = vanilla.ImageView((15,161,12,12))
		self.w.iconLeftMargin.setImage(imagePath="../resources/leftMargin.png")
		self.w.iconRightMargin = vanilla.ImageView((15,185,12,12))
		self.w.iconRightMargin.setImage(imagePath="../resources/rightMargin.png")
		self.w.marginSelectionGroup = vanilla.RadioGroup((32,133,-15,70),["Both Margins","Left Margin Only","Right Margin Only"],sizeStyle="small")
		self.w.marginSelectionGroup.set(0) # default both margins
		
		# divider
		self.w.divider3 = vanilla.HorizontalLine((15,216,-15,1))
		
		# commit button
		self.w.commitButton = vanilla.Button((15, 232, -15, 20), "Commit Adjustments", sizeStyle="small", callback=self.commitButtonCallback)
		
		self.w.open() # go go gadget window
		
	
	#	--------------------------
	#	Preform Adjustments
	#	- - -
	#	adjustmentAmount = amount to adjust (an integer)
	#	glyphs = set of glyphs to adjust
	#	mode = "set" (explicitly, ie "=") or "add" (assume add by default)
	#	--------------------------
	def adjustMargin(self,font,glyphs,adjustmentAmount,mode="add"):
		
		if mode == "set": # = sign supplied, setting one value equal to another
			
			for glyphName in glyphs: #iterate for all glyphs in set
				glyph = font[glyphName]
				glyph.prepareUndo("Metric Adjustment")
				if self.w.marginSelectionGroup.get() == 0: # adjust both margins
					glyph.leftMargin = adjustmentAmount
					glyph.rightMargin = adjustmentAmount
					print("Adjusted left and right margins to " + str(adjustmentAmount) + " for glyph: " + glyphName)
				elif self.w.marginSelectionGroup.get() == 1:
					glyph.leftMargin = adjustmentAmount
					print("Adjusted left margin to " + str(adjustmentAmount) + " for glyph: " + glyphName)
				elif self.w.marginSelectionGroup.get() == 2: # adjust right margin only
					glyph.rightMargin = adjustmentAmount
					print("Adjusted right margin to " + str(adjustmentAmount) + " for glyph: " + glyphName)
				glyph.performUndo()
			
		elif mode =="add": # adding some value (positive or negative) to current value
			
			for glyphName in glyphs: # iterate for all glyphs in set
				glyph = font[glyphName]
				glyph.prepareUndo("Metric Adjustment")
				if self.w.marginSelectionGroup.get() == 0: # adjust both margins
					glyph.leftMargin = glyph.leftMargin + adjustmentAmount
					glyph.rightMargin = glyph.rightMargin + adjustmentAmount
					print("Adjusted left and right margins " + str(adjustmentAmount) + " for glyph: " + glyphName)
				elif self.w.marginSelectionGroup.get() == 1:
					glyph.leftMargin = glyph.leftMargin + int(adjustmentAmount)
					print("Adjusted left margin " + str(adjustmentAmount) + " for glyph: " + glyphName)
				elif self.w.marginSelectionGroup.get() == 2: # adjust right margin only
					glyph.rightMargin = glyph.rightMargin + adjustmentAmount
					print("Adjusted right margin " + str(adjustmentAmount) + " for glyph: " + glyphName)
				glyph.performUndo()
			
		return
	
	
	def commitButtonCallback(self, sender):
		#
		# Note:
		# Code is getting pretty spaghettified, need to make this stuff into functions to get 
		# away from all the if else's, but, at least things work okay for the time being.
		#
		
		if CurrentFont() is None:  
			self.showMessage("Nothing Open","Please open a file first.") # show error, can't work with nothing...
		else:		
			font = CurrentFont()
			
			adjustmentAmount = self.w.amountTextBox.get()
			
			if len(adjustmentAmount) == 0:
				self.showMessage("How Much?","Please enter an adjustment amount.") # show error, can't work with nothing...
			else:
				
				#
				#	Get scope
				#
				
				# which glyphs we're working with
				if self.w.glyphsRadioGroup.get() == 0:
					glyphs = font.keys() # all
				else:
					glyphs = font.selection # a subset
					if glyphs == []:
						# "selected glyphs" is checked but nothing is selected
						self.showMessage("Adjust What?", "Please select at least one glyph to preform the adjustments on.")
						return # bail
					
				#
				#	Do adjustments
				#
				
				# if the user wants to set a margin exactly 
				if adjustmentAmount[:1] == "=":
					
					if adjustmentAmount[1:2] == "-": # if a negative sign proceeds the "="
						if adjustmentAmount[2:3].isdigit():
							# set to a specific number
							adjustmentAmount = int(adjustmentAmount[1:]) # stuff after =, make sure we're dealing with integers
							adjustmentMode = "set"
							self.adjustMargin(font,glyphs,adjustmentAmount,adjustmentMode)
								
						else: # not a digit found after "-"
							self.showMessage("Error","cannot deal with things like =-A")
						
						return # bail
					
					if (adjustmentAmount[1:].isdigit()): # if after the "=" a number is supplied
						# set to a specific number
						adjustmentAmount = int(adjustmentAmount[1:]) # stuff after =, make sure we're dealing with integers
						adjustmentMode = "set"
						self.adjustMargin(font,glyphs,adjustmentAmount,adjustmentMode)
													
						return # bail
					
					else: # if after the "=" a character is supplied
						# use an exisiting glyphs measurements
						characterName = adjustmentAmount[1:] # everything after the =
						
						# see if the glyph even exists at all
						if characterName in font:
							character = font[characterName]
							adjustmentLeft = int(character.leftMargin) # integers only please
							adjustmentRight = int(character.rightMargin) # integers only please
						else:
							self.showMessage("Glyph Not Found.","Glyph \"" + characterName + "\" does not exist in this font.")
				
						
						# preform adjustments using the supplied character's metrics
						for glyphName in glyphs:
							glyph = font[glyphName]
							glyph.prepareUndo("Metric Adjustment")
							if self.w.marginSelectionGroup.get() == 0: # adjust both margins
								glyph.leftMargin = adjustmentLeft
								glyph.rightMargin = adjustmentRight
								print("Adjusted left margin to " + str(adjustmentLeft) + " for glyph: " + glyphName)
								print("Adjusted right margin to " + str(adjustmentRight) + " for glyph: " + glyphName)
							elif self.w.marginSelectionGroup.get() == 1: # adjust left margin only
								glyph.leftMargin = adjustmentLeft
								print("Adjusted left margin to " + str(adjustmentLeft) + " for glyph: " + glyphName)
							elif self.w.marginSelectionGroup.get() == 2: # adjust right margin only
								glyph.rightMargin = adjustmentRight
								print("Adjusted right margin to " + str(adjustmentRight) + " for glyph: " + glyphName)
							glyph.performUndo()
						
						return # bail
				
				else: # for all other adjustments (+ or -)
					adjustmentAmount = int(adjustmentAmount) # make sure we're dealing with integers
					adjustmentMode = "add"
					self.adjustMargin(font,glyphs,adjustmentAmount,adjustmentMode)
					
					return # bail
				
OpenWindow(AdjustMargins)
import random

object = FreeCADGui.Selection.getSelection()[0]
randomColors=[]
for f2 in object.Shape.Faces:
	randomColors.append((random.random(),random.random(),random.random()))

object.ViewObject.DiffuseColor=randomColors

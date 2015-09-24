# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- export part with colors for  android/kivy
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------
## https://grabcad.com/library/motor-driver-rf520n-1/files/Motor%20driver%20RF520N.stp

import Draft
import Mesh,MeshPart, Part
from math import sin,cos,pi
import random


sources = FreeCADGui.Selection.getSelection()


targetname="TTC"
pathdemo="/tmp/"
pathdemo="/home/thomas/Dokumente/freecad_buch/152_obj_export_mit_farben/tmp/"
obname="exported_from_freecad"




def removeObj(obj):
	print "remove ", obj.Name, " == ", obj.Label
	App.ActiveDocument.removeObject(obj.Name)

def splitToFaces(sel):
	result=[]
	for sx in sel:
		shape=sx.Shape
		s=App.ActiveDocument.addObject('Part::Feature','copy')
		s.Shape=shape
		App.ActiveDocument.ActiveObject.Label=sx.Label
		FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=sx.ViewObject.DiffuseColor
		ll=Draft.downgrade(s,delete=False)
		faces=ll[0]
		n=0
		multi= len(s.ViewObject.DiffuseColor)<>1
		for f in faces:
			gg.addObject(f)
			print f.ViewObject
			if multi:
				f.ViewObject.DiffuseColor=s.ViewObject.DiffuseColor[n]
			else:
				f.ViewObject.DiffuseColor=s.ViewObject.DiffuseColor
			n += 1
			result.append(f)
		removeObj(s)
		FreeCAD.ActiveDocument.recompute()
	return result




def farbwert(r,g,b):
	mmin=min(r,g,b)
	mmax=max(r,g,b)
	mdiff=mmax-mmin
	if mmax==mmin:
		h=0
	elif mmax==r:
		h=2+(g-b)/mdiff
	elif mmax==g:
		h=4+(b-r)/mdiff
	elif mmax==b:
		h=(r-g)/mdiff
	else:
		raise Exception("farbberechnung")
	h =   h * pi/3
	return h

gg=App.ActiveDocument.addObject("App::DocumentObjectGroup","Gruppe")
sources=splitToFaces(sources)

f1=open(pathdemo+obname+".obj",'w')
f1.write("# FreeCAD export colored OBJ File:\n")
f1.write("mtllib "+obname+".mtl\n")
f1.write("o "+obname+"\n")

sloop=-1
v_string="#v_string .\n"
vt_string="#vt_string\n"
f_string="#f_string\n" + "s off\n" + "usemtl Material" + "\n\n"

z=0
h=farbwert(0,0,1.0)
x=0.5+ 0.5*cos(h)*0.9
y=0.5 + 0.5*sin(h)*0.9
vt_string += "# " + str(z) +  "  Fehlerfarbe "   + "\n"
vt_string += "vt 0.5 0.5\n"

v_ix=0
f_ix=1

for source in  sources:
	sloop += 1
	__doc__=App.ActiveDocument
	__mesh__=__doc__.addObject("Mesh::Feature","Mesh")
	
	# netzmethode  - laufzeit und qualitaet testen #+#
	
	# mefisto
	#__mesh__.Mesh=MeshPart.meshFromShape(Shape=source.Shape,MaxLength=0.5)
	
	# standard
	__mesh__.Mesh=Mesh.Mesh(source.Shape.tessellate(0.1))
	
	# netgen
	#__mesh__.Mesh=MeshPart.meshFromShape(Shape=source.Shape,Fineness=2,SecondOrder=0,Optimize=1,AllowQuad=0)
	
	__mesh__.ViewObject.CreaseAngle=25.0
	target=__doc__.addObject("Part::Feature",targetname)
	__shape__=Part.Shape()
	__shape__.makeShapeFromMesh(__mesh__.Mesh.Topology,0.100000)

	target.Shape=__shape__
	target.purgeTouched()
	removeObj(__mesh__)

	del __shape__
	del __doc__, __mesh__

	s=target.Shape
	vc=0
	points=[]
	for vx in s.Vertexes:
		v=vx.Point
		v_string +="# sloop=" + str(sloop) + " vx=" + str(vc) + "\n"
		v_string += ''.join(["v ", str(v[0])," ",str(v[1])," ",str(v[2]),"\n"])
		points.append(v)
		vc += 1
	fc=0

	pref=source.Shape.Faces
	flist={}
	fnlist={}
	fcolorlist={}
	dlist={}
	ez=0
	
	dlist=s.Faces

	sc=source.ViewObject.DiffuseColor[0]
	target.ViewObject.DiffuseColor=sc
	h=farbwert(sc[0],sc[1],sc[2])
	x=0.5+ 0.5*cos(h)*0.9
	y=0.5 + 0.5*sin(h)*0.9
	vt_string +="# " + str(z) +  "   " + str(sc)  + "\n"
	vt_string +="vt " +str(x) + " " + str(y) + "\n"
	z += 1

	fc=0
	for e in s.Faces:
		try:
			f_string += ''.join(['f ',str(points.index(e.Vertexes[0].Point)+1 + v_ix),
				'/',str(fc+1 + f_ix),' ',str(points.index(e.Vertexes[1].Point)+1 + v_ix),
				'/',str(fc+1 + f_ix),' ',str(points.index(e.Vertexes[2].Point)+1 + v_ix),'/',str(fc+1 + f_ix),'\n'])
		except:
			print "Fehler ",fc
			pass
	v_ix += len(points)
	f_ix += 1
	vt_string += "\n# next part v_ix="  + str(v_ix) + " f_ix=" + str(f_ix) +"\n\n" 
	f_string += "\n# next part v_ix="  + str(v_ix) + " f_ix=" + str(f_ix) +"\n\n" 
	removeObj(target)

f1.write(v_string)
f1.write(vt_string)
f1.write(f_string)
f1.close()

if 1:
	import os
	cmd="cd " + pathdemo + "; python multi_color.py "+ pathdemo+obname+ ".obj &"
	FreeCAD.Console.PrintMessage("\n"+cmd+"\n")
	os.system(cmd)

'''
files:

multi_color.py
exported_from_freecad.mtl
exported_from_freecad.obj
farbkreis.png
simple.glsl
''' 

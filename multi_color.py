#qpy:kivy

#import os
import kivy3
from kivy.app import App
from kivy.clock import Clock
from kivy3 import Scene, Renderer, PerspectiveCamera
from kivy3.loaders import OBJMTLLoader,OBJLoader
from kivy.uix.floatlayout import FloatLayout

file=""

from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '400')

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import *


class MainApp(App):

	
	rotx=Property(True)
	roty=Property(True)
	
	def stop_rotx(self,a):
		self.rotx= not self.rotx

	def stop_roty(self,a):
		self.roty= not self.roty

	def build(self):
		box= BoxLayout(orientation='vertical')
		layout = GridLayout(cols=4)
		layout.add_widget(Button(text='rotx',on_press=self.stop_rotx))
		layout.add_widget(Button(text='roty',on_press=self.stop_roty))

		
		box.add_widget(layout)
		root = FloatLayout()
		box.add_widget(root)
		self.renderer = Renderer(shader_file="simple.glsl")
		scene = Scene()
		camera = PerspectiveCamera(45, 1, 1, 1000)
		camera.position=(0,0,90)
		#loader = OBJMTLLoader()
		#obj = loader.load("my_colors.obj", "my_colors.mtl")
		loader = OBJLoader()
		#obj = loader.load("my_colors.obj")
		
		#obj = loader.load("Cube.obj")
		#obj = loader.load("Fusion003.obj")
		obj = loader.load(file)

		scene.add(*obj.children)
		for obj in scene.children:
			obj.pos.z = -6.

		self.renderer.render(scene, camera)
		self.orion = scene.children[0]

		root.add_widget(self.renderer)
		self.renderer.bind(size=self._adjust_aspect)
		Clock.schedule_interval(self._rotate_obj, 1 / 20)
		return box

	def _adjust_aspect(self, inst, val):
		rsize = self.renderer.size
		aspect = rsize[0] / float(rsize[1])
		self.renderer.camera.aspect = aspect

	def _rotate_obj(self, dt):
		if self.rotx:
			self.orion.rot.x += 0.2
		if self.roty:
			self.orion.rot.y += 0.4

if __name__ == '__main__':
	
	import sys
#	print "\n".join(sys.argv)
	file=sys.argv[1]
	print file
	MainApp().run()

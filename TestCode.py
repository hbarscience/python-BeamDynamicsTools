from numpy import *

class Class1(object):
	c=123
	def __init__(self,a=1,b=2):
		self.a=a
		self.b=self.c

class Class2(Class1):
	def __init__(self,ClassIn):
		pass

	def Function(self,N):
		return self.A*N

A = Class1()

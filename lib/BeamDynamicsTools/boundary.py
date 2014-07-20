from numpy import *
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
from numpy.linalg import norm,det
import matplotlib.pyplot as plt

class boundary:

	def __init__(self,Rb,Zb,cw=-1):
		Cvec = []; # Corner Locations 
		Mvec = []; # Middle of line locations
		Tvec = []; # Tangent vectors of border
		Nvec = []; # Normal Vectors of border
		self.Rb = Rb
		self.Zb = Zb
		for i in range(len(Rb)):
			Corner = array([Rb[i],Zb[i]])
			MidPoint = array([(Rb[i]+Rb[i-1])/2,(Zb[i]+Zb[i-1])/2])
			Tangent = array([Rb[i]-Rb[i-1],Zb[i]-Zb[i-1]]); Tangent=Tangent/norm(Tangent)
			Normal = array([-Tangent[1],Tangent[0]]); Normal = Normal/norm(Normal)

			Cvec.append(Corner); 
			Mvec.append(MidPoint); 
			Tvec.append(Tangent); 
			Nvec.append(cw*Normal); 
#			print Corner[i-1]-Corner[i-2]
		self.Cvec = Cvec
		self.Mvec = Mvec
		self.Tvec = Tvec
		self.Nvec = Nvec
		self.Nv = len(Nvec)
		print 'boundary initialized'

	def Plot2D(self,FIG=1):
		pl.figure(FIG)
		Cvec = self.Cvec; Mvec = self.Mvec; Tvec = self.Tvec; Nvec = self.Nvec

		for i in range(self.Nv):
			pl.plot([Cvec[i][0],Cvec[i-1][0]],[Cvec[i][1],Cvec[i-1][1]])
			pl.plot([Nvec[i][0]+Mvec[i][0],Mvec[i][0]],[Nvec[i][1]+Mvec[i][1],Mvec[i][1]])
			pl.plot(Mvec[i][0],Mvec[i][1],'o')

		pl.xlim(0.3-1,0.3+1)
		pl.ylim(-1,1)

	def Border(self,Type='poloidal'):
		if Type=='poloidal':
			RB=[]; ZB=[];
			for i in range(len(self.Rb)):
				RB.append(self.Rb[i])
				ZB.append(self.Zb[i])
			RB.append(self.Rb[0])
			ZB.append(self.Zb[0])
			pl.plot(RB,ZB,'k')

		if Type=='top':
			for i in range(len(self.Rb)):
				x,y=Circle(self.Rb[i])
				pl.plot(x,y,'k')

	def InVolume(self,r):
		x0 = [sqrt(r[0]*r[0] + r[1]*r[1]) ,r[2]]
		IN = True; i=-1;
		D1 = []
		while (IN == True and i<self.Nv-1):
			D1 = x0-self.Cvec[i-1]
			D2 = x0-self.Cvec[i]
			if (dot(D1,self.Tvec[i-1])>0 and dot(D2,self.Nvec[i-1])<0):
				if dot(D1,self.Nvec[i])<0:
					IN = False
			i = i+1
		return IN

	# Xboundary determines the line drawn between two points r0 and r1 crosses a the boundary.
	# This function returns: boolean (IN), normal vector, tangent vector, incident vector.
	def Xboundary(self,r0,r1):
		x0 = array([sqrt(r0[0]**2 + r0[1]**2) ,r0[2]])
		x1 = array([sqrt(r1[0]**2 + r1[1]**2) ,r1[2]])
		IN = True; i=-1; Di1 = []; Di2 = []; Df = []; NORM=[]; TAN=[]; INC=[]; RT = r1
		while (IN == True and i<self.Nv):
			Di1 = x0-self.Cvec[i-1]; Di1 = Di1/norm(Di1)
			Di2 = x0-self.Cvec[i]; Di1 = Di1/norm(Di1)
			Df = x1-self.Cvec[i-1]
			if dot(Di1,self.Tvec[i])>0 and dot(Di2,self.Tvec[i])<0:
				if dot(Di1,self.Nvec[i])>0 and dot(Di2,self.Nvec[i])>0:
					if dot(Df,self.Nvec[i])<0 and dot(Df,self.Nvec[i])<0:
						IN = False
						Phi = arctan(r0[1]/r0[0])
						NORM = array([ self.Nvec[i][0]*cos(Phi), self.Nvec[i][0]*sin(Phi), self.Nvec[i][1] ])
						TAN = array([ self.Tvec[i][0]*cos(Phi), self.Tvec[i][0]*sin(Phi),self.Tvec[i][1] ]);
						TAN = TAN/norm(TAN)
						INC = r1-r0; INC = INC/sqrt( INC[0]**2 + INC[1]**2 + INC[2]**2 )
						RT = r1
			i=i+1
		return IN,NORM,TAN,INC,RT

	def Figure3D(self,FIG=1):
		fig = pl.figure(FIG)
		ax = Axes3D(fig)
		return ax

	def Plot3D(self,ax,Nt=16,Color='b',PhiMin=-pi/8,PhiMax=pi/2):
		#Phi = linspace(0,2*pi*(1-1/Nt),Nt)
		Phi = linspace(PhiMin,PhiMax,Nt)
		xp=[]; yp=[]; zp=[];
		for i in range(Nt):
			Nr = len(self.Rb)+1
			x=[]; y=[]; z=[];
			for j in range(Nr):
				x.append(cos(Phi[i])*self.Rb[j-1])
				y.append(sin(Phi[i])*self.Rb[j-1])
				z.append(self.Zb[j-1])
			if i == 0 or i==Nt-1:
				ax.plot(x,y,z,'k',linewidth=3)
			else:
				ax.plot(x,y,z,Color)
			xp.append(x); yp.append(y); zp.append(z)

#		d1=1.25; d2=1.8; dz=(d2+d1)/2.0
	
		Nc = Nt*10
		Phi = linspace(PhiMin,PhiMax,Nc)
		xt=[]; yt=[]; zt=[];
		for j in range(Nr):
			for i in range(Nc):
				xp.append(cos(Phi[i])*self.Rb[j-1])
				yp.append(sin(Phi[i])*self.Rb[j-1])
				zp.append(self.Zb[j-1])
			ax.plot(xp[-Nc:-1], yp[-Nc:-1], zp[-Nc:-1],Color)
		pl.xlim(-1,1); pl.ylim(-1,1)
		return ax
		#return xp,yp,zp,xt,yt,zt

# Test Case

def TestInVolume(Bound,Ni):
	pl.figure(1)
	Xrand = array([0.0,0.0])
	for i in range(Ni):
		Xrand[0] = random.rand()
		Xrand[1] = random.rand()*2 - 1
		print i
		if Bound.InVolume(Xrand):
			pl.plot(Xrand[0],Xrand[1],'.g')
		else:
			pl.plot(Xrand[0],Xrand[1],'.r')

def Intersection(a1,a2,b1,b2):
	x1=a1[0]; x2=a2[0]; x3=b1[0]; x4=b2[0];
	y1=a1[1]; y2=a2[1]; y3=b1[1]; y4=b2[1];

	xOut = ( (x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4) )
	yOut = ( (x1*y2-y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4) )

	return array([xOut,yOut])

def Circle(R,Nt=100):
	t = linspace(0,2*pi,Nt)
	x = R*cos(t)
	y = R*sin(t)
	return x,y

#Rb = [ 0.2 , 0.25, 0.4 , 0.6 , 0.8 , 0.8 , 0.6 , 0.4 , 0.25, 0.2 ]
#Zb = [-0.55,-0.6 ,-0.6 ,-0.5 ,-0.2 , 0.2 , 0.5 , 0.6 , 0.6 , 0.55]


#Wall = boundary(Rb,Zb)
#Wall.Plot2D(1)

#TestInVolume(Wall,1000)

#Wall.Plot3D(Nt=16,FIG=2)
pl.show()



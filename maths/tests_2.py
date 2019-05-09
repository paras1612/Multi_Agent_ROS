import numpy as np
import matplotlib.pyplot as plt

class motionVector:
	x = None
	y = None
	z = None

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def magnitude(self):
		return np.sqrt(self.x**2 + self.y**2 + self.z**2)

	def normalise(self):
		mag = self.magnitude()
		return motionVector(self.x/mag, self.y/mag, self.z/mag)

	def cross(self, vec):
		crossed = motionVector(self.y * vec.z - self.z * vec.y, self.x * vec.z - self.z * vec.x, self.x * vec.y - self.y * vec.x)
		return crossed

	def radiusVector(self):
		t = np.arange(0,self.x.shape[0]/5,0.2)
		v = motionVector(np.diff(self.x)/np.diff(t), np.diff(self.y)/np.diff(t), np.diff(self.z)/np.diff(t))
		magV = v.magnitude()
		v = v.normalise()

		t1 = (t[1:] + t[:-1])*0.5
		a = motionVector(np.diff(v.x)/np.diff(t1), np.diff(v.y)/np.diff(t1), np.diff(v.z)/np.diff(t1))
		magA = a.magnitude()

		rc = (magV[1:] + magV[:-1])*0.5/magA
		a = a.normalise()
		return rc, motionVector(a.x, a.y, a.z)

	def wingVelocity(self,d,w):
		rc, ncap = self.radiusVector()
		r1 = rc + d
		r2 = -rc + d
		rc1 = motionVector(ncap.x*r1, ncap.y*r1, ncap.z*r1)
		rc2 = motionVector(ncap.x*r2, ncap.y*r2, ncap.z*r2)

		for i in range(2):
			w.x = (w.x[1:] + w.x[:-1])*0.5
			w.y = (w.y[1:] + w.y[:-1])*0.5
			w.z = (w.z[1:] + w.z[:-1])*0.5
			
		v1 = w.cross(rc1)
		v2 = w.cross(rc2)
		return v1,v2


t = np.arange(0,100*0.2,0.2)
x = 2*np.cos(t)
y = 2*np.sin(t)
z = np.zeros(t.shape)
w = motionVector(np.zeros(t.shape) + 10, np.zeros(t.shape) + 10, np.zeros(t.shape) + 10)

r = motionVector(x,y,z)
rc, ncap = r.radiusVector()
print(rc)
v1,v2 = r.wingVelocity(4,w)
print(v1.x)
print(v2.x)


	



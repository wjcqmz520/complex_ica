import pdb,os,time
import numpy as np
from math import log
from numpy.linalg import *
from numpy.random import rand
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import axes3d
import complex_ica as cica
reload(cica)

m = 50000
n = 5
exp1 = np.ceil(10*rand())
r = np.random.exponential(exp1,size=(n,m))
f = np.zeros(r.shape)
for j in xrange(n):
    f[j] = np.random.uniform(-2*np.pi,2*np.pi,size=(1,m))
Xu = r*np.cos(f)+1j*np.sin(f)
# Standardize data
Xu = inv(np.diag(Xu.std(1))).dot(Xu)
# Mixing using complex mixing matrix A
A  = rand(n,n)+1j*rand(n,n)
Xm = A.dot(Xu)

K,W,S,EG = cica.complex_FastICA(Xm,max_iter=30,algorithm='deflation',\
                    n_components=n)

'''
Compute the SSE
'''
absKAHW  = np.abs((K.dot(A)).conj().T.dot(W))
maximum  = np.max(absKAHW)
SSE      = (np.sum(absKAHW**2)-maximum**2+np.repeat(1-maximum,5)**2).sum()

print SSE

fig     = plt.figure('demo')
ax      = fig.add_subplot(121)
ax.plot(np.ma.masked_invalid(EG.T),'.-')
ax.set_title('Convergence of G')

ntp=100
ax2  = fig.add_subplot(122,projection='3d')
z    = np.linspace(-2,2,ntp)
x    = np.imag(Xu[0,:ntp])
y    = np.real(Xu[0,:ntp])
ax2.plot(x,y,z,'.-')

x    = np.imag(S[0,:ntp])
y    = np.real(S[0,:ntp])
ax2.plot(x,y,z,'.-')

plt.show()





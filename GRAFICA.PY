
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import multivariate_normal
from mpl_toolkits.mplot3d import Axes3D

def fitness(ind1, ind2):
    return pow(ind1-5,2)+pow(ind2-5,2)	
    #return 100*(pow(pow(ind1,2)-ind2,2))+pow(1-ind1,2)
    #return float("%.5f"%(-1*np.cos(ind1)*np.cos(ind2)*np.exp(-1*pow((ind1-pi),2)-pow(ind2-pi,2))))	
	
def normal(x, desv): 
    retorno=-0.5*((x/desv)*(x/desv))
    retorno=pow(np.e,retorno)
    return retorno/(desv*(np.sqrt(6.283184)))


d=0
pi=3.141592
x=[]
while d<=5: 
   d=d+0.01
   x.append(d)	

#print(x)
z=[]
desv=3
y=[]
d=0
for i in range(len(x)):
   d=d+0.01	  
   y.append(d)		
   z.append(fitness(x[i],y[i]))

#print(y)
'''
plt.scatter(x , y , c='red')
plt.show()
'''
fig = plt.figure()

ax = fig.gca(projection='3d')

surf=ax.plot_surface(x,y,z,cmap='viridis',linewidth=0)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.plot_wireframe(x,y,z)
#fig.colorbar(surf, shrink=0.5, aspect=10)
plt.show()



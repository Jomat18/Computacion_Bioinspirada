import numpy 
import matplotlib.pyplot as plt

def crear_poblacion(size,xi,xf,vi,vf):
	poblacion=[]
	print "************************Poblacion Inicial********************************"
	for i in range(size):
		x_=list(numpy.random.uniform(xi,xf,2))
		v_=list(numpy.random.uniform(vi,vf,2))	
		for vel in v_:
			x_.append(vel)
		x_.append(0.0)
		x_.append(0.0)
		x_.append(100000)
		poblacion.append(x_)
		print "x1=",poblacion[i][0],"x2=",poblacion[i][1],"v1=",poblacion[i][2],"v2=",poblacion[i][3]

	print '\n'
	return poblacion

def fitness(x1,x2):
	return pow(x1,2)+pow(x2,2)


def actualizar_velocidad(ind,w,fi1,fi2, gl_x1,gl_x2,r1,r2):
	ind[2]=w*ind[2]+fi1*r1*(ind[4]-ind[0])+fi2*r2*(gl_x1-ind[0])
	ind[3]=w*ind[3]+fi1*r1*(ind[5]-ind[1])+fi2*r2*(gl_x2-ind[1])
	return ind[2],ind[3]

def pso(size):
	pob=crear_poblacion(size,xmin,xmax,-1,1)
	lgx_1=0
	lgx_2=0
	fit_lg=10000000	
	it=0
	while(it<iteraciones):
		print "*************************Iteracion ",it+1,"*******************************"
		for i in range(size):
			temp=fitness(pob[i][0],pob[i][1])
			if temp<pob[i][6]:
				pob[i][4]=pob[i][0]
				pob[i][5]=pob[i][1]
				pob[i][6]=temp

			if temp<fit_lg:
				fit_lg=temp
				lgx_1=pob[i][0]
				lgx_2=pob[i][1]			 	


		for i in range(size):
			r1=numpy.random.uniform(0,1)
			r2=numpy.random.uniform(0,1)
			w=numpy.random.uniform(0,1)				
			pob[i][2],pob[i][3]=actualizar_velocidad(pob[i],w,fi1,fi2,lgx_1,lgx_2,r1,r2)
			pob[i][0]=pob[i][0]+pob[i][2]
			if pob[i][0]>xmax:
				pob[i][0]=xmax
			if pob[i][0]<xmin:
				pob[i][0]=xmin
			pob[i][1]=pob[i][1]+pob[i][3]
			if pob[i][1]>xmax:
				pob[i][1]=xmax	
			if pob[i][1]<xmin:
				pob[i][1]=xmin

			print "x1=",pob[i][0],"x2=",pob[i][1],"v1=",pob[i][2],"v2=",pob[i][3],"fit=",pob[i][6] 	
			if 'sca' in globals(): sca.remove()
			sca = plt.scatter(pob[i][0], pob[i][1], s=200, lw=0, c='red', alpha=0.5); #plt.pause(0.001)

		print '\n'
		it+=1


iteraciones=100
size=6
fi1=2
fi2=2
xmin=-5
xmax=5
pso(size)
plt.ioff(); plt.show()





			



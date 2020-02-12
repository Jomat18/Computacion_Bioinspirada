import numpy 
import matplotlib.pyplot as plt
import copy

def f1(x1,x2):
	return 4*pow(x1,2)+4*pow(x2,2)

def f2(x1,x2):
	return pow(x1-5,2)+pow(x2-5,2)	

def crear_poblacion(size,xi,xf,yi,yf,vi,vf):
	poblacion=[]
	print "************************ Poblacion Inicial ********************************"
	for i in range(size):
		x_=[]
		repo=[]
		x_.append(numpy.random.uniform(xi,xf))
		x_.append(numpy.random.uniform(yi,yf))
		v_=list(numpy.random.uniform(vi,vf,2))	
		for vel in v_:
			x_.append(vel)
		repo.append(x_[0])
		repo.append(x_[1])
		repo.append(f1(x_[0],x_[1]))
		repo.append(f2(x_[0],x_[1]))
		repo.append('')
		x_.append([repo])
		poblacion.append(x_)
		print "x1=",poblacion[i][0],"x2=",poblacion[i][1],"v1=",poblacion[i][2],"v2=",poblacion[i][3]

	return poblacion

def evaluar(x1,x2):
	fit=[]	
	fit.append(x1)
	fit.append(x2)
	fit.append(f1(x1,x2))
	fit.append(f2(x1,x2))
	fit.append('')
	return fit	
	

def actualizar_repositorio(nuevo,repositorio):	
	size=len(repositorio)	
	for i in range(size):
		dominado,do_f,iq=no_dominado(nuevo,repositorio[i])
		if dominado==False:
			print "x_i:", "x1=",nuevo[0],"x2=",nuevo[1],"f1=",nuevo[2],"f2=",nuevo[3]
			for r in range(len(repositorio)):
				print "x1=",repositorio[r][0],"x2=",repositorio[r][1],"f1=",repositorio[r][2],"f2=",repositorio[r][3]
			return repositorio
		if dominado and iq:
			repositorio[i][4]='d'			
		if do_f:
			repositorio[i][4]='d'
	i=0
	while i<size:
		if repositorio[i][4]=='d':
			repositorio.pop(i)
			i-=1
			size=len(repositorio)
		i+=1	

	if dominado and nuevo[4]!='i':	
		repositorio.append(nuevo)
	
	print "x_i:", "x1=",nuevo[0],"x2=",nuevo[1],"f1=",nuevo[2],"f2=",nuevo[3]
	for r in range(len(repositorio)):
		print "x1=",repositorio[r][0],"x2=",repositorio[r][1],"f1=",repositorio[r][2],"f2=",repositorio[r][3]
	return repositorio


def no_dominado(nuevo,repositorio):
	dominado1=False
	dominado2=False
	iguales1=False
	iguales2=False
	
	if nuevo[2]==repositorio[2]:
		iguales1=True
	if nuevo[2]<repositorio[2]:
		dominado1=True	
	if nuevo[3]==repositorio[3]:
		iguales2=True
	if nuevo[3]<repositorio[3]:
		dominado2=True
	if iguales1 and iguales2:
		nuevo[4]='i'

	return dominado1 or dominado2,dominado1 and dominado2, iguales1 or iguales2 


def actualizar_velocidad(ind,w,fi1,fi2,repo_gl,r1,r2):
	a_l=numpy.random.randint(len(ind[4]))
	a_g=numpy.random.randint(len(repo_gl))
	
	ind[2]=w*ind[2]+fi1*r1*(ind[4][a_l][0]-ind[0])+fi2*r2*(repo_gl[a_g][0]-ind[0])
	ind[3]=w*ind[3]+fi1*r1*(ind[4][a_l][1]-ind[1])+fi2*r2*(repo_gl[a_g][1]-ind[1])
	return ind[2],ind[3]

def pso(size):
	pob=crear_poblacion(size,xmin,xmax,ymax,ymin,-1,1)
	print 
	repo_gl=copy.copy(pob[0][4])
	it=0
	
	while(it<iteraciones):
		print "************************* Iteracion ",it+1,"*******************************"
	        print
		for i in range(size):
			fit=evaluar(pob[i][0],pob[i][1])
			print "****************************** Repositorio local ",i+1,"******************************"
			pob[i][4]=actualizar_repositorio(fit,pob[i][4])
			fit[4]=''
			print
			print "****************************** Repositorio Global ******************************"
			repo_gl=actualizar_repositorio(fit,repo_gl)
			print

		print "****************************** Nueva Poblacion ******************************"
		for i in range(size):
			r1=numpy.random.uniform(0,1)
			r2=numpy.random.uniform(0,1)
			w=numpy.random.uniform(0,1)				
			#w=0.01
			pob[i][2],pob[i][3]=actualizar_velocidad(pob[i],w,fi1,fi2,repo_gl,r1,r2)
			pob[i][0]=pob[i][0]+pob[i][2]
			if pob[i][0]>xmax:
				pob[i][0]=xmax
			if pob[i][0]<xmin:
				pob[i][0]=xmin
			pob[i][1]=pob[i][1]+pob[i][3]
			if pob[i][1]>ymax:
				pob[i][1]=ymax	
			if pob[i][1]<ymin:
				pob[i][1]=ymin

			f_1=f1(pob[i][0],pob[i][1])
			f_2=f2(pob[i][0],pob[i][1])
			print "x1=",pob[i][0],"x2=",pob[i][1],"v1=",pob[i][2],"v2=",pob[i][3],"f1=",f_1,"f2=",f_2
			#if 'sca' in globals(): sca.remove()
			#sca = plt.scatter(f_1,f_2, s=100, lw=0, c='red', alpha=0.5); #plt.pause(0.001)

		print 
		it+=1
	'''
	print "******************************Repositorio Global******************************"
	for i in range(len(repo_gl)):
		print repo_gl[i]
	'''

#size_repo=10
iteraciones=10
size=10
fi1=2
fi2=2
xmin=0
xmax=5
ymax=3
ymin=0
pso(size)
#plt.ioff(); plt.show()





			



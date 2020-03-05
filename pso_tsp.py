import numpy as np
import copy

distancias=[[0,12,3,23,1,5,23,56,12,11],
            [12,0,9,18,3,41,45,5,41,27],
            [3,9,0,89,56,21,12,48,14,29],
            [23,18,89,0,87,46,75,17,50,42],
	    [1,3,56,87,0,55,22,86,14,33],
	    [5,41,21,46,55,0,21,76,54,81],
	    [23,45,12,75,22,21,0,11,57,48],
	    [56,5,48,17,86,76,11,0,63,24],
	    [12,41,14,50,14,54,57,63,0,9],
	    [11,27,29,42,33,81,48,24,9,0]]


costos=[[0,22,47,15,63,21,23,16,11,9],
       [22,0,18,62,41,52,13,11,26,43],
       [47,18,0,32,57,44,62,20,8,36],
       [15,62,32,0,62,45,75,63,14,12],
       [63,41,57,62,0,9,99,42,56,23],
       [21,52,44,45,9,0,77,58,22,14],
       [23,13,62,75,99,77,0,30,25,60],
       [16,11,20,63,42,58,30,0,66,85],
       [11,26,8,14,56,22,25,66,0,54],
       [9,43,36,12,23,14,60,85,54,0]]


def permutacion(lista, size):
	a=np.random.randint(size)
	b=np.random.randint(size)
	while(a==b):
		b=np.random.randint(size)
	
	temp=lista[a]
	lista[a]=lista[b]
	lista[b]=temp

def fitness(ruta):
	costo1=0
        costo2=0
	size=len(ruta)-1
	for i in range(size):
		costo1+=distancias[ord(ruta[i])%65][ord(ruta[i+1])%65]
                costo2+=costos[ord(ruta[i])%65][ord(ruta[i+1])%65]
			
	return costo1,costo2


def generar_poblacion(ciudades, size):	
	poblacion=[]
	velocidad=[]
	valor=len(ciudades)
	for i in range(size):
		ruta=[]
		repo=[]	
		camino=copy.copy(ciudades)
		permutacion(camino, valor)
		ruta.append(camino)
		repo.append(camino)
		f_1,f_2=fitness(camino)
		repo.append(f_1)
		repo.append(f_2)
		repo.append('')
		ruta.append([repo])
		ruta.append(velocidad)
		temp=copy.copy(ruta)
		poblacion.append(temp)
		del ruta[:]				

	return poblacion


def swap(lista1,pos):
	i=np.random.choice(pos)
	pos.remove(i)
	j=np.random.choice(pos)
	temp=lista1[i]
	lista1[i]=lista1[j]
	lista1[j]=temp

	return i, j

def posiciones(per1, per2):
	size=len(per1)
	pos=[]
	for i in range(size):
		if per1[i]!=per2[i]: 
			pos.append(i)

	return pos

def iguales(per1, per2):
	size=len(per1)
	for i in range(size):
		if per1[i]!=per2[i]:
			return True

	return False

def diferencia(lista1,lista2):
	velocidad=[]
	while iguales(lista1,lista2):
		swaps=[]
		pos = posiciones(lista1,lista2)
		i,j = swap(lista1,pos)
		swaps.append(i)
		swaps.append(j)
		swaps.append(1)  #1
		temp=copy.copy(swaps)
		velocidad.append(temp)
		del swaps[:]


	return velocidad

def swap2(lista1,pos):
	r=np.random.uniform(0,1)
	if len(pos) and r<pos[2]:
		i=pos[0]
		j=pos[1]
		temp=lista1[i]
		lista1[i]=lista1[j]
		lista1[j]=temp


def evaluar(ruta):
	fit=[]	
	f_1,f_2=fitness(ruta)
	fit.append(ruta)
	fit.append(f_1)
	fit.append(f_2)
	fit.append('')
	return fit	
	

def actualizar_repositorio(nuevo,repositorio):	
	size=len(repositorio)	
	for i in range(size):
		dominado,do_f,iq=no_dominado(nuevo,repositorio[i])
		if dominado==False:
			print "Nueva_ruta:", nuevo[0],"f1=",nuevo[1],"f2=",nuevo[2] 
			for r in range(len(repositorio)):
				print repositorio[r][0],"f1=",repositorio[r][1],"f2=",repositorio[r][2]
			return repositorio
		if dominado and iq:
			repositorio[i][3]='d'			
		if do_f:
			repositorio[i][3]='d'
	i=0
	while i<size:
		if repositorio[i][3]=='d':
			repositorio.pop(i)
			i-=1
			size=len(repositorio)
		i+=1	

	if dominado and nuevo[3]!='i':	
		repositorio.append(nuevo)
	
	print "Nueva_ruta:", nuevo[0],"f1=",nuevo[1],"f2=",nuevo[2] 
	for r in range(len(repositorio)):
		print repositorio[r][0],"f1=",repositorio[r][1],"f2=",repositorio[r][2]
	return repositorio


def no_dominado(nuevo,repositorio):
	dominado1=False
	dominado2=False
	iguales1=False
	iguales2=False
	
	if nuevo[1]==repositorio[1]:
		iguales1=True
	if nuevo[1]<repositorio[1]:
		dominado1=True	
	if nuevo[2]==repositorio[2]:
		iguales2=True
	if nuevo[2]<repositorio[2]:
		dominado2=True
	if iguales1 and iguales2:
		nuevo[3]='i'

	return dominado1 or dominado2,dominado1 and dominado2, iguales1 or iguales2 


def actualizar_velocidad(x,local_,global_):
	a_l=np.random.randint(len(local_))
	a_g=np.random.randint(len(global_))

	copia=copy.copy(local_[a_l][0])
	copia2=copy.copy(global_[a_g][0])
	velocidad=[]
	a=diferencia(copia,x)
	print "pbest-x(t-1)", a
	b=diferencia(copia2,x)	
	print "gbest-x(t-1)", b
	velocidad=a+b
	return velocidad


def actualizar_x(x, velocidad):	
	for vel in velocidad:
		swap2(x,vel)
	
	return x


def pso(ciudades,size):
	pob=generar_poblacion(ciudades,size)	
	repo_gl=copy.copy(pob[0][1])	
	it=0
	
	while(it<iteraciones):
		print "************************* Iteracion ",it+1,"*******************************"
		for i in range(size):
			fit=evaluar(pob[i][0])
			print "****************************** Repositorio local ",i+1,"******************************"
			pob[i][1]=actualizar_repositorio(fit,pob[i][1])
			fit[3]=''
			print
			print "****************************** Repositorio Global ******************************"
			repo_gl=actualizar_repositorio(fit,repo_gl)
			print

				 	
		for i in range(size):	
			f_1,f_2=fitness(pob[i][0])
			print i+1," Actual", pob[i][0],"fit1: ",f_1 ,"fit2: ", f_2
			#print "Mejor", pob[i][2],"fitness: ",fitness(pob[i][2])	
			velocidad=actualizar_velocidad(pob[i][0],pob[i][1],repo_gl)
			if len(velocidad)!=0:
				pob[i][0]=actualizar_x(pob[i][0],velocidad)
			
			print "Velocidad:", pob[i][2]
			pob[i][2]=velocidad
			print 

		it+=1
		print 	
	

ciudades=['A','B','C','D','E','F','G','H','I']
iteraciones=10
size=10
pso(ciudades,size)




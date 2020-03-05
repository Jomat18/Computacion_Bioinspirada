import numpy as np
import copy

distancias=[[0,1,3,4,5],
            [1,0,1,4,8],
            [3,1,0,5,1],
            [4,4,5,0,2],
	    [5,8,1,2,0]]


def permutacion(lista, size):
	a=np.random.randint(size)
	b=np.random.randint(size)
	while(a==b):
		b=np.random.randint(size)
	
	temp=lista[a]
	lista[a]=lista[b]
	lista[b]=temp


def generar_poblacion(ciudades, size):	
	poblacion=[]
	local=[]
	velocidad=[]
	valor=len(ciudades)
	for i in range(size):
		ruta=[]
		camino=copy.copy(ciudades)
		permutacion(camino, valor)
		ruta.append(camino)
		ruta.append(100000)
		ruta.append(local)
		ruta.append(velocidad)
		temp=copy.copy(ruta)
		poblacion.append(temp)
		del ruta[:]				

	return poblacion


def fitness(ruta):
	costo=0
	size=len(ruta)-1
	for i in range(size):
		costo+=distancias[ord(ruta[i])%65][ord(ruta[i+1])%65]	

	return costo

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


def actualizar_velocidad(x,local_,global_):
	copia=copy.copy(local_)
	copia2=copy.copy(global_)
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
	per_global=0
	fit_lg=10000000	
	it=0
	
	while(it<iteraciones):
		print "*************************Iteracion ",it+1,"*******************************"
		for i in range(size):
			temp=fitness(pob[i][0])
			if temp<pob[i][1]:
				pob[i][2]=copy.copy(pob[i][0])
				pob[i][1]=temp

			if temp<fit_lg:
				fit_lg=temp
				per_global=pob[i][0]
							 	

		for i in range(size):	
			print i+1," Actual", pob[i][0],"fitness: ",fitness(pob[i][0])
			print "Mejor", pob[i][2],"fitness: ",fitness(pob[i][2])	
			velocidad=actualizar_velocidad(pob[i][0],pob[i][2],per_global)
			if len(velocidad)!=0:
				pob[i][0]=actualizar_x(pob[i][0],velocidad)
			
			print "Velocidad:", pob[i][3]
			pob[i][3]=velocidad
			print 

		it+=1

		print "Mejor Global:",per_global,"fitness: ",fitness(per_global)
		print 	
	

ciudades=['A','B','C','D','E']
iteraciones=4
size=4
pso(ciudades,size)




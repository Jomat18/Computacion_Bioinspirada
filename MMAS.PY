import numpy as np
import copy

#del a[i] i indice
# a.pop(i) i indice
# a.remove(elemento) 

distancias=[[0,12,6,4],
	    [12,0,6,8],
	    [6,6,0,7],
	    [4,8,7,0]]			


flujo=[[0,3,8,3],
       [3,0,2,4],
       [8,2,0,5],
       [3,4,5,0]]


def producto(f, d, size):
	resultado=0;	
	for i in range(size):
		resultado+=f[i]*d[i]		
			
	return resultado

def columna_fila(index,size):
	lista=[]
	for i in range(size):
		lista.append(distancias[i][index])
	
	return lista

def m_visibilidad():
	size=len(distancias)
	visibilidad=[0]*size
	for i in range(size):
		visibilidad[i]=[0]*size
		for j in range(size):
			if i!=j:
				visibilidad[i][j]=float("%.5f"%(1.0/producto(flujo[i],columna_fila(j,size),size)))
			else:
				visibilidad[i][j]=0

	return visibilidad


def m_feromonas():
	size=len(distancias)
	feromonas=[0]*size
	for i in range(size):
		feromonas[i]=[0]*size
		for j in range(size):
			if i!=j:
				feromonas[i][j]=feromona_inicial
			else:
				feromonas[i][j]=0

	return feromonas


def calcular_ruta(ciudades_destino):
	ruta=[]
	ciudad_inicial=np.random.choice(orden)
	ruta.append(ciudad_inicial)
	ciudades_destino.remove(ciudad_inicial)
	while len(ciudades_destino)!=0:
		suma=0		
		size=len(ciudades_destino)
		probabilidad=[0.0]*size
		for i in range(size):
			t=feromona[ciudad_inicial-1][ciudades_destino[i]-1]
			t=pow(t,alpha) 
			n=visibilidad[ciudad_inicial-1][ciudades_destino[i]-1] 
			n=pow(n,beta) 
			probabilidad[i]=t*n
			suma+=t*n	
	
		hasta=len(probabilidad)
		suma_probabilidad=0
		for i in range(hasta):
			probabilidad[i]=(probabilidad[i]/suma)+suma_probabilidad
			suma_probabilidad+=probabilidad[i]


		aleatorio=np.random.uniform(0,1)
		
		for i in range(hasta):
			if aleatorio<probabilidad[i]:
				ciudad_inicial=ciudades_destino[i]
				ruta.append(ciudad_inicial)	
				ciudades_destino.remove(ciudad_inicial)
				break

				
	return ruta

def fitness(permutacion):
	costo=0
	size=len(permutacion)
	
	for i in range(size):
		fila=permutacion[i]-1
		permutacion_copy=copy.copy(permutacion)
		a=range(size)
		a.remove(i)
		permutacion_copy.pop(i)
		for j,k in zip(a,permutacion_copy): 
			costo+=flujo[i][j]*distancias[fila][k-1]	

	return costo

def actualizar_feromona(mejor_permutacion, mejor_solucion):
	size=len(distancias)
	sumas=[0.0]
	agregar=True
	
	for i in range(size-1):
		for j in range(i+1,size):
			inicio=orden[i]
			fin=orden[j]
			suma_delta=(1-p)*feromona[inicio-1][fin-1]
			sumas.append(suma_delta)			
			for r in range(len(mejor_permutacion)-1):
				if inicio==mejor_permutacion[r] or fin==mejor_permutacion[r]:
					if  inicio==mejor_permutacion[r+1] or fin==mejor_permutacion[r+1]:
						temp=1.0/mejor_solucion
						agregar=False
						sumas.append(temp)
						break
				
			if agregar:			
				sumas.append(0.0)
				
			agregar=True	
					
			actualizar=sum(sumas)
			if actualizar>t_max:
				actualizar=t_max
			if actualizar<t_min:
				actualizar=t_min

			print(inicio,fin,"valor: ",actualizar)
			del sumas[:]
			feromona[inicio-1][fin-1]=actualizar
			feromona[fin-1][inicio-1]=actualizar



def generaciones():
	rutas=[None]*n_hormigas
	for i in range(n_hormigas):
		rutas[i]=[0]*len(orden)

	fitness_hormigas=[0.0]*n_hormigas
	#solucion_best=1000000
	#permutacion_best=[0]*len(flujo)	
	
	for m in range(n_iteraciones):
		print("********************Iteracion: ",m+1,"**********************")
		for i in range(n_hormigas):
			ciudades_destino=copy.copy(orden)
			rutas[i]=calcular_ruta(ciudades_destino)
			fitness_hormigas[i]=fitness(rutas[i])
			print("Hormiga: ",i+1,rutas[i]," costo: ", fitness_hormigas[i])

		menor=np.argsort(fitness_hormigas)
		#if fitness_hormigas[menor[0]]<solucion_best:
		#	solucion_best=fitness_hormigas[menor[0]]
		#	permutacion_best=rutas[menor[0]]

		print("Mejor hormiga :",rutas[menor[0]],"costo:", fitness_hormigas[menor[0]])
		actualizar_feromona(rutas[menor[0]], fitness_hormigas[menor[0]])
	

#Parametros
p = 0.9
alpha = 1
beta = 1
n_hormigas = 10
n_iteraciones = 100
orden=[1,2,3,4]
t_max=10.0
t_min=0.1
feromona_inicial = t_max
visibilidad = m_visibilidad()
feromona = m_feromonas()
generaciones()




















